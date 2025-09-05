#!/bin/bash
mkdir ~/.local/bin/
chmod +x giusmap
mv giusmap ~/.local/bin/
sudo echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc