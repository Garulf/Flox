# FLOX

## About

Python library to help build Flow Launcher and Wox plugins

## Usage

```
from flox import Flox
# import after flox to automatically import from lib directory in plugin path
import requests

# have your class inherit from Flox
class Test(Flox):

    # add underscore to have Flox run on query
    def _query(self, query):
        for _ in range(250):
            self.add_item(
                title=self.args,
                subtitle=str(_)
            )

    # _context will run when the context menu is activated
    def _context_menu(self, data):
        for _ in range(250):
            self.add_item(
                title=self.args,
                subtitle=str(Flox.__bases__[0].__name__)
            )

if __name__ == "__main__":
    Test()
```

Flox should be installed in the plugins root directory like so:

```
Plugin/
    plugin.json
    yourplugin.py
    flox/
        __init__.py
        flox.py
```
## External libraries

In order to make installation for the user easy, Flox will add `lib/` from your plugins root directory to the system path.
Install all external packages to this directory. 

This can be done easily with `pip install --target=./lib <package>`

### Example

```
Plugin/
    plugin.json
    icon.png
    flox/
        __init__.py
        flox.py
    lib/
        packageA/
            ...
        packageB/
            ...
    yourplugin.py
    ...
 ```
 
## Flow Launcher Setup

Flow Launcher requires an external package to handle json-rpc. Flox will attempt to import the flowlahncher package from the plugin's `lib/` directory (described above).
Including this with your package is recommended to avoid the user from having to install external packages to run.

