users_db = {
    "ivan": {
        "id": 1,
        "username": "ivan",
        "email": "ivan@gmail.com",
        "hashed_password": b'$2b$12$FWEH5dusmHZP0MHdlyblp.EgPEF6J4wetZm9EUukGFjOUBLEDoO7y'
    }
}

def get_user(username: str):
    return users_db.get(username)