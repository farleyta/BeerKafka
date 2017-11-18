from flask import Blueprint, jsonify, request
from pykafka import KafkaClient
from flask_cors import cross_origin
from auth import requires_auth
import json

routes = Blueprint('routes', __name__)

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

# GET current list of topics
@routes.route('/topics')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def topics():
    client = get_kafka_client()
    return jsonify([topic for topic in client.topics])


# POST new message to specified topic
@routes.route('/topics/<topic>', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def topics_new(topic):
    message = request.get_json()
    client = get_kafka_client()
    topic = client.topics[topic.encode('ascii')]
    if not (topic):
        return 'No topic found for: {topic}'.format(topic=topic)
    producer = topic.get_sync_producer()
    producer.produce(json.dumps(message))
    return "Message added successfully"
