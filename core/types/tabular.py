from typing import Any, Text


class TabularHeader(object):
    def __init__(self, *args):
        for i, k in enumerate(args):
            setattr(self, k, i)

    def has(self: Any, key: Text):
        return hasattr(self, key)

    def to_list(self):
        return self.__dict__.keys()

    # def __repr__(self):
    #     dict_keys = self.keys
    #     class_attr = []
    #     for k in dict_keys:
    #         class_attr.append(k)

    #     class_attr_str = ", ".join(class_attr)

    #     return f"{self.__class__.__name__} [{class_attr_str}]"

    def __repr__(self):
        dict_keys = self.__dict__.keys()
        class_attr = []
        for k in dict_keys:
            v = getattr(self, k, None)
            if type(v) == int:
                class_attr.append(f"{k} = {v}")

            if type(v) == str:
                class_attr.append(f'{k} = "{v}"')

            if v is None:
                class_attr.append(f"{k} = None")

        class_attr_str = ", ".join(class_attr)

        return f"{self.__class__.__name__} [{class_attr_str}]"
