import abc
from django.utils import timezone
from django.apps import apps

class Subject:

    @abc.abstractmethod
    def provjera(self,lijek,owner):
        pass


class Proxy(Subject):
    def __init__(self,real_subject):
        self.realSubject = real_subject

    def provjera(self,lijek,owner):
        return self.realSubject.provjera(lijek,owner)

class RealSubject(Subject):

    def __init__(self,kod):
        self.kod=kod

    def provjera(self,lijek,owner):

        if(lijek.kod==self.kod or lijek.recept==False):
            model_narudzba = apps.get_model('app', 'Faktura')
            model_narudzba_lijek = apps.get_model('app', 'LijekNarudzba')
            narudzba_lijek = model_narudzba_lijek.objects.create(lijek=lijek)
            narudzba = model_narudzba.objects.filter(owner=owner, is_ordered=False)
            if narudzba.exists():
                narudzba = narudzba[0]
                if narudzba.lijekovi.filter(lijek__slug=lijek.slug).exists():
                   narudzba_lijek.quantity += 1
                   narudzba_lijek.save()
                   return True

                else:
                   narudzba.lijekovi.add(narudzba_lijek)
                   return True
            else:
               ordered_date = timezone.now()
               narudzba = model_narudzba.objects.create(owner=owner, date_ordered=ordered_date)
               narudzba.lijekovi.add(narudzba_lijek)
               return True
        else:
            return False


