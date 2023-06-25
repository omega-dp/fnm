from django.urls import include, path

from .apis import UserProfileMeAPI, UserMeApi

from .auth import (
    UserJwtLoginApi,
    UserJwtLogoutApi,
    UserSessionLoginApi,
    UserSessionLogoutApi,
)

urlpatterns = [
    path(
        "auth/session/",
        include(
            (
                [
                    path("login/", UserSessionLoginApi.as_view(), name="login"),
                    path("logout/", UserSessionLogoutApi.as_view(), name="logout"),
                ],
                "session",
            )
        ),
    ),
    path(
        "jwt/",
        include(
            (
                [
                    path("login/", UserJwtLoginApi.as_view(), name="login"),
                    path("logout/", UserJwtLogoutApi.as_view(), name="logout"),
                ],
                "jwt",
            )
        ),
    ),
]

urlpatterns += [
    # Other URLs
    path("me/", UserMeApi.as_view(), name="me"),
    path('me/profile/', UserProfileMeAPI.as_view(), name='profile'),
]
