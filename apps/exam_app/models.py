from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Manager(models.Manager):
    def basic_validator(self, postData, type):
        if type == "Register":
            errors = []
            if len(postData['name']) < 0:
                errors.append("You need to enter in a first name!")
            if len(postData['password']) < 8:
                errors.append("You need to enter in a password 8 characters or longer!")
            if postData['confirmpw'] != postData['password']:
                errors.append("Your passwords do not match!")
            if len(postData['email']) < 0:
                errors.append("You need to enter in an email!")
            if not EMAIL_REGEX.match(postData['email']):
                errors.append("You need to enter in a valid email!")
            if len(postData['date']) < 0:
                errors.append("Please enter your date of birth!")
            if len(errors) > 0:
                return errors
            elif len(errors) == 0:
                hashpass = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt(5))
                new_user = User.objects.create(name=postData['name'], email=postData['email'], password=hashpass)
                return new_user
        if type == "Login":
            lerrors = []
            if len(User.objects.filter(email=postData['Logemail'])) > 0:
                user = User.objects.filter(email=postData['Logemail'])[0]
                if not bcrypt.checkpw(postData['Logpassword'].encode(), user.password.encode()):
                    lerrors.append("Incorrect email or password")
                    return lerrors
            elif len(User.objects.filter(email=postData['Logemail'])) == 0:
                lerrors.append("Incorrect email or password")
                return lerrors
            return user


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date = models.DateField(null=True)
    objects = Manager()

    def __repr__(self):
        return "<User Object: {} {} {} {}>".format(self.name, self.email, self.password, self.date)


class Task(models.Model):
    taskname = models.CharField(max_length=255)
    taskstatus = models.CharField(max_length=255)
    tasktime = models.TimeField(auto_now_add=False, blank=True)
    taskdate = models.DateTimeField(null=True)
    task = models.ForeignKey(User, related_name="tasks", null=True)

    def __repr__(self):
        return "<User Object: {} {}>".format(self.taskname, self.taskstatus)


class NewTask(models.Model):
    newtaskname = models.CharField(max_length=255)
    newtaskstatus = models.CharField(max_length=255)
    newtasktime = models.TimeField(auto_now_add=False, blank=True)
    newtaskdate = models.DateTimeField(null=True)
    newtask = models.ForeignKey(User, related_name="newtasks", null=True)

    def __repr__(self):
        return "<User Object: {} {}>".format(self.newtaskname, self.newtaskstatus)
