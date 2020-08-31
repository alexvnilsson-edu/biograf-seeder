from typing import Any
import subprocess


class NamedParam(object):
    expecting_kwargs = ["type", "required", "default"]

    def __init__(self, **kwargs):
        for k in kwargs:
            if k in self.expecting_kwargs:
                setattr(self, k, kwargs[k])

    def __repr__(self):
        dict_keys = self.__dict__.keys()
        class_attr = []
        for k in dict_keys:
            v = getattr(self, k, None)
            if v is not None:
                class_attr.append(f"{k} = {v}")

        class_attr_str = ", ".join(class_attr)

        return f"{self.__class__.__name__} [{class_attr_str}]"


def has_kwarg_and_type(expecting: dict, key: str, value: Any) -> bool:
    if expecting.get(key, None) is None:
        raise Exception(f"{key} finns inte i registret.")

    if not hasattr(expecting[key], "type"):
        raise Exception(f"{key}-objektet har inte förväntat attribut 'type'.")

    if not isinstance(value, getattr(expecting.get(key), "type")):
        raise TypeError(
            f"Parametern {key}: {str(type(key).__name__)} möter inte kravet i mottagande objektet."
        )

    return True


class Process(object):
    expecting_kwargs = {
        "shell": NamedParam(type=bool, default=False),
        "check": NamedParam(type=bool, default=False),
    }

    def add_argument(self, *args):
        for __arg in args:
            self.cmd.append(__arg)

    def run(self):
        subprocess.run(
            self.cmd, shell=self.get_option("shell"), check=self.get_option("check")
        )

    def get_option(self, key: str, default_value: Any = None):
        if hasattr(self.expecting_kwargs[key], "default"):
            default_value = getattr(self.expecting_kwargs[key], "default")

        return getattr(self, key, default_value)

    def __init__(self, *args, **kwargs):
        self.cmd = []

        for k in args:
            self.cmd.append(k)

        for k in kwargs:
            if k in self.expecting_kwargs and has_kwarg_and_type(
                self.expecting_kwargs, k, kwargs[k]
            ):
                setattr(self, k, kwargs[k])
            else:
                print(f"{self.__class__.__name__} tar inte emot attributet '{k}'.")

    def __repr__(self):
        dict_keys = self.__dict__.keys()
        class_attr = []
        for k in dict_keys:
            v = getattr(self, k, None)
            if v is not None:
                class_attr.append(f"{k} = {v}")

        class_attr_str = ", ".join(class_attr)

        return f"{self.__class__.__name__} [{class_attr_str}]"
