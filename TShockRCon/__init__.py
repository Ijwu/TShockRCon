from flask import Flask
from TShockRCon import config

app = Flask(__name__)
secret_key = config.get_config_value("SECRET_KEY")
app.secret_key = secret_key


from TShockRCon import routes