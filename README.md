# FLOX

Python library to help build Flow Launcher and Wox plugins

Flox adds many useful methods to speed up plugin devolpment

Heavily inspired from the great work done by deanishe at: [deanishe/alfred-workflow](https://github.com/deanishe/alfred-workflow)

## Installation


### PIP install from pypi

```
pip install flox-lib
```

### PIP install from github

```
pip install git+https://github.com/garulf/flox.git
```

## Basic Usage

```
from flox import Flox

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
