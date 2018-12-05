from django.conf.urls import url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'userProfiles', views.UserProfileSet)

urlpatterns = [
    path('four/', views.Get4UserProfiles.as_view())
] + router.urls
