# config.py

class Config:
    SECRET_KEY = 'supersecret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://payuser:%40FutureBillionaire1@localhost/payroll_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
