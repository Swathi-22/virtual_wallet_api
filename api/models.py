from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


GENDER = (("Male","Male"),("Female","Female"),("Other","Other"),)
STATUS = (("Pending","Pending"),("Completed","Completed"),("Failed","Failed"))
REQUEST_STATUS = (('pending','pending'),('accepted','accepted'),('rejected','rejected'))

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture = models.FileField(null=True,blank=True)
    place = models.CharField(max_length=100,null=True,blank=True)
    gender = models.CharField(max_length=10,null=True,blank=True,choices=GENDER)
    date_of_birth = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,null=True,blank=True,choices=STATUS)
    

class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    wallet_id = models.CharField(max_length=10,null=False,blank=False,unique=True)
    balance = models.DecimalField(default=0,null=False,blank=False,decimal_places=2,max_digits=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=10,null=True,blank=True,choices=GENDER)


class Transaction(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_transaction_from")
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_transaction_to")
    amount = models.DecimalField(default=0,null=False,blank=False,decimal_places=2,max_digits=15)
    status = models.CharField(max_length=10,null=True,blank=True,choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    request_status = models.CharField(max_length=10,null=True,blank=True,choices=REQUEST_STATUS)


class Request(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_request_from")
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_request_to")
    amount = models.DecimalField(default=0,null=False,blank=False,decimal_places=2,max_digits=15)
    status = models.CharField(max_length=10,null=True,blank=True,choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(signal=post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(signal=post_save,sender=User)
def create_wallet(sender,instance,created,**kwargs):
    if created:
        wallet_id = f"{instance.id}_wallet_{instance.username[0]}_{str(instance.id).zfill(4)}"
        Wallet.objects.create(user=instance,wallet_id=wallet_id)