echo "Installing dependencies (may request user password due to sudo)..."
sudo apt-get install python3 python-is-python3 python3-requests python3-colorama python3-pip git -y # apt does not have a stable CLI interface. Use with caution in scripts.
echo "Downloading eat..."
git clone https://github.com/Tyler887/eat.git ~/Eat-PKG-Manager
echo "Symlinking eat command to the python script..."
echo "#!/usr/bin/bash\npython3 ~/Eat-PKG-Manager\eat.py" >> ~/EatPKGSymlink/eat
echo "Forcing BASH to add Eat to the path..."
echo "\n\n# Add eat package manager to the path.\nexport PATH=$PATH:~/EatPKGSymlink" >> ~/.bashrc
echo "Eat was installed. Please restart your shell to apply the changes."
