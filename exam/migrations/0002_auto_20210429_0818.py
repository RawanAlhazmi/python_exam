# Generated by Django 3.2 on 2021-04-29 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Item', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('granted_date', models.DateField()),
                ('granted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('liked_by', models.ManyToManyField(related_name='liked_wishes', to='exam.User')),
                ('wisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to='exam.user')),
            ],
        ),
    ]
