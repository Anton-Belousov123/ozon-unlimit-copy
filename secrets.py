import dataclasses
import os

import dotenv

dotenv.load_dotenv()


@dataclasses.dataclass
class EnvInfo:
    client_id: str
    api_key: str
    telegram_bot_token: str


env_info = EnvInfo(
    client_id=os.getenv('client_id'),
    api_key=os.getenv('api_key'),
    telegram_bot_token=os.getenv('telegram_bot_token')
)
