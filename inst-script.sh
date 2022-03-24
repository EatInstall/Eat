echo "Installing dependencies (may request user password due to sudo)..."
sudo apt-get install python3 python-is-python3 python3-requests python3-colorama python3-pip git -y # apt does not have a stable CLI interface. Use with caution in scripts.
echo "Downloading eat..."
git clone https://github.com/Tyler887/eat.git Eat-PKG-Manager
echo "Symlinking a binary to python script..."
sudo echo "#!/usr/bin/bash\npython3 ~/Eat-PKG-Manager/eat.py" >> /usr/bin/eat
echo "Please restart your shell to apply the changes!"
