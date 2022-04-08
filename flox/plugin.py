from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
import traceback
import json
from tempfile import gettempdir
from functools import wraps
import logging

from .constants import PLUGIN_MANIFEST, DEFAULT_REPORT_TITLE, DEFAULT_REPORT_SUBTITLE
from .launcher import launcher, Launcher
from .item import Item, JsonRPCAction, Glyph


log = logging.getLogger(__name__)


def subkey(subkey):
    class cls_wrapper:
        def __init__(self, func):
            self.func = func
            self.subkey = subkey

        def __set_name__(self, owner, name):
            cls_subkey_methods = getattr(owner, 'subkey_methods', {})
            cls_subkey_methods[self.subkey] = self.func.__name__
            setattr(owner, 'subkey_methods', cls_subkey_methods)

            setattr(owner, name, self.func)
    return cls_wrapper

def query_wrapper(func):
    @wraps(func)
    def wrapper(self, query: str) -> None:
        if query and query[-1] in getattr(self, "subkey_methods", {}):
            log.debug("Subkey method found: %s", self.subkey_methods[query[-1]])
            results = getattr(self, self.subkey_methods[query[-1]])(query) or self._results
            return
        func(self, query)
    return wrapper

class Plugin(ABC):

    def __init_subclass__(cls, **kwargs) -> None:
        super.__init_subclass__(**kwargs)
        cls._results = []
        cls.default_report_title = DEFAULT_REPORT_TITLE
        cls.default_report_subtitle = DEFAULT_REPORT_SUBTITLE
        cls.query = query_wrapper(cls.query)

    def __call__(self, launcher:Launcher):
        self.launcher = launcher
        self.launcher(self)

    @abstractmethod
    def query(self, query: str) -> None:
        pass

    @abstractmethod
    def context_menu(self, params: dict) -> None:
        """
        Context menu.
        """
        pass

    def exception(self, e: Exception) -> None:
        """
        Exception handler.
        """
        self.exception_item(e)
        self.issue_item(e)

    @cached_property
    def root(self) -> Path:
        """
        The root directory of the plugin.
        """
        potential_paths = [
            Path.cwd().absolute(),
            Path(__file__).parent.absolute().parent,
        ]

        for path in potential_paths:

            while True:
                if Path(path, PLUGIN_MANIFEST).exists():
                    return path
                elif Path(path).is_mount():
                    return Path().cwd()

                path = Path(path).parent

    @cached_property
    def manifest(self) -> dict:
        """
        The plugin manifest.
        """
        with open(Path(self.root, PLUGIN_MANIFEST), 'r') as f:
            return json.load(f)

    @cached_property
    def name(self) -> str:
        """
        The plugin name.
        """
        return self.manifest['Name']

    @cached_property
    def id(self) -> str:
        """
        The plugin id.
        """
        return self.manifest['ID']

    @cached_property
    def version(self) -> str:
        """
        The plugin version.
        """
        return self.manifest['Version']

    @cached_property
    def description(self) -> str:
        """
        The plugin description.
        """
        return self.manifest['Description']

    @cached_property
    def author(self) -> str:
        """
        The plugin author.
        """
        return self.manifest['Author']

    @cached_property
    def action_keyword(self):
        """
        The plugin action keyword.
        """
        return self.manifest['ActionKeyword']

    @cached_property
    def language(self):
        """
        The plugin language.
        """
        return self.manifest['Language']

    @cached_property
    def icon(self):
        """
        The plugin icon path.
        """
        return self.manifest['IcoPath']

    @cached_property
    def website(self):
        """
        The plugin website.
        """
        return self.manifest['Website']

    def cache_dir(self):
        """
        The plugin cache directory.
        """
        return Path(gettempdir(), self.name)

    def add_item(self, item:Item):
        """
        Add an item to the results.
        """
        self._results.append(item)

    def exception_item(self, exception):
        self.add_result(
            title=f"Exception: {exception.__class__.__name__}",
            subtitle=str(exception),
            ico_path=self.icon,
            method=self.launcher.change_query,
            hide=True
        )

    def issue_item(self, e):
        trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)).replace('\n', '%0A')
        self.add_result(
            title=self.default_report_title,
            subtitle=self.default_report_subtitle,
            ico_path=self.icon,
            method='self.create_github_issue',
            parameters=[e.__class__.__name__, trace],
        )

    def add_result(self, title, subtitle=None, ico_path=None, score=0, auto_complete_text=None, method=None, parameters=None, hide=False, glyph=None, font_family=None):
        """
        Add a result to the results.
        """
        if ico_path is None:
            ico_path = self.icon
        if not Path(ico_path).is_absolute():
            ico_path = Path(self.root, ico_path)
        if str(font_family).startswith("#"):
            font_family = str(self.root.joinpath(font_family))

        _item = Item(
            Title=title, 
            Subtitle=subtitle, 
            IcoPath=ico_path, 
            Score=score, 
            AutoCompleteText=auto_complete_text,
            )
        if method:
            action = JsonRPCAction(method=method, parameters=parameters, hide=hide)
            _item.JsonRPCAction = action
        if glyph:
            glyph = Glyph(glyph, font_family)
            _item.Glyph = glyph
        self._results.append(_item)
        return _item