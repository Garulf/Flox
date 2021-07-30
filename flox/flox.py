import sys
import os
import json
import time
import traceback


try:
    from wox import Wox as Launcher
    from wox import WoxAPI as API
    PRETEXT = 'Wox'
except ModuleNotFoundError:
    from .lib.flowlauncher import FlowLauncher as Launcher
    from .lib.flowlauncher import FlowLauncherAPI as API
    PRETEXT = 'Flow.Launcher'

PLUGIN_MANIFEST = 'plugin.json'


class Flox(Launcher):

    def __init__(self, lib=None):
        self._start = time.time()
        self._manifest = None
        self._results = []
        self._plugindir = None
        self._appdir = None
        self._app_settings = None
        self._user_keywords = None
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
    def appdir(self):
        if not self._appdir:
            potential_appdir = os.path.dirname(os.path.dirname(self.plugindir))
            if os.path.exists(os.path.join(potential_appdir, 'Plugins')):
                self._appdir = potential_appdir
            elif PRETEXT == 'Flow.Launcher':
                self._appdir = os.path.join(os.getenv('APPDATA'), 'FlowLauncher')
            elif PRETEXT == 'Wox':
                self._appdir = os.path.join(os.getenv('APPDATA'), 'Wox')
        return self._appdir

    @property
    def app_settings(self):
        if not self._app_settings:
            with open(os.path.join(self.appdir, 'Settings', 'Settings.json'), 'r') as f:
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

