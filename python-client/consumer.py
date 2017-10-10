""" Read test data from Kafka to ensure producer and broker are working """

import json

from kafka import KafkaConsumer

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('test-topic',
                         group_id='test-consumer',
                         bootstrap_servers=['kafka:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s val=%s " % (message.topic, message.partition,
                                         message.offset, message.key, message.value))

# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume json messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))


# StopIteration if no message after 1sec
KafkaConsumer(consumer_timeout_ms=1000)
