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
