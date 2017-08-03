import collections.abc
import collections

import itertools
import abc
import typing
import warnings


class ScriptArgument:
    def __init__(self, value, help=None):
        self.value = value
        self._validation = lambda v: True
        self.help = help

    def __str__(self):
        return self.value

    def set_validator(self, callback):
        self._validation = callback

    @property
    def valid(self):
        return self._validation(self.value)

    def check_value(self, value) -> bool:
        return self._validation(value)


class AbsArgumentBuilder(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._args = dict()

    @abc.abstractmethod
    def add_argument(self, name: str, default="", *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def build(self) -> typing.Dict[str, ScriptArgument]:
        pass


class ArgumentBuilder(AbsArgumentBuilder):

    @staticmethod
    def default_validator(data: str)->bool:
        return True

    def add_argument(self, name: str, default="", *args, **kwargs) -> None:
        if name in self._args:
            raise KeyError("{} already being used.")

        new_arg = ScriptArgument(default)

        if "validate" in kwargs:
            new_arg.set_validator(kwargs["validate"])
        else:
            new_arg.set_validator(self.default_validator)

        if "help" in kwargs:
            new_arg.help = kwargs['help']

        self._args[name] = new_arg

    def build(self) -> typing.Dict[str, ScriptArgument]:
        return self._args


class Arguments(collections.abc.Mapping):
    def __init__(self, *args, **kwargs):
        warnings.warn("Use ScriptArgument() instead", DeprecationWarning)
        self._required = dict()
        self._optional = dict()

    def __len__(self):
        return len(self._required) + len(self._optional)

    def __iter__(self):
        return itertools.chain(self._required.__iter__(), self._optional.__iter__())

    def add_required(self, name, default="", *args, **kwargs):
        new_arg = ScriptArgument(default)

        if "validate" in kwargs:
            validator = lambda foo: foo != "" and kwargs["validate"](foo)
        else:
            validator = lambda foo: foo != ""

        if "help" in kwargs:
            new_arg.help = kwargs['help']
        if name in self._required or name in self._optional:
            raise KeyError("{} already being used.")

        new_arg.set_validator(validator)
        self._required[name] = new_arg

    def add_optional(self, name, default="", *args, **kwargs):
        if "validate" in kwargs:
            validator = lambda foo: kwargs["validate"](foo)
        else:
            validator = lambda foo: True
        if name in self._required or name in self._optional:
            raise KeyError("{} already being used.")
        new_arg = ScriptArgument(default)
        new_arg.set_validator(validator)
        self._optional[name] = new_arg

    def __getitem__(self, key):
        if key in self._required:
            return self._required[key]
        if key in self._optional:
            return self._optional[key]
        raise KeyError

    def __setitem__(self, key, item):
        if key in self._required:
            self._required[key] = item
        if key in self._optional:
            self._optional[key] = item
        else:
            raise KeyError

    @property
    def missing(self):
        missing = []
        for k, v in self._required.items():
            if not v.valid:
                missing.append(k)
        return missing

    @property
    def valid(self) -> bool:

        # Check all required fields are filled in
        for k, v in self._required.items():
            if not v.valid:
                return False
        else:
            return True
