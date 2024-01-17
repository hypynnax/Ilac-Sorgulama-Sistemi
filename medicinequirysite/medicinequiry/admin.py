from django.contrib import admin
from .models import *


class KullaniciAdmin(admin.ModelAdmin):
    list_display = ('ad', 'soyad', 'dogum_tarihi', 'kilo', 'kan_grubu', 'cinsiyet', 'gebelik')
    list_filter = ('dogum_tarihi', 'kan_grubu', 'cinsiyet', 'gebelik')
    search_fields = ('ad', 'soyad')

admin.site.register(Kullanici, KullaniciAdmin)


class IlaclarAdmin(admin.ModelAdmin):
    list_display = ('ilac_adi', 'firma_adi', 'recete_turu', 'ithal_imal', 'fiyat', 'yas_araligi', 'cinsiyet', 'dozu', 'turu', 'kullanim_periyodu')
    list_filter = ('ilac_adi', 'firma_adi', 'recete_turu', 'ithal_imal', 'fiyat', 'yas_araligi', 'cinsiyet', 'dozu', 'turu', 'kullanim_periyodu')
    search_fields = ('ilac_adi', 'firma_adi', 'ithal_imal', 'turu')

admin.site.register(Ilaclar, IlaclarAdmin)


class AlerjiAdmin(admin.ModelAdmin):
    list_display = ('alerji_adi',)
    search_fields = ('alerji_adi',)

admin.site.register(Alerji, AlerjiAdmin)


class HastalikAdmin(admin.ModelAdmin):
    list_display = ('hastalik_adi',)
    search_fields = ('hastalik_adi',)

admin.site.register(Hastalik, HastalikAdmin)
