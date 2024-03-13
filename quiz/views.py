from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import LoginForm, RegisterForm, PracticeModeForm,SoloPracticeModeForm
from .models import PracticeMode,Question,ResultPractice,QuizSetting,ActualQuiz, ResultActual,SoloPracticeMode,SoloQuestion,SoloResultPractice
from django.utils import timezone
from django.http import HttpResponse
import random
from datetime import datetime,timedelta
import pytz
from django.middleware.csrf import CsrfViewMiddleware
from django.template.context_processors import csrf
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from operator import itemgetter
from itertools import groupby
from django.views.decorators.csrf import csrf_exempt

# professor & student
# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request,user)
#             return redirect('login')
        
#     else:
#         form = RegisterForm()
        
#     return render(request,'accounts/register.html',{'form':form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST, data=request.POST)
#         if form.is_valid():
#             user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
#             if user is not None:
#                 login(request,user)
#                 if 'bulsu.edu.ph' in user.email and any(char.isdigit() for char in user.email):
#                     return redirect('student-home')
#                 elif 'bulsu.edu.ph' in user.email:
#                     return redirect('professor-home')
#                 else:
#                     messages.error(request,'Your email is not from BULSU')
#                     return redirect('home')
#     else:
#         form = LoginForm()
        
#     return render(request,'accounts/login.html',{'form':form})
@csrf_exempt
def home(request):
    if "register" in request.POST:
        try:
            if request.method == 'POST':
                form_register = RegisterForm(request.POST or None)
                if form_register.is_valid():
                    user = form_register.save()
                    login(request, user)
                    messages.success(request, 'You have been registered! Login Now!')
                    return redirect('home')
                else:
                    for field, errors in form_register.errors.items():
                        for error in errors:
                            messages.error(request, f"Registration Error: {field.capitalize()} - {error}")
        except SuspiciousOperation as e:
            messages.error(request, f'CSRF Verification Failed: {str(e)}')
            return redirect('home')
    elif "login" in request.POST:
        try: 
            if request.method == 'POST':
                form_login = LoginForm(request.POST or None, data=request.POST)
                if form_login.is_valid():
                    user = authenticate(request, username=form_login.cleaned_data['username'], password=form_login.cleaned_data['password'])
                    if user is not None:
                        login(request, user)
                        if 'bulsu.edu.ph' in user.email and any(char.isdigit() for char in user.email):
                            messages.success(request,'You have successfully logged in')
                            return redirect('student-home')
                        elif 'bulsu.edu.ph' in user.email:
                            messages.success(request,'You have successfully logged in')
                            return redirect('professor-home')
                        messages.error(request, 'Login Error: Your Email is not a bulsu acc.')
                        return redirect('home')
                else:
                    # Form is not valid
                    messages.error(request, 'Login Error: Please enter valid credentials.')
            else:
                # The request method is not POST
                messages.error(request, 'Login Error: Invalid request method.')
        except SuspiciousOperation as e:
            messages.error(request, f'CSRF Verification Failed: {str(e)}')
            return redirect('home')
    form_register = RegisterForm()
    form_login = LoginForm()
    return render(request, 'home.html', {'form_login': form_login, 'form_register': form_register})

@login_required(login_url='home')
def student_home(request):
    return render(request,'role/student_home.html')

@login_required(login_url='home')
def professor_home(request):
    user_email = request.user.email
    user_name = user_email.split("@")[0]
    return render(request,'role/professor_home.html',{'user_name':user_name})

# practice quiz student

@csrf_exempt
@login_required(login_url='home')
def student_solo(request):
    if request.method == 'POST':
        form = SoloPracticeModeForm(request.POST)
        if form.is_valid():
            practice_mode_instance = SoloPracticeMode(
                user=request.user,
                difficulty=form.cleaned_data['difficulty'],
                num_questions=form.cleaned_data['num_questions']
            )
            
            # Associate questions based on the selected topic and difficulty
            questions = SoloQuestion.objects.filter(
                difficulty=form.cleaned_data['difficulty'])[:form.cleaned_data['num_questions']]
            
            practice_mode_instance.save()
            practice_mode_instance.questions.set(questions)

            # Pass the practice_mode_instance to the 'practice' view
            return redirect('practice', practice_mode_instance_id=practice_mode_instance.id)
    else:
        form = SoloPracticeModeForm()
    return render(request, 'practiceMode/student_solo.html', {'form': form})
