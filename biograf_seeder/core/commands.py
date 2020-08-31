import click
import os
import sys
import importlib
import importlib.util
import pkgutil
from pkgutil import ModuleInfo, ModuleType

cwd_path = os.getcwd()


def get_package_modules(package: ModuleInfo):
    raise Exception("Not implemented.")


def make_module_path(*args):
    parts_list = []

    for k in args:
        if type(k) == str:
            parts_list.append(k)

    return ".".join(parts_list)


def search_modules_by_name(modules_all: dict = sys.modules, prefix: str = None):
    modules = dict()

    for k in modules_all.keys():
        v = modules_all[k]
        if prefix is not None and prefix in k:
            modules[k] = v

    return modules


def get_packages(*args):
    name = ".".join(args)
    print("get_packages", name, len(args))

    if len(args) < 2:
        print_on_finish = True
    else:
        print_on_finish = False

    if importlib.util.find_spec(name) is None:
        raise Exception(f"Kan inte importera '{name}'.")

    for __module in pkgutil.iter_modules([name]):
        module_name = __module.name
        module_path = make_module_path(name, module_name)
        module = importlib.import_module(module_path)
        module_spec = importlib.util.find_spec(make_module_path(name, module_name))
        walked_packages = pkgutil.walk_packages(module_spec.submodule_search_locations)

        for wp in walked_packages:
            get_packages(name, module_name, wp.name)

        sys.modules[module_path] = module

        if __module.ispkg:
            get_packages(name, module_name)
        else:
            print(
                "module not pkg: ",
                importlib.import_module(make_module_path(name, module_name)),
            )

    if print_on_finish:
        # print("")
        print("Finally: ", search_modules_by_name(sys.modules, name))


def get_module_group_name(module: ModuleInfo, instance: ModuleType) -> str:
    if not hasattr(instance, "cli"):
        raise Exception(f"Need attribute 'cli' in {module.name}.")

    if not hasattr(getattr(instance, "cli"), "name"):
        raise Exception(f"Need attribute 'name' in {module.name}.cli.")

    return getattr(getattr(instance, "cli"), "name")


def get_pkg_commands(*args):
    pkg = ".".join(args)

    package = importlib.import_module(pkg)
    package_path = package.__spec__.submodule_search_locations[0] or None

    pkg_commands = {}

    for __module in pkgutil.iter_modules([package_path]):
        module_name = __module.name
        module = importlib.import_module(f"{pkg}.{module_name}")

        if not __module.ispkg:
            module_command_name = get_module_group_name(__module, module)
            pkg_commands[module_name] = getattr(module, "cli")
        else:
            cmd_group_commands = get_pkg_commands(pkg, __module.name)
            for k in cmd_group_commands.keys():
                sys.modules[k] = cmd_group_commands

            module_command_name = get_module_group_name(__module, module)
            pkg_commands[module_command_name.replace("_", "-")] = click.Group(
                context_settings={"help_option_names": ["-h", "--help"]},
                options_metavar="<options>",
                no_args_is_help=True,
                add_help_option=False,
                subcommand_metavar="command",
                help=module.__doc__,
                commands=cmd_group_commands,
            )

    return pkg_commands
