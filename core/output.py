from typing import List
import click as click
from tabulate import tabulate as tabulate


class Table(object):
    def __init__(self):
        self.__header = []
        self.__items = []
        self.__rows = []

    @property
    def header(self):
        return self.__header

    def set_header(self, *args):
        for k in args:
            self.__header.append(k)

    def append(self, obj: dict):
        self.__items.append(obj)
        row = []
        for k in obj.keys():
            if k in self.__header:
                row.append(obj[k])
        self.__rows.append(row)

    @property
    def __all_rows(self, header: bool = True):
        table = []

        if self.__header and header:
            table.append(self.__header)

        for r in self.__rows:
            table.append(r)

    def __get_column_values(self, column: str):
        c_values = []

        for item in self.__items:
            if item[column]:
                c_values.append(item[column])

        return c_values

    @property
    def __get_rows(self):
        rows = dict()
        columns = self.__header
        for c in columns:
            v = self.__get_column_values(c)
            rows[c] = v

        return rows

    @property
    def rows(self):
        return self.__get_rows

    def print(self):
        rows = dict()
        old_rows = self.rows

        for k in old_rows.keys():
            if len(old_rows[k]) > 0:
                rows[k] = old_rows[k]

        click.echo(tabulate(rows, headers="keys", numalign="left"))

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

        return f"{self.header}\n{self.__class__.__name__} [{class_attr_str}]"
