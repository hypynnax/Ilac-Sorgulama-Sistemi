from django.db import models

class Kullanici(models.Model):
    ad = models.CharField(max_length=255)
    soyad = models.CharField(max_length=255)
    dogum_tarihi = models.DateField()
    tc_no = models.CharField(max_length=20)
    password = models.CharField(max_length=8)
    kilo = models.FloatField()
    kan_grubu = models.CharField(max_length=255)
    cinsiyet = models.CharField(max_length=255)
    gebelik = models.CharField(max_length=255)

class Hastalik(models.Model):
    hastalik_adi = models.CharField(max_length=255)

class KullaniciHastaliklari(models.Model):
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)
    hastalik = models.ForeignKey(Hastalik, on_delete=models.CASCADE)

class Alerji(models.Model):
    alerji_adi = models.CharField(max_length=255)

class KullaniciAlerjileri(models.Model):
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)
    alerji = models.ForeignKey(Alerji, on_delete=models.CASCADE)

class Ilaclar(models.Model):
    ilac_adi = models.CharField(max_length=255)
    firma_adi = models.CharField(max_length=255)
    recete_turu = models.CharField(max_length=255)
    ithal_imal = models.CharField(max_length=255)
    fiyat = models.CharField(max_length=255)
    yas_araligi = models.CharField(max_length=255)
    cinsiyet = models.CharField(max_length=255)
    dozu = models.CharField(max_length=255)
    turu = models.CharField(max_length=255)
    kullanim_periyodu = models.CharField(max_length=255)
    kullanimi_durumu = models.TextField(max_length=255)
    nasil_kullanilir = models.TextField(max_length=255)
    etkin_madde_adi = models.CharField(max_length=255)

class KullaniciIlaclari(models.Model):
    kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)
    ilac = models.ForeignKey(Ilaclar, on_delete=models.CASCADE)
