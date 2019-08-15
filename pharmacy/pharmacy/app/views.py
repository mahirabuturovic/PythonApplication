from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Lijek,Clanak
from .forms import UserLoginForm,ClanakForma
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import ExtendedUserForm,ProfileForm
from django.apps import apps
from . import Factory
from .Proxy import Proxy, RealSubject
import datetime
from django.contrib.auth import authenticate,login

def kreiraj_clanak(request):

    if request.method=="POST":
        forma=ClanakForma(request.POST)
        if forma.is_valid():
            clanak=Clanak(naslov=forma.cleaned_data['naslov'],body=forma.cleaned_data['body'],slug=forma.cleaned_data['slug'])
            clanak.save()
    else:
        forma=ClanakForma()
    return render(request,'kreiraj-clanak.html',{'forma':forma})

def odjava(request):
    logout(request)
    return redirect('registracija')

def clanak_detalji(request,slug):
    model_clanak = apps.get_model('app', 'Clanak')
    clanak=model_clanak.objects.get(slug=slug)
    user=request.user
    return render(request,'clanak.html',{'clanak':clanak,'user':user})

def prikazi_blog(request):
    model_clanak = apps.get_model('app', 'Clanak')
    blog=model_clanak.objects.all().order_by('datum')
    return render(request,'blog.html',{'blog':blog})


def obrisi_iz_korpice(request,slug):
    model_lijek = apps.get_model('app', 'Lijek')
    lijek=model_lijek.objects.get(slug=slug)
    model_narudzba_lijek = apps.get_model('app', 'LijekNarudzba')
    model_narudzba_lijek.objects.filter(lijek=lijek).delete()
    return redirect('prikazi')
# Create your views here.
@login_required(login_url='/login')
def pretraga(request):
    storage=messages.get_messages(request)
    return render(request,'pretraga.html',{'messages':storage})

def prikazi_korpicu(request):
    # get order for the correct user

    try:
        model_order = apps.get_model('app', 'Faktura')
        order = model_order.objects.get(owner=request.user)
        items = order.lijekovi.all()
        suma=0
        for i in items:
            suma+=i.lijek.cijena*i.quantity
        return render(request,'mojakorpica.html',{'items':items,'suma':suma})

    except ObjectDoesNotExist:
        return render(request, 'mojakorpica.html', {'items': ""})


def opis(request,slug):
    model_lijek=apps.get_model('app','Lijek')
    lijek=model_lijek.objects.get(slug=slug)
    opis=lijek.opis
    return render(request,'opis.html',{'opis':opis})
def prikazi(request):
    namjena=request.POST['meni']
    lijekovi=Factory.ConcreteCreator(namjena).lijek.prikazi()
    Snizenje=apps.get_model('app','Snizenje')
    start = datetime.date.today()
    year=datetime.date.today().year
    end=datetime.date(year,12,31)
    snizeni_lijekovi=Snizenje.objects.filter(datum__range=[start,end])
    context={
        'lijekovi':lijekovi,
        'snizeni_lijekovi':snizeni_lijekovi
    }
    return render(request,'prikaz.html',context)

def dodaj_u_korpicu(request,slug):
    lijek=get_object_or_404(Lijek,slug=slug)#rror
    if (Proxy(RealSubject("")).provjera(lijek, request.user) == True):
           messages.info(request, "Lijek " + lijek.naziv + " je dodan u vasu korpicu.")
           return redirect('prikazi')
    else:
        return render(request, 'recept.html', {'slug': slug})

def provjera(request,slug):
    model_lijek=apps.get_model('app','Lijek')
    lijek=model_lijek.objects.get(slug=slug)
    kod=request.POST.get('kod')
    if(Proxy(RealSubject(kod)).provjera(lijek,request.user)==False):
        return render(request, 'upozorenje.html')
    else:
        messages.info(request, "Lijek " + lijek.naziv + " je dodan u vasu korpicu.")
        return redirect('prikazi')

def login_view(request):
    form=UserLoginForm(request.POST or None)
    #valid zove clean
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("prikazi")
    return render(request,"form.html",{"form":form})

def registracija(request):
    if request.method == 'POST':
        form = ExtendedUserForm(request.POST)
        profile_form=ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user=form.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request,user)
            return redirect('prikazi')
    else:
        form = ExtendedUserForm()
        profile_form=ProfileForm()
    return render(request, 'registracija.html',context={'form':form,'profile_form':profile_form})
