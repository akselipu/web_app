import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://leopuustinen:aksu@localhost:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
