

import pika,json

params=pika.URLParameters('amqps://lekpusth:E2YUqJHfhT78MLUBzsrivqxEAtYhCNVA@sparrow.rmq.cloudamqp.com/lekpusth')


connection=pika.BlockingConnection(params)

channel=connection.channel()


channel.queue_declare(queue='jeevan_raksha_admin_queue')


def callback(ch,method,properties,body):
    print('Recieved in Jeevan Raksha Admin')
    print(body)

channel.basic_consume(queue='jeevan_raksha_dj_queue',on_message_callback=callback)

print('Started Consuming')

channel.start_consuming()

channel.close()