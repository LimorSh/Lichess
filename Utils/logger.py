import logging
import os
import sys


if sys.platform.lower() in ['linux', 'darwin'] or sys.platform.lower().startswith('linux'):
    LOG_PATH = "/var/log/installer_app"
else:
    LOG_PATH = "{}/Desktop/Python/Logs".format(os.getenv('USERPROFILE'))

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
basename = os.path.basename(sys.argv[0])
logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)


def do_file_handler():
    fh = logging.FileHandler("{}/{}.log".format(LOG_PATH, basename))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(module)s.%(funcName)s -> %(lineno)d-%(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def do_stream_handler():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(module)s.%(funcName)s -> %(lineno)d-%(levelname)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def do_timed_rotating_file_handler():
    import json
    from logging.handlers import TimedRotatingFileHandler
    rh = TimedRotatingFileHandler(
        "{}/{}.json.log".format(LOG_PATH, basename),
        when="m",
        interval=1,
        backupCount=5)
    rh.setLevel(logging.DEBUG)
    json_fmt = {
        'ts': '%(asctime)s',
        'module': '%(module)s',
        'func': '%(funcName)s',
        'line': '%(lineno)d',
        'level': '%(levelname)s',
        'msg': '%(message)s',
        'name': 'ReverseProxy',
    }
    formatter = logging.Formatter(json.dumps(json_fmt))
    rh.setFormatter(formatter)
    logger.addHandler(rh)


do_file_handler()
do_stream_handler()
# do_timed_rotating_file_handler()
