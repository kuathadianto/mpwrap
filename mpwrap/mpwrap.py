#!/usr/bin/env python3
from paho.mqtt import client as mqtt
from paho.mqtt.publish import single as publish
from datetime import datetime
import time, configparser, sys, getopt, logging


# Main function
def main(argv):
    # Return time in unix format
    def now_in_unix():
        return int(time.mktime(datetime.now().timetuple()))

    # Get arguments if available
    opts = getopt.getopt(argv, 'c:l:')

    args = {}
    for arg in opts[0]:
        args[arg[0]] = arg[1]

    # Check arguments
    if '-c' in args:
        conf_filename = args['-c']
    else:
        conf_filename = './conf.ini'

    if '-l' in args:
        log_filename = args['-l']
    else:
        log_filename = './mpwrap_log.txt'

    logging.basicConfig(filename=log_filename,
                        level=logging.DEBUG,
                        format='%(levelname)s %(asctime)s : %(message)s',
                        filemode='w')
    logger = logging.getLogger()

    # Read config
    conf = configparser.ConfigParser()
    conf.read(conf_filename)

    # Get all templates
    temps = {}
    for section in conf.sections():
        if 'template-' in section:
            name = section.split('template-')[-1]
            temps[name] = {}
            temps[name]['host'] = conf.get(section, 'host')
            temps[name]['port'] = int(conf.get(section, 'port'))
            temps[name]['topic'] = conf.get(section, 'topic')
            temps[name]['qos'] = int(conf.get(section, 'qos'))
            temps[name]['payload'] = conf.get(section, 'payload')

    # The callback for when the client receives a CONNACK response from the server
    def on_connect(client, userdata, flags, rc):
        # Get info in the first run
        log_message = 'Connected with result code ' + str(rc)
        logger.info(log_message)
        print(log_message)

        # Subscribe to the source topic
        client.subscribe(conf.get('source', 'topic'))

    # The callback for when a PUBLISH message is received from the server
    def on_message(client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        splitted_payload = payload.split('|')
        t = splitted_payload[0]
        message = splitted_payload[-1]

        # Looking for the right template
        if t in temps:
            output = temps[t]['payload']
            output = output.replace('__payload__', message)
            output = output.replace('__now__', str(now_in_unix()))
            logger.info('"' + output + '"' + ' to ' + temps[t]['host'] + ':' + str(temps[t]['port']) + '-' + temps[t]['topic'])
            print(output)

            # Resend to the destination after the message is wrapped
            publish(temps[t]['topic'], output, temps[t]['qos'], hostname=temps[t]['host'], port=temps[t]['port'])
        else:
            log_message = 'No template found, not processed.'
            logging.warning(log_message)
            print(log_message)

    # Run wrapper
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(conf.get('source', 'host'), int(conf.get('source', 'port')))
    client.loop_forever()


if __name__ == '__main__':
    main(sys.argv[1:])

