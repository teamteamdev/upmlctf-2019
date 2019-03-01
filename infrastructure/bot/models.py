from datetime import datetime
from peewee import *

db = PostgresqlDatabase("db", user="writer", password="DrARYwy523", host="10.239.0.250", port=5432)


class ArrayField(CharField):
    def db_value(self, value):
        return str(value)

    def python_value(self, value):
        return eval(value)


class Request(Model):
    token = CharField(max_length=60)
    date = DateTimeField()
    activated = BooleanField()

    class Meta:
        database = db


class Promo(Model):
    code = CharField(max_length=60)
    team_id = IntegerField()
    activated = BooleanField(default=False)

    class Meta:
        database = db


class Client(Model):
    user_id = IntegerField(primary_key=True)
    activated = BooleanField()
    name = CharField(null=True, max_length=250)
    team_id = IntegerField(null=True)
    state = IntegerField()
    msg_id = IntegerField(null=True)
    valid_till = CharField(null=True, max_length=6)
    card_number = CharField(max_length=36, null=True)
    cvv = CharField(null=True, max_length=60)
    balance = IntegerField(null=True)
    args = ArrayField(default=[])
    exploited_1 = BooleanField()
    exploited_2 = BooleanField()
    exploited_3 = BooleanField()

    class Meta:
        database = db


class History(Model):
    from_card = CharField(max_length=60)
    to_card = CharField(max_length=60)
    time = DateTimeField()
    amount = IntegerField()

    class Meta:
        database = db

