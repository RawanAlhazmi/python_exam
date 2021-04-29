from django.db import models
import bcrypt
import re
from datetime import datetime, timedelta

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}         
        if len(postData['f_name']) < 2:
            errors["f_name"] = "First name should be at least 2 characters"
        if len(postData['l_name']) < 2:
            errors["l_name"] = "Last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors["confirm"] = "Password doesn't match"
        user_list = User.objects.filter(email=postData['email'])
        if len(user_list)>0: 
            errors["not_u"] = "Email is already Taken"
        # year = timedelta(days=365)
        # thirteen_years = 13 * year
        # today = datetime.today()
        # birthday = datetime.strptime(postData['date'],'%Y-%m-%d')
        # if birthday > datetime.today() - thirteen_years:
        #     errors['birthday'] = "You must be at least 13 years old"
        # if today < birthday:
        #     errors["date"] = "Your BD must be in the past"
        return errors

    def login_validator(self, postData):
            errors = {}  
            # email validation     
            if len(postData['email']) == 0:
                errors["email"] = "Email is Required"
            else:
                EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
                if not EMAIL_REGEX.match(postData['email']):                
                    errors['email'] = "Invalid email address!"
            # password validation
            if len(postData['password']) == 0:
                errors["password"] = "Password is Required"
            else:
                if len(postData['password']) < 8:
                    errors["password"] = "Password should be at least 8 characters"
                user = User.objects.filter(email=postData['email'])
                if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                    errors["wrong"] = "Password isn't correct"
            return errors

class WishManager(models.Manager):
    def basic_validator(self, postData):
            errors = {}  
            # Item validation     
            if len(postData['item']) == 0:
                errors["item"] = "Item is Required"
            else:
                if len(postData['item']) < 3:
                    errors["item"] = "Item should be at least 3 characters"
            # Description validation
            if len(postData['desc']) == 0:
                errors["desc"] = "Description is Required"
            else:
                if len(postData['desc']) < 3:
                    errors["desc"] = "Description should be at least 3 characters"
            return errors




# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    # wishes
    # liked_wishes
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wish(models.Model):
    Item = models.CharField(max_length=45)
    description = models.TextField()
    granted_date = models.DateField(default=datetime.now())
    granted = models.BooleanField(default=False)
    wisher = models.ForeignKey(User, related_name="wishes", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_wishes")
    objects = WishManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
