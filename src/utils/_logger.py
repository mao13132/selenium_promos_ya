# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import logging


def logger_msg(message):
    _msg = f'Logger ddr: {message}'

    logging.error(_msg)

    print(_msg)
