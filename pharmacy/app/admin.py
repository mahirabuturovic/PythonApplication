from django.contrib import admin
from . import models,Observer
from .models import Snizenje
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
# Register your models here.
admin.site.register(models.Lijek)
admin.site.register(models.Snizenje)
admin.site.register(models.UserProfile)
admin.site.register(models.LijekNarudzba)
admin.site.register(models.Faktura)
admin.site.register(models.Clanak)

@receiver(post_save,sender=Snizenje)
def obavijesti_korisnika(sender,instance,created,**kwargs):
  if(created==True):
      (Observer.ObavjestenjeOSnizenju()).obavijesti().notifySubscribers()

