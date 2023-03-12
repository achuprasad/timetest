from django.urls import path
from . import views

urlpatterns = [
        path('',views.Register.as_view(),name='register'),
        path('login',views.Login.as_view(),name='login'),
        path('logout',views.Logout.as_view(), name='logout'),
        path('student',views.StudentPageView.as_view(), name='student_page'),
        path('staff', views.StaffPageView.as_view(), name='staff_page'),
        path('admin',views. AdminPageView.as_view(), name='admin_page'),
        path('editor',views.EditorPageView.as_view(), name='editor_page'),

]