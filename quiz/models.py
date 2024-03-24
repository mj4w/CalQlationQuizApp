from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True, blank=True,null=True)
    
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = None 
        super().save(*args, **kwargs)

    
class Question(models.Model):
    TOPIC_CHOICES = [
        ('Limits','Limits'),
        ('Derivative of a function','Derivative of a function'),
        ('Derivatives of trigonometric functions','Derivative of trigonometric functions'),
        ('Derivatives of inverse trigonometric functions','Derivative of inverse trigonometric functions'),
        ('Derivatives of Logarithmic and exponential functions','Derivative of logarithmic and exponential functions'),
        ('Derivatives of Hyperbolic and inverse hyperbolic functions','Derivative of hyperbolic and inverse hyperbolic functions'),
        ('Implicit Differentiation','Implicit Differentiation'),
        ('Explicit Differentiation','Explicit Differentiation'),
        ('Higher Derivative','Higher Derivative'),
    ]
    topic = models.CharField(max_length=100, choices=TOPIC_CHOICES)
    question_text = models.TextField()
    question_formula = models.TextField(blank=True, null=True)
    option_a = models.TextField(null=True, blank=True)
    option_b = models.TextField(null=True, blank=True)
    option_c = models.TextField(null=True, blank=True)
    answer = models.CharField(max_length=100, null=True, blank=True)
    hint_question = models.CharField(max_length=100, null=True, blank=True)
    solution_here = models.ImageField(upload_to='solutions/',blank=True)

    def __str__(self):
        return f'{self.id} Topic: {self.topic},Question: {self.question_text}'
    
class PracticeMode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100) 
    num_questions = models.IntegerField(default=0)

    questions = models.ManyToManyField(Question)

    def __str__(self):
        return f'{self.user.email} - Topic: {self.topic}, Num Questions: {self.num_questions}'

class ResultPractice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    date = models.DateField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    topic_show = models.ForeignKey(PracticeMode, on_delete=models.CASCADE)
    num_question_show = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    user_answer = models.CharField(max_length=100, null=False) 
    
    def __str__(self):
        return f'{self.user} Score: {self.score} show questions {self.num_question_show}'
    def save(self, *args, **kwargs):
        # Set the date to the current date using timezone.now()
        if not self.date:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)
        
        
# solo practice
class SoloQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy','Easy'),
        ('medium','Medium'),
        ('hard','Hard'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES,  blank=True, null=True)
    question_text = models.TextField()
    question_formula = models.TextField(blank=True, null=True)
    option_a = models.TextField(null=True, blank=True)
    option_b = models.TextField(null=True, blank=True)
    option_c = models.TextField(null=True, blank=True)
    answer = models.CharField(max_length=100, null=True, blank=True)
    hint_question = models.CharField(max_length=100, null=True, blank=True)
    solution_here = models.ImageField(upload_to='solutions/',blank=True)

    def __str__(self):
        return f'{self.pk}: Difficulty: {self.difficulty}, Question: {self.question_text} {self.question_formula}'
    
class SoloPracticeMode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10)
    num_questions = models.IntegerField(default=0)
    questions = models.ManyToManyField(SoloQuestion)

    def __str__(self):
        return f'{self.user.username}, Difficulty: {self.difficulty}, Num Questions: {self.num_questions}'

class SoloResultPractice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    topic_show = models.ForeignKey(SoloPracticeMode, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(SoloQuestion, on_delete=models.CASCADE)
    num_question_show = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    user_answer = models.CharField(max_length=100, null=False) 
    
    def __str__(self):
        return f'{self.user} Score: {self.score} show questions {self.num_question_show}'

# prof side
class QuizSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    select_data = models.DateField(_('Select Date'))
    start_time = models.TimeField(_('Start Time'))
    end_time = models.TimeField(_('End Time'))
    section = models.CharField(_('Section'), max_length=255, null=True, blank=True)
    show_correct_answer = models.CharField(_('Show Answer'), max_length=255, blank=True, null=True)
    show_solution = models.CharField(_('Show Solution'), max_length=255, blank=True, null=True)  
    question_timer = models.IntegerField(_('Question Timer'), default=10)
    
    def formatted_start_time(self):
        return self.start_time.strftime('%I:%M %p')
    
    def formatted_end_time(self):
        return self.end_time.strftime('%I:%M %p')
    
    def __str__(self):
        return f"{self.id} - {self.section} - {self.formatted_start_time()} to {self.formatted_end_time()}"
    
class ActualQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_setting = models.ForeignKey(QuizSetting, on_delete=models.CASCADE,blank=True, null=True)
    add_text = models.CharField(max_length=255, blank=True, null=True)
    add_equation = models.CharField(max_length=255, blank=True, null=True)
    add_solution_here =  models.ImageField(upload_to='prof_solution/',blank=True)
    upload_photo = models.ImageField(upload_to='actual_quiz_photo/',blank=True)
    option_a = models.TextField(null=True, blank=True)
    option_b = models.TextField(null=True, blank=True)
    option_c = models.TextField(null=True, blank=True)
    answer = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.add_text}"
    
class ResultActual(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    quiz_setting = models.ForeignKey(QuizSetting,on_delete =models.CASCADE,blank=True, null=True)
    question = models.ForeignKey(ActualQuiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    user_answer = models.CharField(max_length=100, null=False) 
    time_finished = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user} Score: {self.score} Question: {self.question}'