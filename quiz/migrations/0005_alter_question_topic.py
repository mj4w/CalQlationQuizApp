# Generated by Django 5.0 on 2024-02-29 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_alter_actualquiz_add_solution_here_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.CharField(choices=[('Limits', 'Limits'), ('Derivative of a function', 'Derivative of a function'), ('Derivatives of trigonometric functions', 'Derivative of trigonometric functions'), ('Derivatives of inverse trigonometric functions', 'Derivative of inverse trigonometric functions'), ('Derivatives of Logarithmic and exponential functions', 'Derivative of logarithmic and exponential functions'), ('Derivatives of Hyperbolic and inverse hyperbolic functions', 'Derivative of hyperbolic and inverse hyperbolic functions'), ('Implicit Differentiation', 'Implicit Differentiation'), ('Explicit Differentiation', 'Explicit Differentiation'), ('Higher Derivative', 'Higher Derivative')], max_length=100),
        ),
    ]