#!/bin/bash
user=pi
mysql_user=root
password=asd
database=sensors
sensors=(dht11_temperature dht11_humidity sound light temperature)
proj_dir=/home/$user/room-sensors
arduino_serial=/dev/ttyACM0
ip=192.168.0.12

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Setting up project directory..."
if [ ! -d "$proj_dir" ]; then
  mkdir $proj_dir
else 
  rm -r $proj_dir
fi

echo "Cloning git repo.."
git clone https://github.com/sdelcore/room-sensors.git $proj_dir
cd $proj_dir
chmod +x room_sensors.py
chmod +x websocket_server.py
echo "done."

echo "Setting up Arduino with PlatformIO"
cd sensors
wget https://raw.githubusercontent.com/platformio/platformio-core/develop/scripts/99-platformio-udev.rules
cp 99-platformio-udev.rules /etc/udev/rules.d/99-platformio-udev.rules
rm 99-platformio-udev.rules
service udev restart
platformio run -t upload
cd ..
sed -i "s|.*arduino_serial=.*|arduino_serial = $arduino_serial|" room_sensors.py
echo "done."

echo "Creating cron job..."
echo "*/30 * * * *	$user $proj_dir/room_sensors.py > /dev/null &" > /etc/cron.d/room_sensors
echo "done."

echo "Setting up start up script"
sed -i "s|.*export PATH.*|export PATH='$PATH:$proj_dir'|" room-sensors
chmod 755 room-sensors
cp room-sensors /etc/init.d/room-sensors
update-rc.d room-sensors defaults
echo "done."

echo "Setting up database..."
mysql --user="$mysql_user" --password="$password" --execute="CREATE DATABASE IF NOT EXISTS $database;"

for i in "${sensors[@]}"
do
	mysql --user="$mysql_user" --password="$password" --execute="use $database; DROP TABLE IF EXISTS $i; CREATE TABLE $i (id INT NOT NULL AUTO_INCREMENT,value INT,unit VARCHAR(100),date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY ( id ) )"
done
echo "done."

echo "Setting up web page..."
sed -i "s|.*var ip =.*|var ip = '$ip'|" room-sensors
rm -rf /var/www/html/*
cp -a web/. /var/www/html/
echo "done."

/etc/init.d/room-sensors start
