# class ProductionConfig:
#     def __init__(self):
#         self.ENV = "production"
#         self.DEBUG = False
#         self.PORT = 80
#         self.HOST = '0.0.0.0'
from .config import BaseConfig

class ProductionConfig(BaseConfig):
    DEBUG = False
