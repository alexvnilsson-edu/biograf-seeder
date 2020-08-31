#!/usr/bin/env bash
set -euo pipefail

SCRIPT=$(basename "$0")
VERSION="0.1.0"

function version
{
    local txt=(
        "$SCRIPT version $VERSION"
    )

    printf "%s\n" "${txt[@]}"
}

function usage
{
    local txt=(
        "Utility $SCRIPT for doing stuff."
        "Usage: $SCRIPT [options] <command> [arguments]"
        ""
        "Commands:"
        "  build                setup.py build."
        "  install              setup.py install."
        "  sdist [anything]     setup.py sdist [bdist_wheel]."
        ""
        "Options:"
        "  --help, -h     Print help."
        "  --version, -v  Print version."
    )

    printf "%s\n" "${txt[@]}"
}

function badUsage
{
    local message="$1"
    local txt=(
        "For an overview of the command, execute:"
        "$SCRIPT --help"
    )

    [[ $message ]] && printf "$message\n"

    printf "%s\n" "${txt[@]}"
}

function makeBadUsage() {
    default_message="Ogilltigt alternativ angivet."
    
    arg_message=${1:-$default_message}
    arg_exit = ${2:--1}

    badUsage "${arg_message}"

    [[ $arg_exit -ne -1 ]] && exit 1
}

# Lokala variabler.
python=python3
setuptools=setup.py
venv_path=.venv


# Lokala flaggor.
dry_run=0
verbose=1 # På by default just nu
venv_active=check_venv
venv_attempted_activation=0

# Lokala funktioner.
function check_venv() {
    venv_active=$($python -c 'import os,sys; print(1 if os.getenv("VIRTUAL_ENV") is not None else 0)')
}

# Interna funktioner.
function try_venv_activate() {
    if [[ -d "${venv_path}" ]]; then
        source $venv_path/bin/activate
    else
        debucho "Hittade ingen virtualenv."
    fi
}

function check_venv_active() {
    arg_retry=${1:-"retry-once"}

    if [[ $venv_active = 0 ]]; then
        debucho "Försöker aktivera..."
        if [ "$arg_retry" != "no-retry" ]; then
            (try_venv_activate && echo "OK" && check_venv && check_venv_active "no-retry") || echo "Failed"
        else
            debucho "Skippar återförsök pågrund av möjlig oändlig loop."
        fi
        
    fi
}

function clean_build() {
    rm -rf build dist || echo "" > /dev/null
}

function run_pip() {
    $python -m pip $*
}

function setup_build() {
    exec_args="${@:1}"
    $python $setuptools build $exec_args
}

function setup_sdist() {
    exec_args="${@:1}"
    $python $setuptools sdist bdist_wheel $exec_args
}

function setup_install() {
    exec_args="${@:1}"
    $python $setuptools install $exec_args
}

function app-install() {
    clean_build
    check_venv_active
    try_venv_activate
    run_pip "install" "--requirement requirements.txt"

    [[ $verbose = 1 ]] && (setup_build "--verbose" && setup_install "--verbose") || (setup_build && setup_build)
}

function app-sdist() {
    clean_build
    check_venv_active
    try_venv_activate
    run_pip install "--requirement requirements.txt"
    [[ $verbose = 1 ]] && (setup_sdist "--verbose") || (setup_sdist)
}

function app-bumpversion() {
    exec_args="${@:1}"

    bumpversion --list $exec_args --allow-dirty
}

function app-help() {
    usage
    exit 0
}

source ./build_tools/cli.sh

# Läs in alternativ.
while (( $# ))
do
    case "$1" in
        # install | sdist | bumpversion)
        #     cli_set_command "$1" badUsage
        #     shift
        # ;;
        install | sdist | bumpversion)
            cli_set_command "$1" makeBadUsage
            shift
        ;;
        --dry-run)
            dry_run=1
            shift
        ;;
        --verbose | -V)
            verbose=1
            shift
        ;;
        --help | -h)
            usage
            exit 0
        ;;
        --version | -v)
            version
            exit 0
        ;;
        *)
            badUsage "Ogilltigt alternativ angivet."
            exit 1
        ;;
    esac
done

if [[ ! -z "$arg_command" ]]; then
    if [ "$(type -t ${command_func})" = 'function' ]; then
        $command_func "${@:1}"
    else
        echo "Hittade inte funktionen ${command_func}."
    fi
else
    badUsage
fi


# rm -rf build dist || echo "" > /dev/null
# pip install -r requirements.txt

# if [[ $verbose = 1 ]]; then
#     setup_build "--verbose"
# else
#     setup_build
# fi

# if [[ $install = 1 ]]; then
#     if [[ $verbose = 1 ]]; then
#         setup_install "--verbose"
#     else
#         setup_install
#     fi
# fi