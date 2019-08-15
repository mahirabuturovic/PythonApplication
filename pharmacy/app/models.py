
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.db.models.signals import post_save
# Create your models here.

class Lijek(models.Model):
    NAMJENA=(
        ('bol','bol'),
        ('prehlada','prehlada'),
        ('stres','stres'),
        ('otpornost','otpornost'),
        ('dijabetes','dijabetes'),
        ('rak','rak'),
        ('upala','upala')
    )
    id=models.CharField(primary_key=True,max_length=100)
    naziv=models.CharField(max_length=100)
    cijena=models.FloatField(default=None)
    slika=models.ImageField(default='default.png',blank=True,upload_to='media/')
    recept=models.BooleanField(default=False)
    opis=models.TextField(blank=True,null=True)
    slug=models.SlugField(unique='True')
    kod=models.CharField(max_length=50)
    namjena=models.CharField(max_length=100,choices=NAMJENA,default='none')

class Snizenje(models.Model):
    lijek=models.ForeignKey(Lijek,default=None,on_delete=models.CASCADE)
    iznos=models.IntegerField()
    datum=models.DateField(default=datetime.date.today)

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #dodatna polja
    notification=models.BooleanField(default=False)
    lijekovi=models.ManyToManyField(Lijek,blank=True)

class LijekNarudzba(models.Model):
    lijek = models.ForeignKey(Lijek, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)

class Faktura(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    lijekovi = models.ManyToManyField(LijekNarudzba)
    date_ordered = models.DateTimeField(auto_now=True)

class Clanak(models.Model):
    naslov=models.CharField(max_length=100)
    slug=models.SlugField()
    body=models.TextField()
    datum=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.naslov