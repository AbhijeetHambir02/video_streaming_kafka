from fastapi.security import OAuth2PasswordBearer
from urllib.parse import quote_plus

FILE_UPLOAD = "uploads"

ALGORITHM = 'HS256'
SECRET_KEY = 'my-secret-key'
TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

HOST = "localhost"
USER = "postgres"
PASSWORD = quote_plus("your-password")
PORT = 5432
DATABASE = "innovator_assessment"

CONNECTION_STRING = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"



# Kafka
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
MAX_REQUEST_SIZE = 1024*1204*20
FETCH_MAX_BYTES = 1024*1024*20

# encryption
KEY_SIZE = 32
BLOCK_SIZE = 16
