#!/usr/bin/env bash
#
# set -o errexit

# 1.variables definition

usage=$"
Usage: run.sh --start [--nodaemon]
              --stop
              --status
              --init
"
workdir=$(cd "$(dirname $0)" && pwd)

# 2.functions definition

function activate_venv() {
    if [ -d venv ]; then
        source ./venv/bin/activate || source ./venv/Script/activate
    else
        echo "==venv error=="
        exit 1
    fi
}


function run_init(){
    pip3 install virtualenv
    virtualenv venv
    source ./venv/bin/activate
    # pip3 install -r requirements.txt
    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    if [ $? -eq 0 ]; then
        echo "==init config complete=="
        exit 0
    else
        echo "==init config fail=="
        exit 1
    fi
}

function get_pid(){
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_cloudmemo" | awk '{if($3==1) print $2}')
    echo "$pid"
}



function run_start(){
    activate_venv
    case "$1" in
        "")
            cmd="gunicorn --daemon --workers 1 --bind 0.0.0.0:5200 --timeout 300 --worker-class eventlet wsgi:application_cloudmemo"
            ;;
        "--nodaemon")
            cmd="gunicorn --workers 2 --bind 0.0.0.0:5200 --timeout 300 --worker-class eventlet wsgi:application_cloudmemo"
            ;;
        *)
            echo "${usage}"
            exit 1
    esac
    echo "${cmd}"
    eval "${cmd}"
    # pid="$(get_pid)"
    echo "$(get_pid)"
    exit 0
}

function run_status(){
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_cloudmemo" | grep 5200 | awk '{if($3==1) print $2}')
    echo "pid: $pid"
    exit 0
}

function run_stop(){
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_cloudmemo" | grep 5200 | awk '{if($3==1) print $2}')
    echo "$pid"
    if [ "$pid" == "" ]; then
        echo "not running"
    else
        echo "kill $pid"
        kill "$pid"
    fi
    exit 0
}


# 3.start code

cd "$workdir"

if [ $# -eq 0 ]; then
    echo "${usage}"
    exit 1
fi

if [ $# -ge 1 ]; then
  case $1 in
    --help|-h)
        echo "$usage"
        exit 0
        ;;
    --init)
        run_init
        ;;
    --start)
        run_start $2
        ;;
    --status)
        run_status
        ;;
    --stop)
        run_stop
        ;;
    *)
        echo "$usage"
        exit 1
        ;;
  esac
fi

