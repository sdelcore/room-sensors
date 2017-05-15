#!/bin/bash
user=pi
mysql_user=root
password=asd
database=sensors
sensors=(dht11_temperature dht11_humidity sound light temperature)
proj_dir=/home/$user/room-sensors

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
platformio run -t upload
cd ..
echo "done."

echo "Creating cron job..."
echo "*/30 * * * *	$user $proj_dir/room_sensors.py > /dev/null &" > /etc/cron.d/room_sensors
echo "done."

echo "Setting up start up script"
sed -i "s|.*export PATH.*|export PATH='$PATH:$proj_dir'|" room-sensors
cp room-sensors /etc/init.d/
update-rc.d room-sensors defaults
echo "done."

echo "Setting up database..."
mysql --user="$mysql_user" --password="$password" --database="$database" --execute="DROP DATABASE $database; CREATE DATABASE $database;"

for i in "${sensors[@]}"
do
	mysql --user="$mysql_user" --password="$password" --execute="use $database; CREATE TABLE $i (id INT NOT NULL AUTO_INCREMENT,value INT,unit VARCHAR(100),date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY ( id ) )"
done
echo "done."

echo "Setting up web page..."
rm -rf /var/www/html/*
cp -a web/. /var/www/html/
echo "done."

/etc/init.d/room-sensors start
