# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import psutil
import time
from src.utils.telegram_debug import SendlerOneCreate
from src.utils._logger import logger_msg


def close_old_chrome_process(name_process):
    """Полное закрытие всех процессов Chrome включая дочерние"""
    try:
        # Получаем все процессы Chrome
        chrome_processes = []
        for process in psutil.process_iter(['pid', 'name', 'ppid']):
            if any(proc_name.lower() in process.info['name'].lower() for proc_name in name_process):
                chrome_processes.append(process)
        
        if not chrome_processes:
            logger_msg("Chrome процессы не найдены")
            return True
            
        # Сначала пытаемся мягко завершить процессы
        for process in chrome_processes:
            try:
                process.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Ждем завершения
        time.sleep(3)
        
        # Принудительно убиваем оставшиеся процессы
        for process in chrome_processes:
            try:
                if process.is_running():
                    process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        # Дополнительная проверка и очистка
        time.sleep(2)
        remaining_processes = []
        for process in psutil.process_iter(['pid', 'name']):
            if any(proc_name.lower() in process.info['name'].lower() for proc_name in name_process):
                remaining_processes.append(process)
                try:
                    process.kill()
                except:
                    pass
                    
        if remaining_processes:
            logger_msg(f"Принудительно завершено {len(remaining_processes)} оставшихся Chrome процессов")
            
        return True
        
    except Exception as es:
        error_msg = f'WB DDR: ▶️ Ошибка при закрытии Chrome процессов "{es}"'
        SendlerOneCreate('').save_text(error_msg)
        logger_msg(error_msg)
        return False
