import pika, json

from main import app
from flask import Flask
from flask_mail import Mail, Message

params=pika.URLParameters('amqps://lekpusth:E2YUqJHfhT78MLUBzsrivqxEAtYhCNVA@sparrow.rmq.cloudamqp.com/lekpusth')


connection = pika.BlockingConnection(params)

channel = connection.channel()

mail = Mail(app) # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '*****'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


channel.queue_declare(queue='jeevan_raksha_appointment_queue')

def callback(ch,method,properties,body):
    print('Recieved in main service')
    data=json.loads(body)
    print(data)
    print(properties.content_type)

    if properties.content_type=="homePage":
        msg = Message(
                'Hello',
                sender ='****',
                recipients = ['****']
               )
        msg.body = 'Hello Flask message sent from Flask-Mail'
        mail.send(msg)
        print("mail sent")
        return 'Sent'



channel.basic_consume(queue='jeevan_raksha_appointment_queue', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()