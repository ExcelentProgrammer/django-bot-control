from django.urls import path

from control.views import HomePage, sendMessagePage, taskStatusApi

app_name = "adm"

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("task/<int:pk>/", taskStatusApi.as_view(), name="task"),
    path("send/message/", sendMessagePage.as_view(), name="send-message"),
]
