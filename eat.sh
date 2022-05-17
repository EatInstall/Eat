if [[ "$0" -eq "help" ]]; then
  echo "Usage: eat (install|globalinstall|manual|help) [arguments]"
elif [[ "$0" -eq "install" ]]; then
  if [[ "$1" -eq "" ]]; then
    echo "Error: missing package operand."
    exit 1
  fi
  if [[ "$2" -ne "" ]]; then
    echo "Error: Too many arguments to install (install takes excactly one argument)."
    exit 1
  fi
  python3 ~/Eat-PKG-Manager/eat-install.py $1
else
  echo "Error: $0 is not a valid command. Run `eat help'."
  exit 127
fi
