from django.contrib import admin
from django.urls import path, include

"""
djoser urls:
/jwt/create/ (JSON Web Token Authentication) -create tokens. data format is username and password
/jwt/refresh/ (JSON Web Token Authentication)
/jwt/verify/ (JSON Web Token Authentication)
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls.jwt')),
    path('user/', include('users.urls'))
]
