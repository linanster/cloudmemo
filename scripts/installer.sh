#! /usr/bin/env bash
#
set -u
set +e
# set -o noglob
#
workdir=$(cd "$(dirname $0)" && pwd)
topdir=$(cd "${workdir}" && cd .. && pwd)
scriptdir=${workdir}
cd "${workdir}"
#
# lib: color print
bold=$(tput bold)
green=$(tput setf 2)
red=$(tput setf 4)
reset=$(tput sgr0)

function green() {
	  printf "${bold}${green}%s${reset}\n" "$@";
  }
function red() {
	  printf "${bold}${red}%s${reset}\n" "$@";
  }

function get_release(){
    echo $(cat /etc/os-release | grep ^NAME= | egrep -io "centos|ubuntu" | tr A-Z a-z)
}

# green "hello"
# red "hello"

cat << eof
  __  __          _____           _        _ _           
 |  \/  |        |_   _|         | |      | | |          
 | \  / |_   _     | |  _ __  ___| |_ __ _| | | ___ _ __ 
 | |\/| | | | |    | | | '_ \/ __| __/ _' | | |/ _ \ '__|
 | |  | | |_| |   _| |_| | | \__ \ || (_| | | |  __/ |   
 |_|  |_|\__, |  |_____|_| |_|___/\__\__,_|_|_|\___|_|   
          __/ |                                                            
         |___/                                                             
eof

echo
echo


function install_main_service(){
  cd "${scriptdir}"
  if [ "$(get_release)" == "centos" ];then
    cp cloudmemo.service /usr/lib/systemd/system
  elif [ "$(get_release)" == "ubuntu" ];then
    cp cloudmemo.service /lib/systemd/system
  else
    echo "release error"
    exit 1
  fi
  systemctl daemon-reload
  systemctl enable cloudmemo.service
  systemctl restart cloudmemo.service
  systemctl status cloudmemo.service
  echo
}

function uninstall_main_service(){
  cd "${scriptdir}"
  systemctl stop cloudmemo.service
  systemctl disable cloudmemo.service
  if [ "$(get_release)" == "centos" ];then
    rm -f /usr/lib/systemd/system/cloudmemo.service
  elif [ "$(get_release)" == "ubuntu" ];then
    rm -f /lib/systemd/system/cloudmemo.service
  else
    echo "release error"
    exit 1
  fi
  systemctl daemon-reload
  echo
}



function option1(){
  install_main_service
  green "option1 done!"
}
function option2(){
  uninstall_main_service
  green "option2 done!"
}
function option3(){
  green "option3 done!"
}
function option4(){
  green "option4 done!"
}
function option5(){
  green "option5 done!"
}
function option6(){
  green "option6 done!"
}
function option7(){
  green "option7 done!"
}
function option8(){
  green "option8 done!"
}
function option9(){
  green "option9 done!"
}
function option10(){
  green "option10 done!"
}
function option11(){
  green "option11 done!"
}
function option12(){
  green "option12 done!"
}


cat << eof
====
1) install cloudmemo service
2) uninstall cloudmemo service
q) quit 
====
eof

while echo; read -p "Enter your option: " option; do
  case $option in
    1)
      option1
      break
      ;;
    2)
      option2
      break
      ;;
    q|Q)
      break
      ;;
    *)
      echo "invalid option, enter again..."
      continue
  esac
done

