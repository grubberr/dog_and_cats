#!/Users/ant/dog_and_cats/env/bin/python3

from mongoengine import *
connect('mydb')

date_format = '%m/%d/%Y'

class User(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    birthday = DateTimeField(required=True)

    def __str__(self):
        return "pk = %s, first_name: %s, last_name: %s, birthday: %s" % (
            self.pk,
            self.first_name,
            self.last_name,
            self.birthday.strftime(date_format))


class Pet(Document):
    name = StringField(required=True)
    birthday = DateTimeField(required=True)
    owner = ReferenceField('User', required=True)

    meta = {'allow_inheritance': True}

    def __str__(self):
        return "pk = %s, name: %s, birthday: %s, owner: %s" % (
            self.pk,
            self.name,
            self.birthday.strftime(date_format),
            self.owner.first_name)

class Cat(Pet):
    pass

class Dog(Pet):
    pass
