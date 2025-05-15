from src.config.dev_config import DevConfig
from src.config.production_config import ProductionConfig
from flask_session import Session
import os

class Config:
    def __init__(self):
        self.dev_config = DevConfig()
        self.production_config = ProductionConfig()

