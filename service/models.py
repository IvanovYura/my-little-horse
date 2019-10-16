from service.db.queries import fetch_user


class User:
    """
    Represents logic related to user
    """

    def __init__(self, name: str):
        user = fetch_user(name)

        self.name = user['name']
        self.password = user['password']
        self.is_admin = user['is_admin']

    def verify_password(self, password: str) -> bool:
        # here we should hash the password and compare with one from DB
        if password == self.password:
            return True

        return False
