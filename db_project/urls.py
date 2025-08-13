"""
URL configuration for db_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import home1
from notice.views import notice
from result.views import result_view
from admit_card.views import download_admit_list
from account.views import signuppage, loginpage , homepage,logoutPage,user_info,user_login,student_dashboard,delete
from admit_card.views import download_admit, generate_pdf
from Admin.views import admin_login, custom_admin_dashboard, manage_users, delete_user_admin,manage_results, delete_result, manage_notices, delete_notice, edit_notice,edit_result,manage_quiz_questions,delete_question,add_quiz
from faq.views import faq1
from contact.views import contact1
from Test.views import start_quiz, submit_quiz, quiz_result
from Study_Resources.views import resource_page
from Admin.views import manage_resource, delete_resource
from Performance_Analysis.views import performance_home, performance_result_view
from ChatBot.views import index,chat
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home1),
    path('index/',home1,name='index'),
    path('notice/',notice, name='notice'),
    path('result/',result_view,name='result'),
    path('admit/',download_admit_list,name='admit'),
    path('login/', loginpage, name='login'),   
    path('signup/', signuppage, name='signup'),  
    path('home/',homepage, name='home'),
    path('logout/',logoutPage,name='logout'),
    path("download_admit/", download_admit, name="download_admit"),
    path("generate-pdf/<str:reg_no>/", generate_pdf, name="generate_pdf"),
    path('user_info/',user_info, name="user_info"),
    path('faq/',faq1,name='faq'),
    path('contact-us/',contact1,name='contact'),
    path('admin_login/', admin_login, name='admin_login'),
    path('login/', user_login, name='login'),
    path('stu_dash/',student_dashboard,name='student_dashboard'),
    path('custom-admin/', custom_admin_dashboard, name='custom_admin_dashboard'),
    path('manage-users/', manage_users, name='manage_users'),
    path('delete-user/<int:user_id>/', delete_user_admin, name='delete_user_admin'),
    # path('delete/',delete,name='delete')
    path('manage-results/', manage_results, name='manage_results'),
    path('delete-result/<int:result_id>/', delete_result, name='delete_result'),
    path('edit-result/<int:result_id>/', edit_result, name='edit_result'),
 

    path('manage-notices/', manage_notices, name='manage_notices'),
    path('delete-notice/<int:notice_id>/', delete_notice, name='delete_notice'),
    path('edit-notice/<int:notice_id>/', edit_notice, name='edit_notice'),

    path('quiz/start/', start_quiz, name='start_quiz'),
    path('quiz/submit/', submit_quiz, name='submit_quiz'),
    path('quiz/result/', quiz_result, name='quiz_result'),

    path('manage-quiz-questions/', manage_quiz_questions, name='manage_quiz_questions'),
    path('delete-question/<int:question_id>/', delete_question, name='delete_question'),
    path('add-quiz/', add_quiz, name='add_quiz'),



    path('resources/', resource_page, name='resource_page'),

    path('manage-resource/', manage_resource, name='manage_resource'),
    path('delete-resource/<int:resource_id>/', delete_resource, name='delete_resource'),

    path('performance-home/',performance_home,name='performance_home'),
    path('performance-result/', performance_result_view,name='performance_result'),


    path('chat-home', index, name="chatbot_home"),
    path('chat/', chat, name="chatbot_chat"),

 


]