@csrf_exempt
@login_required(login_url='home')
def student_group(request):
    if request.method == 'POST':
        form = PracticeModeForm(request.POST)
        if form.is_valid():
            practice_mode_instance = PracticeMode(
                user=request.user,
                topic=form.cleaned_data['topic'],
                num_questions=form.cleaned_data['num_questions']
            )
            
            # Associate questions based on the selected topic and difficulty
            questions = Question.objects.filter(
                topic=form.cleaned_data['topic'])[:form.cleaned_data['num_questions']]
            
            practice_mode_instance.save()
            practice_mode_instance.questions.set(questions)

            # Pass the practice_mode_instance to the 'practice' view
            return redirect('practice-group', practice_mode_instance_id=practice_mode_instance.id)
    else:
        form = PracticeModeForm()
        
    return render(request,'practiceMode/student_group.html', {'form': form})

@csrf_exempt
@login_required(login_url='home')
def practice_question_solo(request, practice_mode_instance_id):
    practice_mode_instance = SoloPracticeMode.objects.get(id=practice_mode_instance_id)
    questions = list(practice_mode_instance.questions.all())
    random.shuffle(questions)
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer_key = f'user_answer_{question.id}'
            user_answer = request.POST.get(user_answer_key,'')
            # Check if the user's answer is correct
            if user_answer == question.answer:
                score += 1
            result_p = SoloResultPractice.objects.create(
                user = request.user,
                topic_show = practice_mode_instance, 
                num_question_show=practice_mode_instance.num_questions,
                question = question,
                score = 1 if user_answer == question.answer else 0,
                user_answer=user_answer,
            )
        return redirect('solo-result',practice_mode_instance_id=practice_mode_instance_id)
    return render(request, 'practiceQuestion/question.html', {'practice_mode_instance': practice_mode_instance, 'shuffled_questions': questions})

@login_required(login_url='home')
def solo_result(request, practice_mode_instance_id):
    practice_mode_instance = SoloPracticeMode.objects.get(id=practice_mode_instance_id)

    # Get distinct questions related to the practice_mode_instance_id
    questions = SoloQuestion.objects.filter(soloresultpractice__user=request.user, soloresultpractice__topic_show=practice_mode_instance_id).distinct()
    results_details = []
    total_score = 0
    for question in questions:
        try:
            latest_result = SoloResultPractice.objects.filter(
                user=request.user,
                question=question,
                topic_show=practice_mode_instance_id,
            ).latest('id')
        except SoloResultPractice.DoesNotExist:
            continue

        result_details = {
            'question_text': question.question_text,
            'question_formula': question.question_formula,
            'score': latest_result.score,
            'solution':question.solution_here,
            'user_answer':latest_result.user_answer,
            'correct_answer':latest_result.question.answer
            
        }
        total_score += latest_result.score
        results_details.append(result_details)
        print(result_details['solution'])
   
    return render(request, 'results/solo_result.html', {'results_details': results_details, 'total_score': total_score})
@csrf_exempt
@login_required(login_url='home')
def practice_question_group(request,practice_mode_instance_id):
    practice_mode_instance = PracticeMode.objects.get(id=practice_mode_instance_id)
    time_limit = practice_mode_instance.num_questions * 30
    questions = list(practice_mode_instance.questions.all())
    random.shuffle(questions)
    if request.method == 'POST':
        score = 0
        result_sum = 0
        for question in questions:
            user_answer_key = f'user_answer_{question.id}'
            user_answer = request.POST.get(user_answer_key,'')
            # Check if the user's answer is correct
            if user_answer == question.answer:
                score += 1
            result_p = ResultPractice.objects.create(
                user = request.user,
                topic_show = practice_mode_instance,
                num_question_show=practice_mode_instance.num_questions,
                question = question,
                score = 1 if user_answer == question.answer else 0,
                user_answer=user_answer,
            )
            result_sum += result_p.score
            players = ResultPractice.objects.filter(topic_show=practice_mode_instance).values('user__email').distinct()
        print(players)
        print(result_sum)
        return redirect('result-practice',practice_mode_instance_id=practice_mode_instance_id)
    return render(request, 'practiceQuestion/group_question.html', {'practice_mode_instance': practice_mode_instance, 'shuffled_questions': questions,'time_limit': time_limit})

