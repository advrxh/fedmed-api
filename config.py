import os


class CONFIG:
    debug = os.getenv("DEBUG") == "true"

    if debug:
        mongo_uri = os.getenv("DEBUG_MONGO_URI")
        host = os.getenv("DEBUG_HOST")
        redis_host = os.getenv("DEBUG_REDIS_HOST")
        redis_port = os.getenv("DEBUG_REDIS_PORT")
        redis_password = os.getenv("DEBUG_REDIS_PASSWORD")
