# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path
from time import time
from typing import Union, List, TYPE_CHECKING
from dataclasses import asdict
import logging
if TYPE_CHECKING:
    from .plugin import Plugin

from .constants import FLOW_LAUNCHER_API_PREFIX, FLOW_LAUNCHER_DIR_NAME, WOX_DIR_NAME, WOX_API_PREFIX, INVIS_CHAR, SPACE_CHAR


log = logging.getLogger(__name__)

"""
Slightly modified wox.py credit: https://github.com/Wox-launcher/Wox
"""

def launcher():
    launchers = {
        "wox": Wox,
        "FlowLauncher": FlowLauncher,
    }
    cwd = Path().cwd()
    launcher_dir = None
    if str(FLOW_LAUNCHER_DIR_NAME) in cwd.parts:
        launcher_dir = FLOW_LAUNCHER_DIR_NAME
    elif str(WOX_DIR_NAME) in cwd.parts:
        launcher_dir = WOX_DIR_NAME

    appdata = Path(os.getenv('APPDATA'))
    local_appdata = Path(os.getenv('LOCALAPPDATA'))


    if str(appdata.joinpath(launcher_dir)) in str(cwd):
        user_dir = appdata.joinpath(launcher_dir)
        app_dir = local_appdata.joinpath(launcher_dir)
    elif "UserData" in cwd.parts:
        user_dir = cwd.parts[:-2]
        app_dir = cwd.parts[:-3]
    elif appdata.joinpath(FLOW_LAUNCHER_DIR_NAME).exits():
        user_dir = appdata.joinpath(FLOW_LAUNCHER_DIR_NAME)
        app_dir = local_appdata.joinpath(FLOW_LAUNCHER_DIR_NAME)
    elif appdata.joinpath(WOX_DIR_NAME).exits():
        user_dir = appdata.joinpath(WOX_DIR_NAME)
        app_dir = local_appdata.joinpath(WOX_DIR_NAME)
    else:
        raise FileNotFoundError("Unable to locate Launcher directory")
    if FLOW_LAUNCHER_DIR_NAME in app_dir.parts:
        return FlowLauncher(user_dir, app_dir)
    elif WOX_DIR_NAME in app_dir.parts:
        return Wox(user_dir, app_dir)


class Launcher(object):
    """
    Launcher python plugin base
    """
    def __init__(self, user_dir, app_dir):
        self.user_dir = user_dir
        self.app_dir = app_dir
        self._debug = False

    def __call__(self, plugin:'Plugin', debug=None):
        self.run(plugin, debug)


class Wox(Launcher):
    """
    Wox python plugin base
    """
    def __init__(self, user_dir, app_dir):
        super().__init__(user_dir, app_dir)
        self.api = WOX_API_PREFIX

    def run(self, plugin:'Plugin', debug=None):
        self.plugin = plugin
        rpc_request = {}
        if len(sys.argv) > 1:
            rpc_request = json.loads(sys.argv[1])
        request_method_name = rpc_request.get('method', 'query')
        request_method_parameters = rpc_request.get('parameters', [''])
        request_method = getattr(self.plugin, request_method_name, None)
        if not request_method:
            request_method = getattr(self, request_method_name)
        try:
            results = request_method(*request_method_parameters) or self.plugin._results
        except Exception as e:
            log.exception(e)
            results = self.plugin.exception(e) or self.plugin._results
        if debug:
            self._debug = debug
        if request_method_name == 'query':
            results = {"result": self.plugin._results}

            print(json.dumps(results, default=lambda i: asdict(i)))

    def api_call(self, method:str, parameters:List[str]):
        method = f"{self.api}.{method}"
        output = {"method": method, "parameters": parameters}
        print(json.dumps(output))

    def debug(self,msg):
        """
        alert msg
        """
        print("DEBUG:{}".format(msg))
        sys.exit()

    def change_query(self, query, requery=False):
        """
        change query
        """
        self.api_call("ChangeQuery", [query, requery])

    def shell_run(self, cmd):
        """
        run shell commands
        """
        print(json.dumps({"method": f"{self.api}.ShellRun","parameters":[cmd]}))

    def close_app(self):
        """
        close launcher
        """
        print(json.dumps({"method": f"{self.api}.CloseApp","parameters":[]}))

    def hide_app(self):
        """
        hide launcher
        """
        print(json.dumps({"method": f"{self.api}.HideApp","parameters":[]}))

    def show_app(self):
        """
        show launcher
        """
        print(json.dumps({"method": f"{self.api}.ShowApp","parameters":[]}))

    def show_msg(self, title, sub_title, ico_path=""):
        """
        show messagebox
        """
        print(json.dumps({"method": f"{self.api}.ShowMsg","parameters":[title,sub_title,ico_path]}))

    def open_setting_dialog(self):
        """
        open setting dialog
        """
        print(json.dumps({"method": f"{self.api}.OpenSettingDialog","parameters":[]}))

    def start_loadingbar(self):
        """
        start loading animation in wox
        """
        print(json.dumps({"method": f"{self.api}.StartLoadingBar","parameters":[]}))

    def stop_loadingbar(self):
        """
        stop loading animation in wox
        """
        print(json.dumps({"method": f"{self.api}.StopLoadingBar","parameters":[]}))

    def reload_plugins(self):
        """
        reload all launcher plugins
        """
        print(json.dumps({"method": f"{self.api}.ReloadPlugins","parameters":[]}))

class FlowLauncher(Wox):
    """
    FlowLauncher python plugin base
    """
    def __init__(self, user_dir, app_dir):
        super().__init__(user_dir, app_dir)
        self.api = FLOW_LAUNCHER_API_PREFIX

