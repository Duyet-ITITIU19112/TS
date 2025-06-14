# from flask import Flask, render_template
#
# # Configuration class
# class DevConfig:
#     def __init__(self):
#         self.ENV = "development"
#         self.DEBUG = True
#         self.PORT = 5000
#         self.HOST = '0.0.0.0'
#
# # Instantiate the app
# app = Flask(__name__)
#
# # Load configuration
# config = DevConfig()
# app.config['ENV'] = config.ENV
# app.config['DEBUG'] = config.DEBUG
#
# # Define route for home screen
# @app.route('/')
# def home():
#     return render_template('index.html')  # Looks for templates/index.html
#
# # Run the app
# if __name__ == '__main__':
#     app.run(host=config.HOST, port=config.PORT)


from .config import BaseConfig

class DevConfig(BaseConfig):
    DEBUG = True
