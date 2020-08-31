DEBUG=1

# Nyttiga variabler.
python=python3
setuptools=setup.py

# Logiska variabler.
arg_command=null
command_func=null

# Standardvärden.
default_venv_path=.venv

# Interna flaggor.
venv_active=null

#
# Skriv ut ett meddelande endast under debugging (inklusive call stack).
#
function debucho() {
    _caller=$(caller 1)
    [[ $DEBUG = 1 ]] && echo "[${_caller}] $*"
}

function cli_make_error() {
    _arg_badUsage=${1:-}

    if [[ ! -z "${_arg_badUsage}" ]]; then
        $_arg_badUsage
    fi
}

function cli_set_command() {
    _arg_command=$1
    badUsage=${2:-}
    debucho "setting command = ${_arg_command}"

    if [[ -z "${_arg_command}" ]]; then
        badUsage
        exit 1
    fi

    arg_command=$_arg_command
    command_func=app-$arg_command
}

function check_venv() {
    venv_active=$($python -c 'import os,sys; print(1 if os.getenv("VIRTUAL_ENV") is not None else 0)')
}

# Kärn-funktioner.
function try_venv_activate() {
    venv_path=${1:-$default_venv_path}
    if [[ -d "${venv_path}" ]]; then
        source $venv_path/bin/activate
    else
        debucho "Hittade ingen virtualenv."
    fi
}

CHECK_NO_RETRY=0
CHECK_RETRY_ONCE=1


function check_venv_active() {
    default_retry="${CHECK_VENV_OPTIONS[CHECK_NO_RETRY]}"
    arg_retry=${1:-$CHECK_RETRY_ONCE}

    if [[ $venv_active != 1 ]]; then
        if [[ $arg_retry -eq $CHECK_NO_RETRY ]]; then
            (try_venv_activate && debucho "OK" && check_venv && check_venv_active $CHECK_NO_RETRY) || (debucho "Fel" && exit 1)
        else
            debucho "Skippar återförsök pågrund av möjlig oändlig loop."
            exit 1
        fi
        exit 0
    fi
}

function run_python_script() {
    [[ $venv_active != 1 ]] && (debucho "python3 without venv" && $python -m $*) || (debucho "python with venv" && python -m $*)
}