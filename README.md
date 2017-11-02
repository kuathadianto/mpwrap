# MQTT Payload Wrapper
## What is this?
MQTT Payload Wrapper is a [worker](https://en.wikipedia.org/wiki/Thread_pool) for [MQTT](https://en.wikipedia.org/wiki/MQTT) Broker.
This worker act as a bridge between two topics from two different (but can also same) hosts. With this worker, you can wrap your MQTT
payload with a template you designed and then send it to the destination after the message is wrapped.

## Why is this matters?
Sometimes you want to send a big redundant message from your not-so-powerful IoT devices like [Arduino Nano](https://store.arduino.cc/arduino-nano) 
and [Micro](https://store.arduino.cc/arduino-micro). I say not so powerful, because of limitation of RAM from these two devices.
Suppose with those two devices, you want to send a temperature data from temperature sensor attached to these devices. 
Normally, you have to send just that 5 characters temperature data (example: 20.53), but your boss want it to be in a long JSON format.
Because of lack of RAM, those devices cannot handle the sending message correctly with those long JSON format. Because of that reason, I made
this worker.

## Help! I still don't understand what you mean and how it works...
Suppose you have this setup:
![Setup #1](https://github.com/kuathadianto/mpwrap/raw/master/readmeimg/a.png)
Data Publisher publish temperature to the broker installed on Raspberry Pi, and the PC is the subscriber, which is, everytime data
publisher publish a message, the PC get that message automatically. The PC wants the data of that temperature on this JSON format:
```javascript
{
  "name" = "temperature"
  "data" = "20.53",
  "time" = "1508843039",
  "desc" = "Temperature from data source."
 }
```
What we can see from this format, what is actually changed everytime the data publisher send the message is data (temperature data) and
time (Note: Time in this example is in [unix format](https://en.wikipedia.org/wiki/Unix_time)). Because of that long message, sometimes 
low powered devices is not capable to make this happens.

And then, you install this worker on the Raspberry Pi. With this worker, you make a template called **t_template** and you design that template like this:
```javascript
{
  "name" = "temperature"
  "data" = __payload__,
  "time" = __now__,
  "desc" = "Temperature from data source."
 }
```
Now, instead sending that full JSON format from the Arduino, you only send this:
```javascript
t_template|20.53
```
Note that **t_template** is the name of our template, and 20.53 is temperature data. \_\_payload\_\_ from our template will be replaced 
with temperature data, and \_\_now\_\_ will be replaced with time. Now Arduino send only a short message, but the subscriber (PC) still 
got the message in original full JSON format. Only with that, now Arduino can provide the temperature data peacefully.

Anyway, this is the new setup after mpwrap is installed:
![Setup #2](https://github.com/kuathadianto/mpwrap/raw/master/readmeimg/b.png)

## Cool, so how to configure this thing and how to use it?
### Install as a service on Raspberry Pi/Ubuntu

1. If you don't have mosquitto & unzip installed, install it first:
```bash
sudo apt-get update
sudo apt-get install mosquitto unzip
```
2. Download this zip and unzip it:
```bash
wget https://github.com/kuathadianto/mpwrap/archive/master.zip -O mpwrap.zip
unzip mpwrap.zip
```

3. Make the installation script executable and then install it:
```bash
sudo chmod +x mpwrap-master/raspi-install.sh
cd mpwrap-master
./raspi-install.sh
```
If there are any questions during installation, just answer with 'Yes'
(press Y and then press Enter).

Done! mpwrap is now installed and ready to use.

### Using mpwrap as portable app
Just download this zip, install the requirements on requirement.txt and then run the mpwrap.py on mpwrap folder.

### Uninstallation
Run raspi-uninstall.sh script. Make sure to make it executable first (sudo chmod +x raspi-uninstall.sh).

### Configuration
If you install this as a service on Raspberry Pi or Ubuntu, the configuration file is located on __/etc/mpwrap/conf.ini__.
If you use this as portable app, conf.ini is located on the same folder as mpwrap.py.

On conf.ini, you will find two sections: source and template-example.
On [source], you can configure where the wrapper will subscribe to. For example, the default configuration has this values:
```ini
[source]
host = localhost
port = 1883
topic = mpwrap/in
```
This will make the wrapper subscribing to the localhost broker with port 1883 on the topic mpwrap/in. For every incoming
message to this broker on topic mpwrap/in, the wrapper with examine it and process it according to the template.

After [source], you can create as many templates as you want. For this, you create a new section called [template-{your template name}].
For example, on default conf.ini, you can find a template named example ([template-example]). That templates has these values:
```ini
[template-example]
host = localhost
port = 1883
topic = mpwrap/example
qos = 0
payload = __now__: __payload__
```

Host, port and topic is where the message with this template will be forwarding to. QoS is quality of service (see [MQTT QoS](https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels)).
payload is the wrapper. So for example, if message "example|Hi" has arrived, this message will be wrapped with "example" template.
This message has payload "Hi". On example template, the payload will be wrapped into \_\_now\_\_: \_\_payload\_\_. \_\_now\_\_ and \_\_payload\_\_
is reserved variables. \_\_now\_\_ will be replaced with time in unix format, and then \_\_payload\_\_ will be replaced with payload
from input origin. After wrapped, the message "1509618095: Hi" (1509618095 is just example for unix time) will be forwared
into localhost broker with port 1883 to the topic mpwrap/example.

If you change the configuration file, be sure to restart the mpwrap. If you install mpwrap as a service, you can use this command:
```bash
sudo service mpwrap stop
sudo service mpwrap start
```

### Log file
If something doesn't work as expected, you can see the log file, located on __/etc/mpwrap/log.txt__ if you install mpwrap
as a service or __mpwrap_log.txt__ on the same folder as mpwrap if you run it as a portable app.

For more info about this worker, questions, suggestions, or feature requests, please contact me via twitter at:
[@kuathadianto](https://twitter.com/kuathadianto)

Enjoy! :)
