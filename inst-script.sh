# license: GPLv3+: GPL version 3 or later
sudo echo -n ""
echo "Installing dependencies..."
sudo apt-get install python3 python-is-python3 python3-requests python3-colorama python3-pip python3-yaml git -y >> /dev/null # apt does not have a stable CLI interface. Use with caution in scripts.
echo "Downloading eat..."
git clone https://github.com/Tyler887/eat.git ~/Eat-PKG-Manager >> /dev/null
echo "Creating commands..."
echo "" >> ~/.bashrc
echo "# Add eat package manager commands." >> ~/.bashrc
echo "alias eat='python ~/Eat-PKG-Manager/eat.py'" >> ~/.bashrc
echo "alias eatinst='python ~/Eat-PKG-Manager/eat-install.py'" >> ~/.bashrc
echo "alias eathelp='python ~/Eat-PKG-Manager/man-eat.py'" >> ~/.bashrc
echo "Eat was installed. Please restart your shell to apply the changes."
echo "Then, run eatman for information and usage."
