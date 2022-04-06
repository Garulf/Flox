import sys
import traceback
import os
import json
import time
import webbrowser
import urllib.parse
from datetime import date
import logging
import logging.handlers
from pathlib import Path
from typing import Union
from functools import wraps, cached_property
from tempfile import gettempdir

from .launcher import Launcher
from .browser import Browser

PLUGIN_MANIFEST = 'plugin.json'
FLOW_LAUNCHER_DIR_NAME = "FlowLauncher"
WOX_DIR_NAME = "Wox"
FLOW_API = 'Flow.Launcher'
WOX_API = 'Wox'
LOCALAPPDATA = Path(os.getenv('LOCALAPPDATA'))
APPDATA = Path(os.getenv('APPDATA'))
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CURRENT_WORKING_DIR = Path().cwd()


launcher_dir = None
if str(FLOW_LAUNCHER_DIR_NAME) in CURRENT_WORKING_DIR.parts:
    launcher_dir = FLOW_LAUNCHER_DIR_NAME
    API = FLOW_API
elif str(WOX_DIR_NAME) in CURRENT_WORKING_DIR.parts:
    launcher_dir = WOX_DIR_NAME
    API = WOX_API

if str(APPDATA.joinpath(launcher_dir)) in str(CURRENT_WORKING_DIR):
    USER_DIR = APPDATA.joinpath(launcher_dir)
    APP_DIR = LOCALAPPDATA.joinpath(launcher_dir)
elif "UserData" in CURRENT_WORKING_DIR.parts:
    USER_DIR = CURRENT_WORKING_DIR.parts[:-2]
    APP_DIR = CURRENT_WORKING_DIR.parts[:-3]
elif APPDATA.joinpath(FLOW_LAUNCHER_DIR_NAME).exits():
    USER_DIR = APPDATA.joinpath(FLOW_LAUNCHER_DIR_NAME)
    APP_DIR = LOCALAPPDATA.joinpath(FLOW_LAUNCHER_DIR_NAME)
    API = FLOW_API
elif APPDATA.joinpath(WOX_DIR_NAME).exits():
    USER_DIR = APPDATA.joinpath(WOX_DIR_NAME)
    APP_DIR = LOCALAPPDATA.joinpath(WOX_DIR_NAME)
    API = WOX_API
else:
    raise FileNotFoundError("Unable to locate Launcher directory")
    

APP_ICONS = os.path.join(APP_DIR, "Images")
ICON_APP = os.path.join(APP_ICONS, 'app.png')
ICON_APP_ERROR = os.path.join(APP_ICONS, 'app_error.png')
ICON_BROWSER = os.path.join(APP_ICONS, 'browser.png')
ICON_CALCULATOR = os.path.join(APP_ICONS, 'calculator.png')
ICON_CANCEL = os.path.join(APP_ICONS, 'cancel.png')
ICON_CLOSE = os.path.join(APP_ICONS, 'close.png')
ICON_CMD = os.path.join(APP_ICONS, 'cmd.png')
ICON_COLOR = os.path.join(APP_ICONS, 'color.png')
ICON_CONTROL_PANEL = os.path.join(APP_ICONS, 'ControlPanel.png')
ICON_COPY = os.path.join(APP_ICONS, 'copy.png')
ICON_DELETE_FILE_FOLDER = os.path.join(APP_ICONS, 'deletefilefolder.png')
ICON_DISABLE = os.path.join(APP_ICONS, 'disable.png')
ICON_DOWN = os.path.join(APP_ICONS, 'down.png')
ICON_EXE = os.path.join(APP_ICONS, 'exe.png')
ICON_FILE = os.path.join(APP_ICONS, 'file.png')
ICON_FIND = os.path.join(APP_ICONS, 'find.png')
ICON_FOLDER = os.path.join(APP_ICONS, 'folder.png')
ICON_HISTORY = os.path.join(APP_ICONS, 'history.png')
ICON_IMAGE = os.path.join(APP_ICONS, 'image.png')
ICON_LOCK = os.path.join(APP_ICONS, 'lock.png')
ICON_LOGOFF = os.path.join(APP_ICONS, 'logoff.png')
ICON_OK = os.path.join(APP_ICONS, 'ok.png')
ICON_OPEN = os.path.join(APP_ICONS, 'open.png')
ICON_PICTURES = os.path.join(APP_ICONS, 'pictures.png')
ICON_PLUGIN = os.path.join(APP_ICONS, 'plugin.png')
ICON_PROGRAM = os.path.join(APP_ICONS, 'program.png')
ICON_RECYCLEBIN = os.path.join(APP_ICONS, 'recyclebin.png')
ICON_RESTART = os.path.join(APP_ICONS, 'restart.png')
ICON_SEARCH = os.path.join(APP_ICONS, 'search.png')
ICON_SETTINGS = os.path.join(APP_ICONS, 'settings.png')
ICON_SHELL = os.path.join(APP_ICONS, 'shell.png')
ICON_SHUTDOWN = os.path.join(APP_ICONS, 'shutdown.png')
ICON_SLEEP = os.path.join(APP_ICONS, 'sleep.png')
ICON_UP = os.path.join(APP_ICONS, 'up.png')
ICON_UPDATE = os.path.join(APP_ICONS, 'update.png')
ICON_URL = os.path.join(APP_ICONS, 'url.png')
ICON_USER = os.path.join(APP_ICONS, 'user.png')
ICON_WARNING = os.path.join(APP_ICONS, 'warning.png')
ICON_WEB_SEARCH = os.path.join(APP_ICONS, 'web_search.png')
ICON_WORK = os.path.join(APP_ICONS, 'work.png')


