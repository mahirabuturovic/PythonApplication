from django.conf import settings
from django.apps import apps
import abc
import  datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string

class SubjectPharmacy:
    def __init__(self):
        self.__subscribers = []
        self.__obavjestenje=None

    def attach(self, subscriber):
        self.__subscribers.append(subscriber)

    def detach(self):
        self.__subscribers.pop()

    def notifySubscribers(self):
        for sub in self.__subscribers:
            sub.update()

    def setObavjestenje(self):
        Snizenje = apps.get_model('app', 'Snizenje')
        start = datetime.date.today()
        year = datetime.date.today().year
        end = datetime.date(year, 12, 31)
        snizeni_lijekovi = Snizenje.objects.filter(datum__range=[start, end])
        msg_html = render_to_string('email.html', {'snizeni_lijekovi': snizeni_lijekovi})
        self.__obavjestenje=msg_html

    def getObavjestenje(self):
        return self.__obavjestenje

class ObserverSubscriber:

    @abc.abstractmethod
    def update(self):
        pass

class ConcreteObserver(ObserverSubscriber):

    def __init__(self, publisher, user):
        self.publisher = publisher
        self.publisher.attach(self)
        self.user=user

    def setMail(self,mail):
        self.mail=mail

    def update(self):
        news=self.publisher.getObavjestenje()
        user_mail=self.mail
        from_mail=settings.EMAIL_HOST_USER
        to_mail=[user_mail]
        send_mail("% SNIZENJE %",news,from_mail,to_mail,fail_silently=False)

#klasa dodana samo radi koristenja klasa iznad koje su dio paterna
class ObavjestenjeOSnizenju:

  def __init__(self):
      self._pharmacy=SubjectPharmacy()

  def obavijesti(self):
      self._pharmacy.setObavjestenje()
      observers = []

      for prof in apps.get_model('app', 'UserProfile').objects.all():
          if prof.notification==True:
              observer = ConcreteObserver(self._pharmacy, prof.user)
              observer.setMail(prof.user.email)
              self._pharmacy.attach(observer)
              observers.append(observer)

      return self._pharmacy


