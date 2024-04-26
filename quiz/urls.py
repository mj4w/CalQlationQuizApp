from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    #home
    path('',views.home, name='home'),
    # path('register/',views.register_view, name='register'),
    # path('login/',views.login_view, name='login'),
    path('student-home/',views.student_home, name='student-home'),
    path('professor-home/',views.professor_home, name='professor-home'),

    # practice quiz student
    path('solo-students/',views.student_solo, name='solo-student'),
    path('group-students/',views.student_group, name='group-student'),
    #practice question
    path('practice-question/solo/<int:practice_mode_instance_id>/', views.practice_question_solo, name='practice'),
    # original 
    path('practice-question/soloD/<int:practice_mode_instance_id>/', views.practice_question_solo_default, name='practice-default-solo'),
    #practice-question group
    path('practice-question/group/<int:practice_mode_instance_id>/', views.practice_question_group, name='practice-group'),
    # original 
    path('practice-question/groupD/<int:practice_mode_instance_id>/', views.practice_question_group_default, name='practice-default-group'),
    # prof side
    path('create-quiz',views.create_quiz, name='create-quiz'),
    path('actual-quiz/<int:id>/', views.actual_quiz, name='actual-quiz'),
    path('link-quiz/<int:id>/', views.link_actual_quiz, name='link-actual-quiz'),
    # original 
    path('quiz-form/<int:id>/', views.quiz_form_prof, name='quiz-form'),
    path('get-link/<int:id>/', views.done_create_quiz, name='get-link'),
    #result 
    path('result-practice/<int:practice_mode_instance_id>/', views.resultP, name='result-practice'),
    path('solo-result/<int:practice_mode_instance_id>/', views.solo_result, name='solo-result'),
    path('result-actual/<int:id>/',views.result_actual_quiz, name='result-actual'),
    path('result-all',views.result_all_actual, name='result-all'),
    
    
    #password reset
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    
    # quiz not available template
    path('quiz-not-available/<int:id>/',views.not_available, name='quiz-not-available'),
    
    path('about-us/',views.about_us, name='about-us'),
    path('contact-us/',views.contact_us, name='contact-us'),
    
    path('log-out/',views.log_out, name='logout'),
    
    
    path('submit-solo-answers/', views.submit_solo_answers, name='submit-solo'),
    path('submit-group-answers/', views.submit_group_answers, name='submit-group'),
    path('submit-quiz-answers/', views.submit_prof_answers, name="submit-prof"),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)