import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/gastos_comunes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
