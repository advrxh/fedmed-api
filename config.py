import os


class CONFIG:
    debug = os.getenv("DEBUG") == "true"

    if debug:
        mongo_uri = os.getenv("DEBUG_MONGO_URI")
        host = os.getenv("DEBUG_HOST")
