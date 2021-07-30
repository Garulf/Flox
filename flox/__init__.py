import sys
import os

from .flox import Flox

PLUGIN_MANIFEST = 'plugin.json'

potential_paths = [
    os.path.abspath(os.getcwd()),
    os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
]

for path in potential_paths:

    while True:
        if os.path.exists(os.path.join(path, PLUGIN_MANIFEST)):
            plugindir = path
            break
        elif path == '/':
            break

        path = os.path.dirname(path)

    if plugindir:
        break

lib_path = os.path.join(plugindir, 'lib')
if os.path.exists(lib_path):
    sys.path.append(lib_path)