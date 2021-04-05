import yaml
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer

class Producer:
    def __init__(self, config_file: str, value_type: str = "json", acks: int = 1):

        with open(config_file) as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)

        hosts = conf["kafka"]["hostname"]
        port = conf["kafka"]["port"]

        if value_type == "json":
            self.producer = KafkaProducer(
                bootstrap_servers=[f'{hosts[0]}:{port}', f'{hosts[1]}:{port}',f'{hosts[2]}:{port}'],
                acks=acks,
                compression_type="gzip",
                api_version=(0, 11, 5),
                value_serializer=lambda x: dumps(x).encode("utf-8"),
            )

        elif value_type == "string":
            self.producer = KafkaProducer(
                bootstrap_servers=[f'{hosts[0]}:{port}', f'{hosts[1]}:{port}',f'{hosts[2]}:{port}'],
                acks=acks,
                compression_type="gzip",
                api_version=(0, 11, 5),
                value_serializer=lambda x: x.encode("utf-8"),
            )

            # key 를 넣을떈 아래 조건도 KafkaProducer에 추가
            # key_serializer=lambda x: x.encode("utf-8"),

    def __del__(self):
        self.producer.close()

    def send_to_topic(self, topic: str, value):
        self.producer.send(topic=topic, value=value).add_callback(self.on_send_success).add_callback(self.on_send_error)
        self.producer.flush()

    def on_send_success(self, metadata):
        print('topic:', metadata.topic,'partition:', metadata.partition, 'offset:',metadata.offset)

    def on_send_error(self, excp):
        log.error('I am an errback', exc_info=excp)



class Consumer:

    def __init__(self):
        pass