@login_required(login_url='home')
def resultP(request, practice_mode_instance_id):
    practice_mode_instance = PracticeMode.objects.get(id=practice_mode_instance_id)

    # Get distinct questions related to the practice_mode_instance_id
    questions = Question.objects.filter(resultpractice__user=request.user, resultpractice__topic_show=practice_mode_instance_id).distinct()
    results_details = []
    total_score = 0
    for question in questions:
        try:
            latest_result = ResultPractice.objects.filter(
                user=request.user,
                question=question,
                topic_show=practice_mode_instance_id,
            ).latest('id')
        except ResultPractice.DoesNotExist:
            continue

        result_details = {
            'question_text': question.question_text,
            'question_formula': question.question_formula,
            'score': latest_result.score,
            'solution':question.solution_here,
            'user_answer':latest_result.user_answer,
            'correct_answer':latest_result.question.answer
            
        }
        total_score += latest_result.score
        results_details.append(result_details)
    
    # all participants
    today = timezone.now().date()
    result_group = (
        ResultPractice.objects
        .filter(date=today)
        .values('user', 'user__email')  # Include 'user__email' to fetch the email field
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )
    return render(request, 'results/result_practice.html', {'results_details': results_details, 'total_score': total_score,'result_group': result_group})


# prof side
@csrf_exempt
@login_required(login_url='home')
def create_quiz(request):
    if request.method == 'POST':
        user = request.user
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        show_correct_answer = request.POST.get('show_correct_answer')
        show_solution = request.POST.get('show_solution')
        question_timer = request.POST.get('question_timer')
        section = request.POST.get('section')
        
        save_quiz_setting = QuizSetting.objects.create(
            user=user,
            select_data=date,
            start_time=start_time,
            end_time=end_time,
            show_correct_answer=show_correct_answer,
            show_solution=show_solution,
            question_timer=question_timer,
            section = section,
        )
        save_quiz_setting.save()
        
        return redirect('actual-quiz', id=save_quiz_setting.id)
    
    return render(request, 'profPage/create_quiz.html')

@csrf_exempt
@login_required(login_url='home')
def actual_quiz(request, id):
    quiz_setting = QuizSetting.objects.get(pk=id)

    if request.method == 'POST':
        # Assuming you get the form data from the request
        add_text = request.POST.get('add_text')
        add_equation = request.POST.get('add_equation')
        upload_photo = request.FILES.get('upload_photo')
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        answer = request.POST.get('answer')
        solution = request.POST.get('solution')

        # Create ActualQuiz instance associated with the QuizSetting
        actual_quiz = ActualQuiz.objects.create(
            user=request.user,
            add_text=add_text,
            add_equation=add_equation,
            upload_photo=upload_photo,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            answer=answer,
            quiz_setting=quiz_setting,
            add_solution_here = solution,
        )
        actual_quiz.save()

    return render(request, 'profPage/actual_quiz.html', {'quiz_setting': quiz_setting})

@login_required(login_url='home')
def done_create_quiz(request,id):
    quiz_setting = QuizSetting.objects.get(pk=id)
    answers = ActualQuiz.objects.filter(quiz_setting=quiz_setting)
    return render(request,'profPage/done_create_quiz.html', {'quiz_setting': quiz_setting, 'answers': answers})

@login_required(login_url='home')
def link_actual_quiz(request, id):
    quiz_setting = QuizSetting.objects.get(pk=id)

    # Get the current datetime with timezone information
    current_datetime = timezone.localtime(timezone.now(), pytz.timezone('Asia/Manila'))

    # Combine the date and time, and make them timezone aware
    quiz_start_datetime = timezone.make_aware(
        datetime.combine(quiz_setting.select_data, quiz_setting.start_time),
        timezone.get_current_timezone()
    )
    quiz_end_datetime = timezone.make_aware(
        datetime.combine(quiz_setting.select_data, quiz_setting.end_time),
        timezone.get_current_timezone()
    )

    # Format times using a 12-hour clock format
    current_time_formatted = current_datetime.strftime('%Y-%m-%d %I:%M:%S %p')
    quiz_start_time_formatted = quiz_start_datetime.strftime('%Y-%m-%d %I:%M:%S %p')
    quiz_end_time_formatted = quiz_end_datetime.strftime('%Y-%m-%d %I:%M:%S %p')

    print("Current Datetime:", current_time_formatted)
    print("Quiz Start Datetime:", quiz_start_time_formatted)
    print("Quiz End Datetime:", quiz_end_time_formatted)

    # Check if the current datetime is within the quiz duration
    if quiz_start_datetime <= current_datetime <= quiz_end_datetime:
        answers = ActualQuiz.objects.filter(quiz_setting=quiz_setting)
        time_limit = len(answers) * quiz_setting.question_timer
        if request.method == "POST":
            score = 0
            result_sum = 0
            for answer in answers:
                user_answer_key = f"user_answer_{answer.id}"
                user_answer = request.POST.get(user_answer_key,'')
                print(user_answer)
                if user_answer == answer.answer:
                    score += 1
                result_a = ResultActual.objects.create(
                    user=request.user,
                    quiz_setting=quiz_setting,
                    question=answer,
                    score=1 if user_answer == answer.answer else 0,
                    user_answer=user_answer,
                )
                result_sum += result_a.score
            return redirect('result-actual', id=id)
        return render(request, 'profPage/link_actual_quiz.html', {'quiz_setting': quiz_setting, 'answers': answers, 'time_limit': time_limit})
    else:
        return redirect('quiz-not-available', id=id)
 
