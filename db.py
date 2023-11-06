import sqlite3
from models import User


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.Connection(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, id):
        with self.connection:
            User.create(id=id)

    def user_exists(self, id):
        with self.connection:
            result = User.select().where(User.id == id).prefetch()
            return bool(len(result))

    def set_name(self, id, name, data):
        with self.connection:
            return User.update(name=name, signup=data).where(User.id == id).execute()

    def get_name(self, id):
        with self.connection:
            result = User.select().where(User.id == id).prefetch()
            for row in result:
                name = row.name
            return name

    def get_signup(self, id):
        with self.connection:
            result = User.select().where(User.id == id).prefetch()
            for row in result:
                signup = row.signup
            return signup

    def set_signup(self, id, signup):
        with self.connection:
            return User.update(signup == signup).where(User.id == id)
