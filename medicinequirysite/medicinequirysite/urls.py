from django.contrib import admin
from django.urls import path, include

import medicinequiry.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('medicinequiry.urls')),
    path('', medicinequiry.views.medicine_quiry),
]
