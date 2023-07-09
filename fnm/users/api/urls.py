from django.urls import include, path

# from .apis import UserResource


from .auth import (
    UserJwtLoginApi,
    UserJwtLogoutApi,
    UserSessionLoginApi,
    UserSessionLogoutApi,
    UserCreateAPIView,
)

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name="create-user"),
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
        "auth/",
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
    # path('me/', UserResource.as_view(), name='user-resource'),
    # path('me/update/', UpdateProfileAPI.as_view(), name='profile'),
    # path('list/', UserListApi.as_view(), name='users-list'),
]
