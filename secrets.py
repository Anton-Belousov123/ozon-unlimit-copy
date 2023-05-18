import dataclasses
import os

import dotenv

dotenv.load_dotenv()


@dataclasses.dataclass
class EnvInfo:
    client_id: str
    api_key: str
    telegram_bot_token: str


@dataclasses.dataclass
class SecretInfo:
    DATABASE_NAME: str
    DATABASE_LOGIN: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str


env_info = EnvInfo(
    client_id=os.getenv('client_id'),
    api_key=os.getenv('api_key'),
    telegram_bot_token=os.getenv('telegram_bot_token')
)

secret = SecretInfo(DATABASE_NAME=os.getenv('DATABASE_NAME'),
                    DATABASE_LOGIN=os.getenv('DATABASE_LOGIN'),
                    DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD'),
                    DATABASE_HOST=os.getenv('DATABASE_HOST'),
                    DATABASE_PORT=os.getenv('DATABASE_PORT')
                    )