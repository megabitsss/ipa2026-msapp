import pika
import os

def produce(host, username, password, body):
    #Create plain credentials
    credentials = pika.PlainCredentials(username, password)

    parameters = pika.ConnectionParameters(host=host, credentials=credentials)
    connection = pika.BlockingConnection(parameters) #synchronus connection with localhost
    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct") #create exchange named jobs with 'direct' type
    channel.queue_declare(queue="router_jobs") #create queue named router_jobs for storing messages
    channel.queue_bind(queue="router_jobs", exchange="jobs", routing_key="check_interfaces") #bind jobs (exchange) with router_jobs (queue)
    #with routing keys as 'check_interfaces'

    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body) #message publish testing, body=payload
    #sent message '192.168.1.44' to exchange 'jobs' with routing_keys 'check_interfaces'

    connection.close()

if __name__ == "__main__":
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost") #the second parameter is just in case var.
    rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER", "admin")
    rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS", "rabbitmq")

    produce(rabbitmq_host, rabbitmq_user, rabbitmq_pass,"192.168.1.44") #rabbitmq means rabbitmq container in network
