from django.urls import path
from fnm.cards.apis.apis import (
    ApproveJobCardApi,
    EscalateJobCardApi,
    AssignJobCardApi,
    CompleteJobCardApi,
    CloseJobCardApi,
    CreateJobCardApi,

)

urlpatterns = [
    path('create/', CreateJobCardApi.as_view(), name='create_job_card'),
    path('<int:pk>/approve/', ApproveJobCardApi.as_view(), name='approve_job_card'),
    path('<int:pk>/escalate/', EscalateJobCardApi.as_view(), name='escalate_job_card'),
    path('jobcards/<int:pk>/assign/', AssignJobCardApi.as_view(), name='assign_job_card'),
    path('jobcards/<int:pk>/complete/', CompleteJobCardApi.as_view(), name='complete_job_card'),
    path('jobcards/<int:pk>/close/', CloseJobCardApi.as_view(), name='close_job_card'),
]
