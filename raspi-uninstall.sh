echo "Stopping mpwrap..."
sudo service mpwrap stop

echo "Deleting mpwrap service..."
sudo update-rc.d -f mpwrap remove
sudo rm /etc/init.d/mpwrap

echo "Uninstalling mpwrap..."
sudo rm -R /etc/mpwrap

echo "Done!"