

import pika,json,django

import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appointmentsystem.settings')

# django.setup()

from models import TempDoc



params=pika.URLParameters('amqps://lekpusth:E2YUqJHfhT78MLUBzsrivqxEAtYhCNVA@sparrow.rmq.cloudamqp.com/lekpusth')


connection=pika.BlockingConnection(params)

channel=connection.channel()


channel.queue_declare(queue='jeevan_raksha_appointment_queue')


def callback(ch,method,properties,body):
    print('Recieved in Jeevan Raksha Appointment App')
    data=json.loads(body)
    print(data)
    print(properties.content_type)
    print(data['username'])
    print(data['email'])

    if properties.content_type=='doctor_registered':
        doctor=TempDoc()
        doctor.Email=data["email"]
        doctor.Username=data["username"]

        doctor.save()
        print('Doctor created')



channel.basic_consume(queue='jeevan_raksha_appointment_queue',on_message_callback=callback,auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()