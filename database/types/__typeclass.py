class TypeClass(object):
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

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
