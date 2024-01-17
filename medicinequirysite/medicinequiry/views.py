from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render, redirect
from abc import ABC, abstractmethod
from .models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import smtplib
import string
import random
import json
import medicinequiry.authenticate


user = None
medicineList = []
database = []
target = ''
filter = False
recipient_email = ''
sender_email = 'nktkargo@gmail.com'
sender_email_password = 'luzs jusz gakl sabz'

class Filter(ABC):
    @abstractmethod
    def get_user_data(request):
        pass

    @abstractmethod
    def compare(self):
        pass

    def get_database(self):
        global database
        database = Ilaclar.objects.all()

    def show_result(request):
        serializemedicineList = [{
            'ilac_adi': medicine.ilac_adi,
            'firma_adi': medicine.firma_adi,
            'recete_turu': medicine.recete_turu,
            'ithal_imal': medicine.ithal_imal,
            'fiyat': medicine.fiyat,
            'yas_araligi': medicine.yas_araligi,
            'cinsiyet': medicine.cinsiyet,
            'dozu': medicine.dozu,
            'turu': medicine.turu,
            'kullanim_periyodu': medicine.kullanim_periyodu,
            'kullanimi_durumu': medicine.kullanimi_durumu,
            'nasil_kullanilir': medicine.nasil_kullanilir,
            'etkin_madde_adi': medicine.etkin_madde_adi,
        } for medicine in medicineList]
        return JsonResponse({'medicineList': serializemedicineList[:18]})

    def template_method(self):
        if len(database) == 0:
            self.get_database()
        self.compare()
        self.show_result()

class ComboBox(Filter):
    @csrf_exempt
    @require_POST
    def get_user_data(request):
        global target
        target = json.loads(request.body)['target']
        combobox = ComboBox()
        combobox.template_method()
        return HttpResponse("Başarılı")

    def compare(self):
        global medicineList, filter
        if filter:
            tempList = []
            for medicine in medicineList:
                if medicine.turu.lower() == target.lower():
                    tempList.append(medicine)
            medicineList = tempList

        if len(medicineList) == 0:
            filter = True
            for medicine in database:
                if medicine.turu.lower() == target.lower():
                    medicineList.append(medicine)

class TextBox(Filter):
    @csrf_exempt
    @require_POST
    def get_user_data(request):
        global target
        target = json.loads(request.body)['target']
        textbox = TextBox()
        textbox.template_method()
        return HttpResponse("Başarılı")

    def compare(self):
        global medicineList, filter
        if filter:
            tempList = []
            for medicine in medicineList:
                if target.lower() in medicine.ilac_adi.lower():
                    tempList.append(medicine)
            medicineList = tempList

        if len(medicineList) == 0:
            filter = True
            for medicine in database:
                if target.lower() in medicine.ilac_adi.lower():
                    medicineList.append(medicine)

class Button(Filter):
    @csrf_exempt
    @require_POST
    def get_user_data(request):
        global target
        target = json.loads(request.body)['target']
        button = Button()
        button.template_method()
        return HttpResponse("Başarılı")

    def compare(self):
        global medicineList, filter
        if filter:
            tempList = []
            for medicine in medicineList:
                if medicine.ilac_adi.lower().startswith(target.lower()):
                    tempList.append(medicine)
            medicineList = tempList

        if len(medicineList) == 0:
            filter = True
            for medicine in database:
                if medicine.ilac_adi.lower().startswith(target.lower()):
                    medicineList.append(medicine)

@csrf_exempt
@require_POST
def filter_off(request):
    global medicineList, target, filter
    medicineList = []
    target = ''
    filter = False
    return HttpResponse("Başarılı")

@csrf_exempt
def log_out(request):
    global user
    user = None
    return HttpResponse("Başarılı")

def medicine_quiry(request):
    global user
    medicineList = []
    for i in range(1, 19):
        medicineList.append(Ilaclar.objects.get(pk=i))

    return render(request, 'medicinequirysite/index.html', {'medicineList': medicineList, 'user': user})

