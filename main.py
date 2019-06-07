from TwitterInjector import TwitterInjector
from confluent_kafka import Producer

if __name__ == "__main__":
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    producer.produce("TutorialTopic", "FUCK YOU")
    """
    print("==========STARTING===========")
    connector = TwitterInjector()
    connector.start_stream(follow="85741735")
    print("==========ENDING===========")
    """