@login_required(login_url='home')   
def result_actual_quiz(request,id):
    quiz_setting = QuizSetting.objects.get(pk=id)
    questions = ActualQuiz.objects.filter(resultactual__user=request.user,resultactual__quiz_setting=quiz_setting).distinct()
    print(questions)
    results_details = []
    total_score = 0
    for question in questions:
        try:
            latest_result = ResultActual.objects.filter(
                user=request.user,
                question=question,
            ).latest('id')
        except ResultActual.DoesNotExist:
            continue
        
        result_details = {
            'add_text': question.add_text,
            'add_equation':question.add_equation,
            'solution':question.add_solution_here,
            'score': latest_result.score,
            'user_answer':latest_result.user_answer,
            'correct_answer':latest_result.question.answer,
            
        }
        total_score += latest_result.score
        results_details.append(result_details)
        print(results_details)
        print(latest_result.score)
    return render(request,'results/result_actual.html',{'results_details':results_details,'total_score':total_score,'quiz_setting':quiz_setting})

def result_all_actual(request):
    result_actual = ResultActual.objects.all()
    latest_results = {}

    for result in result_actual:
        if result.quiz_setting:
            quiz_setting_id = result.quiz_setting.id
            user_id = result.user.id

            if (quiz_setting_id, user_id) not in latest_results or result.time_finished > latest_results[(quiz_setting_id, user_id)].time_finished:
                latest_results[(quiz_setting_id, user_id)] = result

    for key, result in latest_results.items():
        result.total_score = ResultActual.objects.filter(quiz_setting=result.quiz_setting, user=result.user).aggregate(total_score=Sum('score'))['total_score']

    latest_results_list = [
        {
            'result': result,
            'total_score': result.total_score,
        }
        for result in latest_results.values()
    ]

    # Sort the list based on the total_score in descending order
    latest_results_list.sort(key=itemgetter('total_score'), reverse=True)

    # Group the sorted list by section and select_data
    grouped_results = {}
    for section_select_data, group in groupby(latest_results_list, key=lambda x: (x['result'].quiz_setting.section, x['result'].quiz_setting.select_data)):
        grouped_results[section_select_data] = list(group)
    return render(request, 'results/result_all_actual.html', {'grouped_results': grouped_results})


def not_available(request,id):
    quiz_setting = QuizSetting.objects.get(pk=id)
    current_datetime = timezone.localtime(timezone.now(), pytz.timezone('Asia/Manila'))

    # Combine the date and time, and make them timezone aware
    quiz_start_datetime = timezone.make_aware(
        datetime.combine(quiz_setting.select_data, quiz_setting.start_time),
        timezone.get_current_timezone()
    )
    quiz_end_datetime = timezone.make_aware(
        datetime.combine(quiz_setting.select_data, quiz_setting.end_time),
        timezone.get_current_timezone()
    )
    if quiz_start_datetime <= current_datetime <= quiz_end_datetime:
        return redirect('link-actual-quiz', id=id)
    return render(request,'notavailable/not_available_quiz.html',{'quiz_setting': quiz_setting})

def about_us(request):
    return render(request,'about_us.html')
def contact_us(request):
    return render(request,'contact_us.html')

def log_out(request):
    logout(request)
    return redirect('home')