import click
import os
import importlib
import pkgutil


def get_module_group_name(
    module: pkgutil.ModuleInfo, instance: pkgutil.ModuleType
) -> str:
    if not hasattr(instance, "cli"):
        raise Exception(f"Need attribute 'cli' in {module.name}.")

    if not hasattr(instance.cli, "name"):
        raise Exception(f"Need attribute 'name' in {module.name}.cli.")

    return instance.cli.name


def get_pkg_commands(pkg):
    pkg_instance = importlib.import_module(pkg)
    pkg_path = os.path.dirname(pkg_instance.__file__)

    pkg_commands = {}

    for module in pkgutil.iter_modules([pkg_path]):
        module_name = module.name
        module_instance = importlib.import_module(f"{pkg}.{module_name}")
        print(module_instance)

        if not module.ispkg:
            module_command_name = get_module_group_name(module, module_instance)
            cli_name = module_instance.cli.name
            pkg_commands[cli_name] = module_instance.cli
        else:
            module_command_name = get_module_group_name(module, module_instance)
            pkg_commands[module_command_name.replace("_", "-")] = click.Group(
                context_settings={"help_option_names": ["-h", "--help"]},
                options_metavar="<options>",
                no_args_is_help=True,
                add_help_option=False,
                subcommand_metavar="command",
                help=module_instance.__doc__,
                commands=get_pkg_commands(f"{pkg}.{module.name}"),
            )

    return pkg_commands
