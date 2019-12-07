from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
# Create your views here.
from project.forms import SignUpForm, UsrEditForm, CarRentChangeForm
from project.models import UserProfile, Language, Car, CarsNames


def SignUpView(request):
    sgform = SignUpForm()
    if request.POST:
        sgform = SignUpForm(request.POST)
        if sgform.is_valid():
            email = sgform.cleaned_data['email']
            password1 = sgform.cleaned_data['password1']
            password2 =sgform.cleaned_data['password2']
            name = sgform.cleaned_data['name']
            lang = sgform.cleaned_data['lang']
            user = User.objects.create(username=name, email=email, is_active=True, date_joined = timezone.now())
            user.save()
            user.set_password(password1)
            user.save()
            userprofile = UserProfile.objects.create(user=user, language=lang)
            userprofile.save()
    return render(request,'any/signup.html', {'signupform':sgform,})

@login_required
def AboutView(request):
    lang = get_object_or_404(UserProfile, user=request.user).language
    if request.POST:
        UsEditForm = UsrEditForm(request.POST)
        if UsEditForm.is_valid():
            usr = get_object_or_404(User, username=request.user.username)
            usr.username = UsEditForm.cleaned_data['username']
            usr.email = UsEditForm.cleaned_data['email']
            usr.save()
            lng = get_object_or_404(Language, lang=UsEditForm.cleaned_data['lang'] )
            usrporf = get_object_or_404(UserProfile, user=usr)
            usrporf.language = lng
            usrporf.save()
            UsEditForm = UsrEditForm(
                initial={'username': usr.username, 'email': usr.email, 'lang': lng, })
    else:
        UsEditForm = UsrEditForm(initial={'username': request.user.username, 'email': request.user.email, 'lang': lang,})
    return render(request,'any/about.html', {'lang':lang, 'UsEditForm':UsEditForm})

@login_required
def AllCarsView(request):
    all_lng = Language.objects.all()
    all_cars = Car.objects.filter(user=request.user)
    if request.POST:
        carForm = request.POST
        newCar = Car.objects.create(user=request.user, date_of_manufacture=carForm['year'])
        newCar.save()
        for ln in Language.objects.all():
            crName = CarsNames.objects.create(lang=ln, car=newCar, name=carForm[""+str(ln.pk)+""])
            crName.save()
            send_mail('From rent car sait', 'You have successfully added a car', 'hamster197@mail.ru',
                      [""+request.user.email+""], fail_silently=False,)
        return redirect('project:Cars_index')
    return render(request,'cars/index.html',{'tall_lng':all_lng, 'tall_cars':all_cars, })

@login_required
def ChangeRentView(request, idd):
    car = get_object_or_404(Car, pk=idd)
    CRForm = CarRentChangeForm(instance=car)
    if request.POST:
        CRForm = CarRentChangeForm(request.POST, instance=car)
        if CRForm.is_valid:
            CRForm.save()
            return redirect('project:Cars_index')
    return render(request, 'cars/change_rent.html', {'car':car, 'CRForm':CRForm,})