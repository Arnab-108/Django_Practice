from django.db import models
from mongoengine import Document , StringField, IntField , CASCADE , ReferenceField , BooleanField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
# Create your models here.


class User(Document):
    username= StringField(required=True)
    email = StringField(required=True , unique=True)
    password = StringField(required=True)
    gender = StringField(required=True)
    age = IntField(required=True)

    def set_password(self,raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self,raw_password):
        return check_password(raw_password ,self.password)

class Todo(Document):
    user = ReferenceField(User , required=True , reverse_delete_rule=CASCADE)
    user_name = StringField(required=True)
    title = StringField(required=True)
    description = StringField(required=True)
    completed = BooleanField(default=False)


