import logging
import logging.handlers

from .plugin import Plugin
from .launcher import launcher, Launcher
from .item import Item, JsonRPCAction, Glyph


log = logging.getLogger('')
if not log.handlers:
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s (%(filename)s): %(message)s',
        datefmt='%H:%M:%S')
    logfile = logging.handlers.RotatingFileHandler(
            "flox.log",
            maxBytes=1024 * 2024,
            backupCount=1)
    logfile.setFormatter(formatter)
    log.addHandler(logfile)
    log.setLevel(logging.DEBUG)