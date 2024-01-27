from django.contrib import admin
from .models import User, PracticeMode,Question,ResultPractice, QuizSetting,ActualQuiz,ResultActual,SoloPracticeMode,SoloQuestion,SoloResultPractice
# Register your models here

admin.site.register(User)
admin.site.register(PracticeMode)
admin.site.register(Question)
admin.site.register(ResultPractice)
admin.site.register(QuizSetting)
admin.site.register(ActualQuiz)
admin.site.register(ResultActual)
admin.site.register(SoloResultPractice),
admin.site.register(SoloPracticeMode)
admin.site.register(SoloQuestion)