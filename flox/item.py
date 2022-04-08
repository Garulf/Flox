from lib2to3.pytree import convert
from typing import Union, List
from pathlib import Path
from dataclasses import dataclass, field, asdict
import json

from .constants import DEFAULT_GLYPH_FONTFAMILY


@dataclass
class Item:
    """
    Represents a Result item
    """
    Title: str
    Subtitle: str = None
    IcoPath: str = None
    Glyph: Glyph = None
    Score: int = 0
    JsonRPCAction: JsonRPCAction = None
    AutoCompleteText: str = None


    def __post_init__(self):
        if not isinstance(self.Title, (str)):
            self.Title = str(self.Title)
        if not isinstance(self.IcoPath, (str)):
            self.IcoPath = str(self.IcoPath)

    def __str__(self):
        return json.dumps(asdict(self), default=lambda o: o.__dict__)

    def __repr__(self) -> str:
        return self.__str__()

@dataclass
class JsonRPCAction:
    """
    Determines what method to call when result is selected
    """
    method: Union[str, callable]
    parameters: List[str] = field(default_factory=list)
    dontHideAfterAction: bool = False

    def __post_init__(self):
        if callable(self.method):
            self.method = self.method.__name__

@dataclass
class Glyph:
    Glyph: str
    FontFamily: str = field(default=DEFAULT_GLYPH_FONTFAMILY)