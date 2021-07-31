import sys
import os
import json
import time
from datetime import date

try:
    from wox import Wox as Launcher
    from wox import WoxAPI as API
    PRETEXT = 'Wox'
except ModuleNotFoundError:
    from .lib.flowlauncher import FlowLauncher as Launcher
    from .lib.flowlauncher import FlowLauncherAPI as API
    PRETEXT = 'Flow.Launcher'

PLUGIN_MANIFEST = 'plugin.json'

APP_ICONS = os.path.join(os.path.dirname(os.getenv('PYTHONPATH')), 'Images')

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

    def __init__(self, lib=None):
        self._start = time.time()
        self._manifest = None
        self._results = []
        self._plugindir = None
        self._approam = None
        self._appdir = None
        self._app_settings = None
        self._user_keywords = None
        self._appversion = None
        if lib:
            lib_path = os.path.join(plugindir, lib)
            sys.path.append(lib_path)
        super().__init__()


    def query(self, query):
        try:
            self.args = query.lower()
            self.query = query

            self._query(query)

        except Exception as e:
            self.add_item(
                title=e.__class__.__name__,
                subtitle=str(e)
            )
        return self._results

    def context_menu(self, data):
        try:

            self._context_menu()

        except Exception as e:
            self.add_item(
                title=e.__class__.__name__,
                subtitle=str(e)
            )
        return self._results

    def add_item(self, title, subtitle='', icon=None, method=None, parameters=None, context=None, hide=False):

        item = {
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": icon or self.icon,
            "ContextData": context,
            "JsonRPCAction": {}
        }
        item['JsonRPCAction']['method'] = method
        item['JsonRPCAction']['parameters'] = parameters
        item['JsonRPCAction']['dontHideAfterAction'] = hide        
        self._results.append(item)
        return item

    @property
    def plugindir(self):

        if not self._plugindir:
            potential_paths = [
                os.path.abspath(os.getcwd()),
                os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
            ]

            for path in potential_paths:

                while True:
                    if os.path.exists(os.path.join(path, PLUGIN_MANIFEST)):
                        self._plugindir = path
                        break
                    elif path == '/':
                        break

                    path = os.path.dirname(path)

                if self._plugindir:
                    break

        return self._plugindir

    @property
    def manifest(self):
        if not self._manifest:
            with open(os.path.join(self.plugindir, PLUGIN_MANIFEST), 'r') as f:
                self._manifest = json.load(f)
        return self._manifest

    @property
    def id(self):
        return self.manifest['ID']

    @property
    def icon(self):
        return self.manifest['IcoPath']

    @property
    def action_keyword(self):
        return self.manifest['ActionKeyword']

    @property
    def version(self):
        return self.manifest['Version']

    @property
    def approam(self):
        if not self._approam:
            potential_approam = os.path.dirname(os.path.dirname(self.plugindir))
            if os.path.exists(os.path.join(potential_approam, 'Plugins')):
                self._approam = potential_approam
            elif PRETEXT == 'Flow.Launcher':
                self._approam = os.path.join(os.getenv('approam'), 'FlowLauncher')
            elif PRETEXT == 'Wox':
                self._approam = os.path.join(os.getenv('approam'), 'Wox')
        return self._approam

    @property
    def app_settings(self):
        if not self._app_settings:
            with open(os.path.join(self.approam, 'Settings', 'Settings.json'), 'r') as f:
                self._app_settings = json.load(f)
        return self._app_settings

    @property
    def user_keywords(self):
        if not self._user_keywords:
            self._user_keywords = self.app_settings['PluginSettings']['Plugins'][self.id]['ActionKeywords']
        return self._user_keywords

    @property
    def user_keyword(self):
        return self.user_keywords[0]

    @property
    def appdir(self):
        if not self._appdir:
            self._appdir = os.path.dirname(os.getenv('PYTHONPATH'))
        return self._appdir

    def appicon(self, icon):
        return os.path.join(self.appdir, 'images', icon + '.png')

    @property
    def applog(self):
        today = date.today().strftime('%Y-%m-%d')
        file = f"{today}.txt"
        return os.path.join(self.approam, 'Logs', self.appversion, file)

    
    @property
    def appversion(self):
        if not self._appversion:
            self._appversion = os.path.basename(self.appdir).replace('app-', '')
        return self._appversion
