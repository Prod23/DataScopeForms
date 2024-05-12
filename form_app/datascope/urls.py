from django.urls import path
from . import views

urlpatterns = [
    path("submit-form/<slug:username>", views.submit_form, name="submit-form"),
    path("submit-form-admin/<slug:username>",
         views.submit_form_admin, name="submit-form-admin"),
    path("submit-form-course/<slug:username>",
         views.submit_form_course, name="submit-form-course"),
    path("submit-form-course-admin/<slug:username>",
         views.submit_form_course_admin, name="submit-form-course-admin"),
    path("", views.signup, name="register"),
    path("login", views.signin, name="signin"),
    path("success", views.success_page, name="success_page_url"),
    path('generate-data', views.generate_data, name='generate_data'),
    path('generate-R1', views.generate_R1, name="generate_R1"),
    path('generate-R2', views.generate_R2, name="generate_R2"),
    path('generate-R3', views.generate_R3, name="generate_R3"),
    path('login-admin', views.signin_admin, name="signin_admin")
]
