from django.urls import path

from sponsors.views import HomePage, DeletePage, CreatePage, UpdatePage

app_name = "sponsors"

urlpatterns = [
    path("list/", HomePage.as_view(), name="list"),
    path("delete/<int:pk>/", DeletePage.as_view(), name="delete"),
    path("create/", CreatePage.as_view(), name="create"),
    path("edit/<int:pk>/", UpdatePage.as_view(), name="edit"),
]
