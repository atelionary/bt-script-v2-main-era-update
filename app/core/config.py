import os
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from app.constants import tao5_HOTKEY

# Load environment variables from .env file
load_dotenv(".env")


class Settings(BaseModel):
    VERSION: str = "0.1.0"
    NETWORK: str = "wss://entrypoint-finney.opentensor.ai:443"
    # WALLET_NAMES: List[str] = []
    # DELEGATORS: List[str] = []
    DEFAULT_RATE_TOLERANCE: float = 0.005
    DEFAULT_MIN_TOLERANCE: bool = False
    DEFAULT_RETRIES: int = 1
    DEFAULT_DEST_HOTKEY: str = tao5_HOTKEY
    
    # WALLET_NAMES: List[str] = os.getenv("WALLET_NAMES", "").split(",")
    # DELEGATORS: List[str] = os.getenv("DELEGATORS", "").split(",")
    WALLET_NAMES: List[str] = ["shib", "atel"]
    DELEGATORS: List[str] = ["5Fr9ArEKsuBgGyafH8u6G611KaCisYDhHuEb2LmD46HzkbzX" ,"5CHLb1prLQ4MjA6bYbpPfx1gzvaGpeSfXkk84sMDcNXRQDPd"]
    
    ADMIN_HASH: str = "$2b$12$tlj2uJ0FF9Gxk9x6yCtZkewTtfiBnesTJKIQD8YiDBtb9psjpHwUS"

settings = Settings()
