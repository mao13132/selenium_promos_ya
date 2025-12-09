import os

import undetected_chromedriver as uc


class CreatBrowser:
    def __init__(self, path_short_chrome, name_profile_chrome):

        options = uc.ChromeOptions()

        options.add_argument('--no-sandbox')

        options.add_argument('--disable-dev-shm-usage')

        options.add_argument("--log-level=3")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")

        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")

        options.add_argument("--disable-extensions")
        options.add_argument('--disable-application-cache')
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument('--headless=new')

        options.add_argument("--password-store=basic")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        # options.add_argument(
        #     "--disable-features=PrivacySandboxSettings4,PrivacySandboxAdsAPIs,Topics,AdMeasurement,ProtectedAudience,FirstPartySets")
        #
        # options.add_argument("--disable-features=OptimizationGuideModelDownloading,OptimizationHints")
        # options.add_argument("--disable-features=InterestFeedV2,Feed")
        # options.add_argument("--disable-features=AutofillServerCommunication")
        options.add_argument(
            "--disable-features="
            "OptimizationGuideModelDownloading,"
            "OptimizationHints,"
            "InterestFeedV2,"
            "Feed,"
            "AutofillServerCommunication,"
            "TranslateUI,"
            "PrivacySandboxSettings4,"
            "PrivacySandboxAdsAPIs,"
            "Topics,"
            "AdMeasurement,"
            "ProtectedAudience,"
            "FirstPartySets"
        )
        # ускорение
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-component-update")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-background-timer-throttling")

        # Уведомления
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        options.add_argument("--disable-ipv6")

        full_path = os.path.join(path_short_chrome, name_profile_chrome)

        os.makedirs(full_path, exist_ok=True)

        options.add_argument(f'--user-data-dir={full_path}')
        options.add_argument(f"--profile-directory=Default")

        experimental_options = {
            'prefs': {'profile.default_content_setting_values.notifications': 2}
        }

        # отключаем копирование профиля UC
        uc.TARGET_VERSION = None
        uc.Patcher().auto = False

        for key, value in experimental_options.items():
            options.add_experimental_option(key, value)

        self.driver = uc.Chrome(
            options=options,
            version_main=None,  # Автоопределение версии
            driver_executable_path=None,  # Автоматический поиск
        )

        if self.driver:
            self.driver.maximize_window()

            try:
                browser_version = self.driver.capabilities['browserVersion']
                driver_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
                print(f"\nБраузер: {browser_version} драйвер: {driver_version}. Профиль: {path_short_chrome}")
            except:
                print(f'\nНе получилось определить версию uc браузера')
