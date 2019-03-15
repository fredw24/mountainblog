from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        users = User.objects.filter(email = postData['email'])
        if len(users) > 0:
            errors["email"] = "This email has already existed"
        if len(postData['fname']) < 2:
            errors["fname"] = "Your first name is too small"
        if len(postData['lname']) < 2:
            errors["lname"] = "Your last name is too small"    
        if not EMAIL_REGEX.match(postData['email']): 
            errors["email"] = "Email must be valid"
        if len(postData['pcode']) < 8:
            errors["pcode"] = "Password is too small"
        if postData['pcode'] != postData['pcodeCon']:
            errors["pcode"] = "Password does not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        salt = bcrypt.gensalt()
        if len(user) == 0: 
            errors["email"] = "This email does not exist"
        elif not bcrypt.checkpw(postData['pcode'].encode(), user[0].password.encode()):
            errors["pcode"] = "No Password found"
        return errors


class MountainManager(models.Manager):
    def mountain_validator(self, postData):
        errors = {}
        if len(postData['newmountain']) < 3:
            errors['newmountain'] = "Your Mountain title is less than 3 characters"
        if len(postData['newlocation']) < 3:
            errors['newlocation'] = "Mountain location is required"
        return errors

    def like_validator(self, postData):

        errors = {}
        getuser = User.objects.get(id = postData['userid'])

        mountain = Mountain.objects.filter(users_who_like = getuser, id = postData['mountainid'])
        if len(mountain) > 0:
            errors['userid'] = "You Already put a Like on the Mountain"
        return errors

    def unlike_validator(self, postData):
        errors = {}
        getUser = User.objects.get(id = postData['userid'])
        mountain = Mountain.objects.filter(users_who_like = getUser, id = postData['mountainid'])
        if len(mountain) == 0:
            errors['userid'] = "You did not have any like"
        return errors

class BlogManager(models.Manager):
    def blog_validator(self, postData):
        errors = {}
        if len(postData['blogprocess']) < 15:
            errors['blogprocess'] = "Your Blog is too small"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Mountain(models.Model):
    mountain = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name = "mountain", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name = "liked_mountain")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MountainManager()

class Blog(models.Model):
    blog = models.TextField()
    user = models.ForeignKey(User, related_name = "bloguser", on_delete=models.CASCADE)
    mountain = models.ForeignKey(Mountain, related_name = 'blogmountain', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BlogManager()