class Flox(Launcher):

    def __init_subclass__(cls, api=API, app_dir=APP_DIR, user_dir=USER_DIR):
        cls._debug = False
        cls.appdir = APP_DIR
        cls.user_dir = USER_DIR
        cls.api = api
        cls._start = time.time()
        cls._results = []
        cls._settings = None
        cls.font_family = '/Resources/#Segoe Fluent Icons'
        cls.issue_item_title = 'Report Issue'
        cls.issue_item_subtitle = 'Report this issue to the developer'

    @cached_property
    def browser(self):
        return Browser(self.app_settings)

    def exception(self, exception):
        self.exception_item(exception)
        self.issue_item(exception)

    def _query(self, query):
        self.args = query.lower()

        self.query(query)

    def _context_menu(self, data):
        self.context_menu(data)

    def exception_item(self, exception):
        self.add_item(
            title=exception.__class__.__name__,
            subtitle=str(exception),
            icon=ICON_APP_ERROR,
            method=self.change_query,
            dont_hide=True
        )

    def issue_item(self, e):
        trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)).replace('\n', '%0A')
        self.add_item(
            title=self.issue_item_title,
            subtitle=self.issue_item_subtitle,
            icon=ICON_BROWSER,
            method=self.create_github_issue,
            parameters=[e.__class__.__name__, trace],
        )

    def create_github_issue(self, title, trace, log=None):
        url = self.manifest['Website']
        if 'github' in url.lower():
            issue_body = f"Please+type+any+relevant+information+here%0A%0A%0A%0A%0A%0A%3Cdetails open%3E%3Csummary%3ETrace+Log%3C%2Fsummary%3E%0A%3Cp%3E%0A%0A%60%60%60%0A{trace}%0A%60%60%60%0A%3C%2Fp%3E%0A%3C%2Fdetails%3E"
            url = f"{url}/issues/new?title={title}&body={issue_body}"
        webbrowser.open(url)

    def add_item(self, title:str, subtitle:str='', icon:str=None, method:Union[str, callable]=None, parameters:list=None, context:list=None, glyph:str=None, score:int=0, **kwargs):
        icon = icon or self.icon
        if not Path(icon).is_absolute():
            icon = Path(self.plugindir, icon)
        item = {
            "Title": str(title),
            "SubTitle": str(subtitle),
            "IcoPath": str(icon),
            "ContextData": context,
            "Score": score,
            "JsonRPCAction": {}
        }
        auto_complete_text = kwargs.pop("auto_complete_text", None)

        item["AutoCompleteText"] = auto_complete_text or f'{self.user_keyword} {title}'.replace('* ', '')
        if method:
            item['JsonRPCAction']['method'] = getattr(method, "__name__", method)
            item['JsonRPCAction']['parameters'] = parameters or []
            item['JsonRPCAction']['dontHideAfterAction'] = kwargs.pop("dont_hide", False)
        if glyph:
            item['Glyph'] = {}
            item['Glyph']['Glyph'] = glyph
            font_family =  kwargs.pop("font_family", self.font_family)
            if font_family.startswith("#"):
                font_family = str(Path(self.plugindir).joinpath(font_family))
            item['Glyph']['FontFamily'] = font_family
        for kw in kwargs:
            item[kw] = kwargs[kw]
        self._results.append(item)
        return self._results[-1]

    @cached_property
    def plugindir(self):
        potential_paths = [
            os.path.abspath(os.getcwd()),
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        ]

        for path in potential_paths:

            while True:
                if os.path.exists(os.path.join(path, PLUGIN_MANIFEST)):
                    return path
                elif os.path.ismount(path):
                    return os.getcwd()

                path = os.path.dirname(path)

    @cached_property
    def manifest(self):
        with open(os.path.join(self.plugindir, PLUGIN_MANIFEST), 'r') as f:
            return json.load(f)

    @cached_property
    def id(self):
        return self.manifest['ID']

    @cached_property
    def icon(self):
        return self.manifest['IcoPath']

    @cached_property
    def action_keyword(self):
        return self.manifest['ActionKeyword']

    @cached_property
    def version(self):
        return self.manifest['Version']

    @cached_property
    def appdata(self):
        # Userdata should be up two directories from plugin root
        return os.path.dirname(os.path.dirname(self.plugindir))

    @property
    def app_settings(self):
        with open(os.path.join(self.appdata, 'Settings', 'Settings.json'), 'r') as f:
            return json.load(f)

    @cached_property
    def user_keywords(self):
        return self.app_settings['PluginSettings']['Plugins'].get(self.id, {}).get('UserKeywords', [self.action_keyword])

    @cached_property
    def user_keyword(self):
        return self.user_keywords[0]

    @cached_property
    def appicon(self, icon):
        return os.path.join(self.appdir, 'images', icon + '.png')

    @property
    def applog(self):
        today = date.today().strftime('%Y-%m-%d')
        file = f"{today}.txt"
        return os.path.join(self.appdata, 'Logs', self.appversion, file)

    
    @cached_property
    def appversion(self):
        return os.path.basename(self.appdir).replace('app-', '')

    @cached_property
    def logfile(self):
        file = "plugin.log"
        return os.path.join(self.plugindir, file)

    @cached_property
    def logger(self):
        logger = logging.getLogger('')
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s (%(filename)s): %(message)s',
            datefmt='%H:%M:%S')
        logfile = logging.handlers.RotatingFileHandler(
                self.logfile,
                maxBytes=1024 * 2024,
                backupCount=1)
        logfile.setFormatter(formatter)
        logger.addHandler(logfile)
        logger.setLevel(logging.WARNING)
        return logger

    def logger_level(self, level):
        if level == "info":
            self.logger.setLevel(logging.INFO)
        elif level == "debug":
            self.logger.setLevel(logging.DEBUG)
        elif level == "warning":
            self.logger.setLevel(logging.WARNING)
        elif level == "error":
            self.logger.setLevel(logging.ERROR)
        elif level == "critical":
            self.logger.setLevel(logging.CRITICAL)

    @cached_property
    def api(self):
        launcher = os.path.basename(os.path.dirname(self.appdir))
        if launcher == 'FlowLauncher':
            return FLOW_API
        else:
            return WOX_API

    @cached_property
    def name(self):
        return self.manifest['Name']

    @cached_property
    def author(self):
        return self.manifest['Author']

    @cached_property
    def settings_path(self):
        dirname = self.name
        setting_file = "Settings.json"
        return os.path.join(self.appdata, 'Settings', 'Plugins', dirname, setting_file)

    @cached_property
    def settings(self):
        if not os.path.exists(os.path.dirname(self.settings_path)):
            os.mkdir(os.path.dirname(self.settings_path))
        return Settings(self.settings_path)

    def browser_open(self, url):
        self.browser.open(url)

    @cached_property
    def python_dir(self):
        return self.app_settings["PluginSettings"]["PythonDirectory"]

class Settings(dict):

    def __init__(self, filepath):
        super(Settings, self).__init__()
        self._filepath = filepath
        self._save = True
        if os.path.exists(self._filepath):
            self._load()
        else:
            data = {}
            self.update(data)
            self.save()

        
    def _load(self):
        data = {}
        with open(self._filepath, 'r') as f:
            try:
                data.update(json.load(f))
            except json.decoder.JSONDecodeError:
                pass

        self._save = False
        self.update(data)
        self._save = True

    def save(self):
        if self._save:
            data = {}
            data.update(self)
            with open(self._filepath, 'w') as f:
                json.dump(data, f, sort_keys=True, indent=4)
        return
    
    def __setitem__(self, key, value):
        super(Settings, self).__setitem__(key, value)
        self.save()

    def __delitem__(self, key):
        super(Settings, self).__delitem__(key)
        self.save()

    def update(self, *args, **kwargs):
        super(Settings, self).update(*args, **kwargs)
        self.save()

    def setdefault(self, key, value=None):
        ret = super(Settings, self).setdefault(key, value)
        self.save()
        return ret
