from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

from app.config import(
    CONNECTION_STRING,
    KAFKA_BOOTSTRAP_SERVERS,
    KEY_SIZE,
    BLOCK_SIZE
)

engine = create_engine(url=CONNECTION_STRING)
Base = declarative_base()
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = LocalSession()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# video fileencryption
def generate_key():
    return os.urandom(KEY_SIZE)

def encrypt_file(input_path, output_path, key):
    iv = os.urandom(BLOCK_SIZE)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_path, "rb") as infile, open(output_path, "wb") as outfile:
        outfile.write(iv)  # prepend IV
        while chunk := infile.read(1024 * 1024):
            outfile.write(encryptor.update(chunk))
        outfile.write(encryptor.finalize())

# decrypt file
def decrypt_stream(file_path, key, chunk_size=1024 * 1024):
    with open(file_path, "rb") as infile:
        iv = infile.read(BLOCK_SIZE)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        while chunk := infile.read(chunk_size):
            yield decryptor.update(chunk)
        yield decryptor.finalize()

# send file to kafka
async def send_encrypted_video(topic: str ='test-topic', file_path: str = None, chunk_size=1024*512):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )
    await producer.start() 
    
    try:
        with open(file_path, "rb") as video_file:
            while chunk := video_file.read(chunk_size):
                await producer.send_and_wait(topic, chunk)
    except Exception as e:
        print(f"Error sending video: {e}")
    finally:
        await producer.stop()


# read file from kafka
async def get_video_stream(topic="test-topic"):
    try:
        consumer = AIOKafkaConsumer(
            topic, 
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            consumer_timeout_ms=10000,
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,
        )
        await consumer.start()

        async for msg in consumer:
            yield msg.value
    except Exception as e:
        print(f"Error reading video from Kafka: {e}")
    finally:
        await consumer.stop()