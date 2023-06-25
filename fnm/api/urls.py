
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", include("fnm.users.api.urls"), name="users"),
    path("request/", include("fnm.request.urls"), name="requests")

   # path("obtain-token/", obtain_auth_token),
]
