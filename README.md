# FLOX

Python library to help build Flow Launcher and Wox plugins

Flox adds many useful methods to speed up plugin devolpment

Heavily inspired from the great work done by deanishe at: https://github.com/deanishe/alfred-workflow 

## Installation

### PIP install from github

`pip install git+https://github.com/garulf/flox.git`

Flox should be installed in the plugins root directory like so:

```
Plugin/
    plugin.json
    yourplugin.py
    flox/
        __init__.py
        flox.py
```

## Usage

```
from flox import Flox
# import after flox to automatically import from lib directory in plugin path
import requests

# have your class inherit from Flox
class YourClass(Flox):

    def query(self, query):
        for _ in range(250):
            self.add_item(
                title=self.args,
                subtitle=str(_)
            )

    def context_menu(self, data):
        self.add_item(
            title=data,
            subtitle=data
        )

if __name__ == "__main__":
    YourClass()
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

