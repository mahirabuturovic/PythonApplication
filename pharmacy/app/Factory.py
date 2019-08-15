from django.apps import apps
import abc

class Creator:

    def __init__(self,tip):
        self.lijek=self.factory_method(tip)

    @abc.abstractmethod
    def factory_method(self,tip):
        pass

    def some_operation(self):
         self.lijek.prikazi()

class ConcreteCreator(Creator):

    def factory_method(self,tip):
        if (tip == 'stres'):
            return ConcreteProduct1Antidepresivi()
        elif (tip == 'rak'):
            return ConcreteProduct7Citostatici()
        elif (tip == 'bolovi'):
            return ConcreteProduct4Analgetici()
        elif (tip == 'dijabetes'):
            return  ConcreteProduct6Inzulini()
        elif (tip == 'nedostatak vitamina'):
            return ConcreteProduct5Vitamini()
        elif (tip == 'prehlada'):
            return ConcreteProduct2Antipiretici()
        elif (tip == 'upala'):
            return ConcreteProduct3Antbiotici()

class Product:
   @abc.abstractmethod
   def prikazi(self):
       pass

class ConcreteProduct1Antidepresivi(Product):
       def prikazi(self):
           return apps.get_model('app','Lijek').objects.filter(namjena='stres')

class ConcreteProduct2Antipiretici(Product):
       def prikazi(self):
           return apps.get_model('app', 'Lijek').objects.filter(namjena='prehlada')

class ConcreteProduct3Antbiotici(Product):
       def prikazi(self):
           return apps.get_model('app', 'Lijek').objects.filter(namjena='upala')

class ConcreteProduct4Analgetici(Product):
       def prikazi(self):
           return apps.get_model('app', 'Lijek').objects.filter(namjena='bol')

class ConcreteProduct5Vitamini(Product):
        def prikazi(self):
           return apps.get_model('app', 'Lijek').objects.filter(namjena='otpornost')

class ConcreteProduct6Inzulini(Product):
        def prikazi(self):
          return apps.get_model('app', 'Lijek').objects.filter(namjena='dijabetes')


class ConcreteProduct7Citostatici(Product):
        def prikazi(self):
            return apps.get_model('app', 'Lijek').objects.filter(namjena='rak')
