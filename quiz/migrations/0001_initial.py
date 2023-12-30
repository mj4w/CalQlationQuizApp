# Generated by Django 5.0 on 2023-12-30 13:00

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(choices=[('Limits', 'Limits'), ('Derivative of a function', 'Derivative of a function'), ('Derivatives of trigonometric functions', 'Derivative of trigonometric functions'), ('Derivatives of inverse trigonometric functions', 'Derivative of inverse trigonometric functions'), ('Derivatives of Logarithmic and exponential functions', 'Derivative of logarithmic and exponential functions'), ('Derivatives of Hyperbolic and inverse hyperbolic functions', 'Derivative of hyperbolic and inverse hyperbolic functions'), ('Implicit Differentiation', 'Implicit Differentiation'), ('Explicit Differentiation', 'Explicit Differentiation')], max_length=100)),
                ('question_text', models.TextField()),
                ('option_a', models.TextField(blank=True, null=True)),
                ('option_b', models.TextField(blank=True, null=True)),
                ('option_c', models.TextField(blank=True, null=True)),
                ('answer', models.CharField(blank=True, max_length=100, null=True)),
                ('hint_question', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SoloQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.CharField(blank=True, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=10, null=True)),
                ('question_text', models.TextField()),
                ('option_a', models.TextField(blank=True, null=True)),
                ('option_b', models.TextField(blank=True, null=True)),
                ('option_c', models.TextField(blank=True, null=True)),
                ('answer', models.CharField(blank=True, max_length=100, null=True)),
                ('hint_question', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='username')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PracticeMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('num_questions', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('questions', models.ManyToManyField(to='quiz.question')),
            ],
        ),
        migrations.CreateModel(
            name='QuizSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('select_data', models.DateField(verbose_name='Select Date')),
                ('start_time', models.TimeField(verbose_name='Start Time')),
                ('end_time', models.TimeField(verbose_name='End Time')),
                ('section', models.CharField(blank=True, max_length=255, null=True, verbose_name='Section')),
                ('show_correct_answer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Show Answer')),
                ('show_solution', models.CharField(blank=True, max_length=255, null=True, verbose_name='Show Solution')),
                ('question_timer', models.IntegerField(default=10, verbose_name='Question Timer')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActualQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_text', models.CharField(blank=True, max_length=255, null=True)),
                ('add_equation', models.CharField(blank=True, max_length=255, null=True)),
                ('add_solution_here', models.TextField(blank=True, null=True)),
                ('upload_photo', models.ImageField(blank=True, upload_to='actual_quiz_photo/')),
                ('option_a', models.TextField(blank=True, null=True)),
                ('option_b', models.TextField(blank=True, null=True)),
                ('option_c', models.TextField(blank=True, null=True)),
                ('answer', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('quiz_setting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.quizsetting')),
            ],
        ),
        migrations.CreateModel(
            name='ResultActual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('user_answer', models.CharField(default='', max_length=100)),
                ('time_finished', models.DateTimeField(default=django.utils.timezone.now)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.actualquiz')),
                ('quiz_setting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.quizsetting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResultPractice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('num_question_show', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('user_answer', models.CharField(default='', max_length=100)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('topic_show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.practicemode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoloPracticeMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.CharField(max_length=10)),
                ('num_questions', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('questions', models.ManyToManyField(to='quiz.soloquestion')),
            ],
        ),
        migrations.CreateModel(
            name='SoloResultPractice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_question_show', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('user_answer', models.CharField(default='', max_length=100)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.soloquestion')),
                ('topic_show', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.solopracticemode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]