@csrf_exempt
@require_POST
def medicine_find(request):
    name = json.loads(request.body)['ilac_adi']
    medicine = Ilaclar.objects.get(ilac_adi=name)
    serializemedicine = {
        'ilac_adi': medicine.ilac_adi,
        'firma_adi': medicine.firma_adi,
        'recete_turu': medicine.recete_turu,
        'ithal_imal': medicine.ithal_imal,
        'fiyat': medicine.fiyat,
        'yas_araligi': medicine.yas_araligi,
        'cinsiyet': medicine.cinsiyet,
        'dozu': medicine.dozu,
        'turu': medicine.turu,
        'kullanim_periyodu': medicine.kullanim_periyodu,
        'kullanimi_durumu': medicine.kullanimi_durumu,
        'nasil_kullanilir': medicine.nasil_kullanilir,
        'etkin_madde_adi': medicine.etkin_madde_adi,
    }
    return JsonResponse({'medicine': serializemedicine})

@csrf_exempt
def medication_recommendation(request):
    global user
    return render(request, 'medicinequirysite/medication_recommendation.html', {'user': user.ad})

@csrf_exempt
@require_POST
def medication(request):
    global user, database
    database = Ilaclar.objects.all()
    yas = json.loads(request.body)['yas']
    cinsiyet = json.loads(request.body)['cinsiyet']
    agri = json.loads(request.body)['agri']

    medicine = []
    for medicines in database:
        yasAraligi = medicines.yas_araligi.split('/')[0].split('-')
        if len(yasAraligi) == 2:
            minYas = int(yasAraligi[0])
            maxYas = int(yasAraligi[1])
            cinsiyetAraligi = medicines.cinsiyet
            if (int(yas) >= minYas and int(yas) <= maxYas) and (cinsiyet.lower() == cinsiyetAraligi.lower() or cinsiyetAraligi == 'Hepsi') and (agri in medicines.kullanimi_durumu):
                medicine.append(medicines)

    if len(medicine) >= 1:
        medicine = medicine[0]
        serializemedicine = {
            'ilac_adi': medicine.ilac_adi,
            'firma_adi': medicine.firma_adi,
            'recete_turu': medicine.recete_turu,
            'ithal_imal': medicine.ithal_imal,
            'fiyat': medicine.fiyat,
            'yas_araligi': medicine.yas_araligi,
            'cinsiyet': medicine.cinsiyet,
            'dozu': medicine.dozu,
            'turu': medicine.turu,
            'kullanim_periyodu': medicine.kullanim_periyodu,
            'kullanimi_durumu': medicine.kullanimi_durumu,
            'nasil_kullanilir': medicine.nasil_kullanilir,
            'etkin_madde_adi': medicine.etkin_madde_adi,
        }
        return JsonResponse({'user': user.ad, 'medicine': serializemedicine})
    elif len(medicine) == 0:
        return render(request, 'medicinequirysite/medication_recommendation.html', {'user': user.ad})

@csrf_exempt
def profile(request):
    global user
    if user != None:
        ilaclarListesi = Ilaclar.objects.all()
        alerjilerListesi = Alerji.objects.all()
        hastaliklarListesi = Hastalik.objects.all()
        if request.method == "POST":
            user.kilo = request.POST.get('kilo')
            if user.cinsiyet == 'KADIN':
                user.gebelik = request.POST.get('gebelikDurumuAl')
            user.save()
            ilaclar = request.POST.get('ilaclarlisteAl').split(', ')
            alerjiler = request.POST.get('alerjilerlisteAl').split(', ')
            hastaliklar = request.POST.get('hastaliklarlisteAl').split(', ')

            if ilaclar != None:
                for ilac in ilaclar:
                    KullaniciIlaclari(
                        kullanici = user,
                        ilac = Ilaclar.objects.get(ilac_adi=ilac)[0],
                    ).save()

            if hastaliklar != None:
                for hastalik in hastaliklar:
                    KullaniciHastaliklari(
                        kullanici = user,
                        hastalik = Hastalik.objects.get(hastalik_adi=hastalik)[0],
                    ).save()

            if alerjiler != None:
                for alerji in alerjiler:
                    KullaniciAlerjileri(
                        kullanici = user,
                        alerji = Alerji.objects.get(alerji_adi=alerji)[0],
                    ).save()

            return render(request, 'medicinequirysite/profile.html', {'user': user, 'ilaclar': ilaclarListesi, 'alerjiler': alerjilerListesi, 'hastaliklar': hastaliklarListesi})

        return render(request, 'medicinequirysite/profile.html', {'user': user, 'ilaclar': ilaclarListesi, 'alerjiler': alerjilerListesi, 'hastaliklar': hastaliklarListesi})

