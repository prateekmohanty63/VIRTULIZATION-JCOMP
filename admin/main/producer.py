# url: amqps://lekpusth:E2YUqJHfhT78MLUBzsrivqxEAtYhCNVA@sparrow.rmq.cloudamqp.com/lekpusth



import pika,json

params=pika.URLParameters('amqps://lekpusth:E2YUqJHfhT78MLUBzsrivqxEAtYhCNVA@sparrow.rmq.cloudamqp.com/lekpusth')


connection=pika.BlockingConnection(params)

channel=connection.channel()



def publish(method,body):
    properties=pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='jeevan_raksha_appointment_queue',body=json.dumps(body),properties=properties)
