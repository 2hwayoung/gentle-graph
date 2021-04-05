import yaml
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer

class Producer:
    def __init__(self, config_file: str, value_type: str = "json"):

        with open(config_file) as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)

        if value_type == "json":
            self.producer = KafkaProducer(
                bootstrap_servers=['kafka1:9092','kafka2:9092','kafka3:9092'],
                acks=1,
                compression_type="gzip",
                api_version=(0, 11, 5),
                value_serializer=lambda x: dumps(x).encode("utf-8"),
            )

        elif value_type == "string":
            self.producer = KafkaProducer(
                bootstrap_servers=f"{conf['kafka']['hosts'][0]}:{conf['kafka']['port']},{conf['kafka']['hosts'][1]}:{conf['kafka']['port']},{conf['kafka']['hosts'][2]}:{conf['kafka']['port']}",
                acks=1,
                compression_type="gzip",
                api_version=(0, 11, 5),
                value_serializer=lambda x: x.encode("utf-8"),
            )
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
