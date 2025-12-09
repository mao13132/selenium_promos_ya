# ---------------------------------------------
# Program by @developer_telegrams
# Модуль грамотного закрытия браузера
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time
import psutil
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, InvalidSessionIdException

from src.utils._logger import logger_msg


class GracefulBrowserShutdown:
    """Класс для грамотного закрытия браузера без влияния на другие Chrome процессы"""

    def __init__(self, driver, name_profile_chrome):
        self.driver = driver
        self.browser_pid = None
        self.chrome_process = None
        self.name_profile_chrome = name_profile_chrome
        self._get_browser_process_info()

    def _get_browser_process_info(self):
        """Получает информацию о процессе браузера по PID"""
        try:
            if hasattr(self.driver, 'service') and hasattr(self.driver.service, 'process'):
                # Получаем PID chromedriver
                chromedriver_pid = self.driver.service.process.pid

                # Ищем дочерний процесс Chrome
                for process in psutil.process_iter():
                    try:
                        # Получаем информацию о процессе через отдельные методы
                        process_pid = process.pid
                        process_ppid = process.ppid()
                        process_name = process.name()

                        # Проверяем что это дочерний процесс chromedriver и это Chrome
                        if (process_ppid == chromedriver_pid and
                                'chrome' in process_name.lower()):
                            self.browser_pid = process_pid
                            self.chrome_process = process
                            break

                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue

            # Альтернативный способ через capabilities
            if not self.browser_pid:
                try:
                    # Пытаемся получить PID через JavaScript
                    pid_script = "return navigator.userAgent;"
                    self.driver.execute_script(pid_script)

                    # Ищем процесс по user-data-dir
                    user_data_dir = None
                    for process in psutil.process_iter():
                        try:
                            process_name = process.name()
                            process_cmdline = process.cmdline()
                            process_pid = process.pid

                            if ('chrome' in process_name.lower() and
                                    process_cmdline and
                                    any('--user-data-dir' in arg for arg in process_cmdline)):

                                # Проверяем что это наш профиль
                                for arg in process_cmdline:
                                    if '--user-data-dir' in arg and self.name_profile_chrome in arg:
                                        self.browser_pid = process_pid
                                        self.chrome_process = process
                                        break

                                if self.browser_pid:
                                    break
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue

                except Exception as e:
                    logger_msg(f"Не удалось получить PID через альтернативный способ: {e}")

        except Exception as e:
            logger_msg(f"Ошибка при получении информации о процессе браузера: {e}")

    def graceful_shutdown(self, timeout=30):
        """Грамотное закрытие браузера с проверками и таймаутами"""
        try:
            # Этап 0: Пытаемся закрыть браузер через CDP в первую очередь
            try:
                try:
                    setattr(self.driver, '_closed_by_cdp', True)
                except Exception:
                    pass

                self.driver.execute_cdp_cmd("Browser.close", {})
            except Exception:
                pass

            # Проверяем, завершился ли процесс после CDP закрытия (короткий таймаут)
            if self._verify_process_terminated(timeout=min(10, timeout)):
                return True

            # Этап 1: Закрываем все вкладки кроме одной
            self._close_extra_tabs()

            # Этап 2: Graceful quit через WebDriver
            success = self._webdriver_quit(timeout=10)

            if success:
                # Этап 3: Проверяем что процесс действительно завершился
                return self._verify_process_terminated(timeout=timeout)
            else:
                # Этап 4: Принудительное завершение только нашего процесса
                return self._force_terminate_browser_process()

        except Exception as e:
            logger_msg(f"Ошибка при грамотном закрытии браузера: {e}")
            return self._force_terminate_browser_process()

    def _close_extra_tabs(self):
        """Закрывает все вкладки кроме одной"""
        try:
            handles = self.driver.window_handles

            # Оставляем только одну вкладку
            for i, handle in enumerate(handles[1:], 1):
                try:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
                except Exception as e:
                    logger_msg(f"Не удалось закрыть вкладку {i}: {e}")

            # Переключаемся на оставшуюся вкладку
            if handles:
                self.driver.switch_to.window(handles[0])

        except Exception as e:
            logger_msg(f"Ошибка при закрытии вкладок: {e}")

    def _webdriver_quit(self, timeout=10):
        """Пытается закрыть браузер через WebDriver API"""
        try:
            # Устанавливаем короткий таймаут для операций
            self.driver.implicitly_wait(1)

            # Вызываем quit
            self.driver.quit()

            # Ждем завершения
            start_time = time.time()
            while time.time() - start_time < timeout:
                if not self._is_browser_process_running():
                    return True
                time.sleep(0.5)

            logger_msg(f"WebDriver quit не завершился за {timeout} секунд")
            return False

        except (WebDriverException, InvalidSessionIdException, NoSuchWindowException):
            # Эти исключения ожидаемы при закрытии
            time.sleep(2)
            return not self._is_browser_process_running()

        except Exception as e:
            logger_msg(f"Ошибка при WebDriver quit: {e}")
            return False

    def _is_browser_process_running(self):
        """Проверяет, запущен ли процесс браузера"""
        try:
            if self.chrome_process:
                return self.chrome_process.is_running()
            elif self.browser_pid:
                return psutil.pid_exists(self.browser_pid)
            return False
        except:
            return False

    def _verify_process_terminated(self, timeout=20):
        """Проверяет что процесс браузера действительно завершился"""
        try:
            start_time = time.time()

            while time.time() - start_time < timeout:
                if not self._is_browser_process_running():
                    return True

                time.sleep(0.5)

            logger_msg(f"Процесс браузера не завершился за {timeout} секунд")
            return False

        except Exception as e:
            logger_msg(f"Ошибка при проверке завершения процесса: {e}")
            return False

    def _force_terminate_browser_process(self):
        """Принудительно завершает только процесс нашего браузера"""
        try:
            if not self.chrome_process and not self.browser_pid:
                logger_msg("Нет информации о процессе браузера для принудительного завершения")
                return True

            logger_msg(f"Принудительное завершение процесса браузера PID: {self.browser_pid}")

            if self.chrome_process:
                # Сначала пытаемся мягко завершить
                try:
                    self.chrome_process.terminate()
                    time.sleep(3)

                    if not self.chrome_process.is_running():
                        logger_msg("Процесс браузера завершен через terminate()")
                        return True

                except psutil.NoSuchProcess:
                    logger_msg("Процесс уже завершен")
                    return True

                # Если не помогло - принудительно
                try:
                    self.chrome_process.kill()
                    time.sleep(2)
                    logger_msg("Процесс браузера принудительно завершен через kill()")
                    return True

                except psutil.NoSuchProcess:
                    logger_msg("Процесс уже завершен")
                    return True

            return True

        except Exception as e:
            logger_msg(f"Ошибка при принудительном завершении процесса: {e}")
            return False

    def emergency_cleanup(self):
        """Экстренная очистка при критических ошибках"""
        try:
            logger_msg("Выполняю экстренную очистку браузера...")

            # Пытаемся любыми способами закрыть драйвер
            try:
                if hasattr(self.driver, 'quit'):
                    self.driver.quit()
            except:
                pass

            # Принудительно завершаем процесс
            self._force_terminate_browser_process()

            # Дополнительная пауза
            time.sleep(3)

            logger_msg("Экстренная очистка завершена")
            return True

        except Exception as e:
            logger_msg(f"Ошибка при экстренной очистке: {e}")
            return False


def graceful_browser_shutdown(driver, name_profile_chrome, timeout=30):
    """Функция-обертка для грамотного закрытия браузера"""
    if not driver:
        logger_msg("Драйвер не передан для закрытия")
        return True

    shutdown_manager = GracefulBrowserShutdown(driver, name_profile_chrome)
    return shutdown_manager.graceful_shutdown(timeout=timeout)


def emergency_browser_cleanup(driver, name_profile_chrome):
    """Функция экстренной очистки браузера"""
    if not driver:
        return True

    shutdown_manager = GracefulBrowserShutdown(driver, name_profile_chrome)
    return shutdown_manager.emergency_cleanup()

