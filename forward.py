import pika
import smtplib


def email(FROM,TO,message):
    server = smtplib.SMTP("74.125.22.108", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    data=eval(body)
    email(data['FROM'],data['TO'],data['message'])
    print "sent email"
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

channel.start_consuming()