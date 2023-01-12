

import pika,json

params=pika.URLParameters('amqps://lekpusth:E2YUqJHfhT78MLUBzsrivqxEAtYhCNVA@sparrow.rmq.cloudamqp.com/lekpusth')


connection=pika.BlockingConnection(params)

channel=connection.channel()


channel.queue_declare(queue='jeevan_raksha_appointment_queue')


def callback(ch,method,properties,body):
    print('Recieved in Jeevan Raksha Admin')
    data=json.loads(body)
    print(data)

channel.basic_consume(queue='jeevan_raksha_appointment_queue',on_message_callback=callback,auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()