from django.urls import path

from .api.apis import ImprestRequestAPI, \
    ImprestReqActionAPI, ImprestRequestListAPI, \
    LeaveRequestAPI, LeaveRequestActionAPI,\
    LeaveRequestsListAPI, LeaveRequestUpdateAPI

urlpatterns = [
    path("imprest/", ImprestRequestAPI.as_view(), name="imprests"),
    path("imprest/list/", ImprestRequestListAPI.as_view(), name="imprests-list"),
    path("imprest/action/<int:imprest_request_id>/", ImprestReqActionAPI.as_view(), name="action"),
    path("leave/", LeaveRequestAPI.as_view(), name="leave-request"),
    path("leave/list/", LeaveRequestsListAPI.as_view(), name="leave-request-list"),
    path('leave/action/<int:leave_request_id>/', LeaveRequestActionAPI.as_view(), name='leave-request-action'),
    path('leave/update/<int:leave_request_id>/', LeaveRequestUpdateAPI.as_view(), name='leave-request-update'),
]
