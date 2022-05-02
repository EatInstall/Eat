echo "──────────────────────────────────────────────
─██████████████─██████████████─██████████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─
─██░░██████████─██░░██████░░██─██████░░██████─
─██░░██─────────██░░██──██░░██─────██░░██─────
─██░░██████████─██░░██████░░██─────██░░██─────
─██░░░░░░░░░░██─██░░░░░░░░░░██─────██░░██─────
─██░░██████████─██░░██████░░██─────██░░██─────
─██░░██─────────██░░██──██░░██─────██░░██─────
─██░░██████████─██░░██──██░░██─────██░░██─────
─██░░░░░░░░░░██─██░░██──██░░██─────██░░██─────
─██████████████─██████──██████─────██████─────
──────────────────────────────────────────────"
echo "         Eat Installer 1.0"
echo ">>> Please enter your password if you are prompted."
command sudo echo -n "" || echo "Failed to authenticate. Ensure you are in the sudoers file. See message above."  && exit 1
if [ -d "$(eval ~)/Eat-PKG-Manager" ]; then
   echo "You already have eat installed. Did you mean to run 'eathelp' instead?"
   exit 1
fi
echo "Installing dependencies..."
command sudo apt-get install python3 python-is-python3 python3-requests python3-colorama python3-pip python3-yaml git -y >> /dev/null # apt does not have a stable CLI interface. Use with caution in scripts.
echo "Downloading eat..."
command git clone https://github.com/Eatinstall/Eat.git ~/Eat-PKG-Manager >> /dev/null
echo "Creating commands..."
echo "" >> ~/.bashrc
echo "# Add eat package manager commands." >> ~/.bashrc
echo "alias eat='python ~/Eat-PKG-Manager/eat.py'" >> ~/.bashrc
echo "alias eatinst='python ~/Eat-PKG-Manager/eat-install.py'" >> ~/.bashrc
echo "alias eathelp='python ~/Eat-PKG-Manager/man-eat.py'" >> ~/.bashrc
echo "Eat was installed. Please restart your shell to apply the changes."
echo "Then, run eathelp for information and usage."
