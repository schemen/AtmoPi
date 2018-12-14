# AtmoPi

## Create and install virtual environment
```x-sh
git clone https://github.com/schemen/AtmoPi.git && cd AtmoPi
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
## Usage
### Help output

```
$ ./ap.py --help
Usage: ap.py [OPTIONS] COMMAND [ARGS]...

  Welcome to AtmoPi, your very own DIY Weather station

Options:
  --help  Show this message and exit.

Commands:
  db      Commands regarding the sensors
  sensor  Commands regarding the sensors
  start   Start AtmoPi
```

### Configuration
Copy the config.ini.example to config.ini
```
[CONFIG]
AP_LOCATION="Livingroom"
AP_NAME="AtmoPy 1"
POLL_INTERVAL=60
INFLUXDB_DATABASE=atmopi
INFLUXDB_SERVER=db.example.com
INFLUXDB_PORT=8086
INFLUXDB_USER=root
INFLUXDB_PASSWORD=root
SENSOR_LIST=mock,mock_temp,grove_temp_hum_pro
```
##### AP_LOCATION
This is the location where your AtmoPi is located. This value will be transmitted with the sensor data to your influxdb as a tag.

##### AP_NAME
This is the name of your AtmoPi. This value will be transmitted with the sensor data to your influxdb as a tag.

##### POLL_INTERVAL
Interval where the `Collector` gets data from the sensors. Note that if this value is lower than the Sensors capability, it will use the sensors pre set minimum interval.

##### Influx DB Options
Those are self-explanatory. HTTP is used.

##### SENSOR_LIST
List of enabled sensors. Currently available sensors:
* mock
* mock-temp
* [grove_temp_hum_pro](http://wiki.seeedstudio.com/Grove-Temperature_and_Humidity_Sensor_Pro/)

## Other requirements for GrovePi

```
apt-get install libatlas-base-dev
```
