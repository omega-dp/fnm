from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("users/", include("fnm.users.api.urls"), name="users"),
    path("cards/", include("fnm.cards.urls"), name="cards"),
    path("req/", include("fnm.request.urls"), name="requests")

    # path("obtain-token/", obtain_auth_token),
]
