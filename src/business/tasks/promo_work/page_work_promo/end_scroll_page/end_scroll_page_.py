# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
def is_end_scroll_page(driver):
    try:
        is_at_bottom = driver.execute_script("""
        return window.innerHeight + window.pageYOffset >= document.body.scrollHeight;
        """)
    except:
        return False

    return is_at_bottom
