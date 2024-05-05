from django.urls import path
from . import views
from .views import AccountListView, UploadCSVView


urlpatterns = [
    path('accounts/', AccountListView.as_view(), name='accounts-list'),
    path('consumers/', AccountListView.as_view(), name='accounts-list'),
    path('upload-csv/', UploadCSVView.as_view(), name='upload-csv'),

]