from . import views
from django.urls import path
import medicinequiry.managment.fillDatabase as fillDatabase

app_name = 'medicinequiry'

urlpatterns = [
    path('medicine_quiry/', views.medicine_quiry, name='medicine_quiry'),
    path('medicine_find/', views.medicine_find, name='medicine_find'),
    path('show_result/', views.Filter.show_result, name='show_result'),
    path('medicine_quiry/search/', views.TextBox.get_user_data, name='medicine_quiry_search'),
    path('medicine_quiry/select/', views.ComboBox.get_user_data, name='medicine_quiry_select'),
    path('medicine_quiry/char/', views.Button.get_user_data, name='medicine_quiry_char'),
    path('medication_recommendation/', views.medication_recommendation, name='medication_recommendation'),
    path('medication/', views.medication, name='medication'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('mail/', views.send_mail, name='mail'),
    path('register/', views.register, name='register'),
    path('change_password/', views.change_password, name='change_password'),
    path('filter_off/', views.filter_off, name='filter_off'),
    path('log_out/', views.log_out, name='log_out'),
    path('fillDatabase/', fillDatabase.fill_Database, name='fillDatabase'),
    path('fillDatabase/illness/', fillDatabase.fill_Database_Hastaliklar, name='fillDatabase_illness'),
    path('fillDatabase/allergy/', fillDatabase.fill_Database_Alerjiler, name='fillDatabase_allergy'),
]