def login(request) :
    global user
    if request.method == 'POST':
        tc_number = request.POST.get('tcno')
        password = request.POST.get('password')
        user = medicinequiry.authenticate.verify(tcno=tc_number, password=password)
        if user is not None:
            return redirect('medicinequiry:medicine_quiry')

    return render(request, 'medicinequirysite/login.html')

def create_password(length):
    password = ''
    karakterler = string.punctuation + string.ascii_letters + string.digits

    for i in range(length):
        password += random.choice(karakterler)

    return password

@csrf_exempt
@require_POST
def send_mail(request):
    global recipient_email, user
    recipient_email = json.loads(request.body)['mail']
    tcno = json.loads(request.body)['tcno']
    password = create_password(8)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = sender_email_password

    subject = "Yeni Şifre Talebiniz"
    message = f"Şifreniz: {password}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        user = Kullanici.objects.get(tc_no=tcno)
        user.password = password
        user.save()
    except Exception as e:
        pass

    return HttpResponse('Başarılı')

@csrf_exempt
def register(request):
    global user
    if user == None:
        ilaclarListesi = Ilaclar.objects.all()
        alerjilerListesi = Alerji.objects.all()
        hastaliklarListesi = Hastalik.objects.all()
        if request.method == 'POST':
            if Kullanici.objects.filter(tc_no=request.POST.get('tcno')).count() == 0:
                Kullanici (
                    ad = request.POST.get('ad'),
                    soyad = request.POST.get('soyad'),
                    dogum_tarihi = request.POST.get('dogum_tarihi'),
                    tc_no = request.POST.get('tcno'),
                    password = request.POST.get('password'),
                    kilo = request.POST.get('kilo'),
                    kan_grubu = request.POST.get('kanGrubu'),
                    cinsiyet = request.POST.get('cinsiyet'),
                    gebelik = '' if request.POST.get('cinsiyet') == 'ERKEK' else request.POST.get('gebelik'),
                ).save()
                if request.POST.get('ilaclarlisteAl') != '':
                    ilaclar = request.POST.get('ilaclarlisteAl').split(', ')
                if request.POST.get('alerjilerlisteAl') != '':
                    alerjiler = request.POST.get('alerjilerlisteAl').split(', ')
                if request.POST.get('hastaliklarlisteAl') != '':
                    hastaliklar = request.POST.get('hastaliklarlisteAl').split(', ')
                user = Kullanici.objects.get(ad=request.POST.get('ad'))
                for ilac in ilaclar:
                    KullaniciIlaclari(
                        kullanici=user,
                        ilac=Ilaclar.objects.get(ilac_adi=ilac)[0],
                    ).save()

                for hastalik in hastaliklar:
                    KullaniciHastaliklari(
                        kullanici=user,
                        hastalik=Hastalik.objects.get(hastalik_adi=hastalik)[0],
                    ).save()

                for alerji in alerjiler:
                    KullaniciAlerjileri(
                        kullanici=user,
                        alerji=Alerji.objects.get(alerji_adi=alerji)[0],
                    ).save()

                return render(request, 'medicinequirysite/profile.html', {'user': user, 'ilaclar': ilaclarListesi, 'alerjiler': alerjilerListesi, 'hastaliklar': hastaliklarListesi})

        return render(request, 'medicinequirysite/register.html', {'ilaclar': ilaclarListesi, 'alerjiler': alerjilerListesi, 'hastaliklar': hastaliklarListesi})

@csrf_exempt
def change_password(request):
    if user != None:
        if request.method == 'POST':
            old_password = request.POST.get('oldPassword')
            new_password = request.POST.get('newPassword')
            if user.password == old_password:
                user.password = new_password
                user.save()
                return redirect('medicinequiry:profile')
        return render(request, 'medicinequirysite/change_password.html')
