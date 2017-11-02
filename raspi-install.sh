echo "Installing mpwrap..."
sudo cp -a mpwrap/. /etc/mpwrap
sudo chmod 755 /etc/mpwrap/mpwrap.py

echo "Installing pip3..."
sudo apt update
sudo apt install python3-pip

echo "Installing requirements..."
sudo pip3 install -r requirements.txt

echo "Configuring mpwrap as a service..."
sudo cp mpwrap.service /etc/init.d/mpwrap
sudo chmod 755 /etc/init.d/mpwrap
sudo update-rc.d mpwrap defaults

echo "Starting mpwrap..."
sudo service mpwrap start

echo "Done!"