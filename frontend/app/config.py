"""App configuration."""
from os import environ
# import redis

class Settings:
    # Environment Variables
    MONGO_URI = environ.get("MONGO_URI")
    API_URI = environ.get("API_URI")
    SECRET_KEY = environ.get("SECRET_KEY")
    
    def __init__(self):
        if not self.MONGO_URI:
            raise ValueError("Missing environment variable: MONGO_URI")
        if not self.API_URI:
            raise ValueError("Missing environment variable: API_URI")
        if not self.SECRET_KEY:
            raise ValueError("Missing environment variable: SECRET_KEY")
    
# class Config:
# class Config:
#     # Environment Variables
#     REDIS_URI = environ.get("REDIS_URI")
    
#     def __init__(self):
#         if not self.REDIS_URI:
#             raise ValueError("Missing environment variable: REDIS_URI")
#         if not self.SECRET_KEY:
#             raise ValueError("Missing environment variable: SECRET_KEY")
    
#     # Flask-Session
#     SESSION_TYPE = 'redis'
#     SESSION_PERMANENT = False
#     SESSION_USE_SIGNER = True 
#     SESSION_REDIS = redis.from_url(REDIS_URI)