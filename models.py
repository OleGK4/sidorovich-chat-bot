from peewee import *
database = SqliteDatabase('sidor.db')


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    name = CharField(null=True)
    password = DateField(null=True)
    money = BigBitField(null=True)
    level = IntegerField(default='1')
    signup = IntegerField(default='setname')


class Quest(BaseModel):
    name = CharField()
    description = TextField()
    reward = IntegerField()
    difficulty = CharField()


class Item(BaseModel):
    name = CharField()
    description = TextField()
    price = IntegerField()


class QuestItem(BaseModel):
    item_id = ForeignKeyField(Item, backref='items')
    quest_id = ForeignKeyField(Quest, backref='items')


class UserQuest(BaseModel):
    user_id = ForeignKeyField(User, backref='quests')
    quest_id = ForeignKeyField(Quest, backref='quests')
    started = DateTimeField()
    ended = DateTimeField()
    status = CharField()


class UserItem(BaseModel):
    user_id = ForeignKeyField(User, backref='items')
    item_id = ForeignKeyField(Item, backref='items')
    started = DateTimeField()
    ended = DateTimeField()
    status = CharField()


class TraderItem(BaseModel):
    item_id = ForeignKeyField(Item, backref='items')


def createtables():
    database.connect()
    database.create_tables([User, Quest, Item, QuestItem, UserQuest, UserItem, TraderItem])
    database.close()


