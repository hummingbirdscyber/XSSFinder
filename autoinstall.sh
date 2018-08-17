#!/bin/bash
echo "Downloading dependencies..";
sudo apt-get install tor && sudo apt-get install python3-pip
pip3 install termcolor
pip3 install bs4	
pip3 install requests

