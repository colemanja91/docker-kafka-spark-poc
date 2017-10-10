""" Generate test data to send to Kafka """

import random
from time import sleep
from json import dumps

from kafka import KafkaProducer, KafkaClient

################################################################################
# Import test data
################################################################################

TEST_DATA = [
    {'id': 1, 'foo': 'bar'},
    {'id': 2, 'foo': 'baz'},
    {'id': 3, 'foo': 'bnat'}
]

################################################################################
# Set up producer
################################################################################

KAFKA = KafkaClient('kafka:9092')
PRODUCER = KafkaProducer(
    bootstrap_servers='kafka:9092',
    client_id='test-producer'
)

TOPIC = 'test-topic'

################################################################################
# Loop, add to kafka
################################################################################

LOOP = True

while LOOP:

    rown = random.randint(0, len(TEST_DATA))

    rec = TEST_DATA[rown]

    try:
        #avro_push(rec)
        PRODUCER.send(TOPIC, value=dumps(rec))
    except UnicodeDecodeError:
        pass

    print('pushed: %s' % rown)

    # Send records at random intervals; adjust this to send more or less frequently
    sleep(random.uniform(0.01, 5))
