import pika
import os


def produce(host, username, password, body):
    # Create plain credentials
    credentials = pika.PlainCredentials(username, password)

    parameters = pika.ConnectionParameters(host=host, credentials=credentials)
    # synchronus connection with localhost
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # create exchange named jobs with 'direct' type
    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    # create queue named router_jobs for storing messages
    channel.queue_declare(queue="router_jobs")
    # bind jobs (exchange) with router_jobs (queue)
    channel.queue_bind(queue="router_jobs", exchange="jobs", routing_key="check_interfaces")
    # with routing keys as 'check_interfaces'
    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body) #message publish testing, body=payload
    connection.close()


if __name__ == "__main__":
    # the second parameter is just in case var.
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost") 
    rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER", "admin")
    rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS", "rabbitmq")
    # rabbitmq means rabbitmq container in network
    produce(rabbitmq_host, rabbitmq_user, rabbitmq_pass,"192.168.1.44") 
