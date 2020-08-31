# Nyttiga variabler.
python=python3
setuptools=setup.py

# Standardvärden.
default_venv_path=.venv

# Interna flaggor.
venv_active=null

function check_venv() {
    venv_active=$($python -c 'import os,sys; print(1 if os.getenv("VIRTUAL_ENV") is not None else 0)')
}

# Kärn-funktioner.
function try_venv_activate() {
    venv_path=${1:-$default_venv_path}
    if [[ -d "${venv_path}" ]]; then
        source $venv_path/bin/activate
    else
        echo "Hittade ingen virtualenv."
    fi
}

function check_venv_active() {
    arg_retry=${1:-"retry-once"}

    if [[ $venv_active != 1 ]]; then
        if [ "$arg_retry" != "no-retry" ]; then
            (try_venv_activate && echo "OK" && check_venv && check_venv_active "no-retry") || (echo "Fel" && exit 1)
        else
            echo "Skippar återförsök pågrund av möjlig oändlig loop."
            exit 1
        fi
        exit 0
    fi
}

function run_python_script() {
    [[ $venv_active != 1 ]] && (echo "python3 without venv" && $python -m $*) || (echo "python with venv" && python -m $*)
}