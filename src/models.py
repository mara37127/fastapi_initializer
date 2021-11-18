import peewee


from config.database import db


class User(peewee.Model):

    username = peewee.CharField(unique=True)

    password = peewee.CharField(null=False)

    isActive = peewee.BooleanField(default=True)

    class Meta:
        database = db


class AuthModel(peewee.Model):

    username = peewee.CharField(unique=True)

    password = peewee.CharField(null=False)

    class Meta:
        database = db