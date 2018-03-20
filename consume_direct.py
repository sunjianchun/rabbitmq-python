# encoding:utf-8
#!/opt/environment/python/rabbitmq/bin/python

import pika
import time

exchange = 'direct_test'
exchange_type = 'direct'

def callback(ch, method, properties, body):
	print "received %s" % body
	print "done"
severities = ['info', 'warning']
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(
		exchange=exchange, 
		exchange_type=exchange_type
	)

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
for severity in severities:
	channel.queue_bind(
		queue=queue_name,
		exchange=exchange,
		routing_key=severity
	)

channel.basic_consume(
	callback, 
	queue=queue_name,
	no_ack=True
	)
print "Waiting for messages. To exit press CTRL+C"
channel.start_consuming()
