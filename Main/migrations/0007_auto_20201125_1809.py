# Generated by Django 3.1.2 on 2020-11-25 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0006_auto_20201125_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleChoiceSurveyTask',
            fields=[
                ('alltasks_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Main.alltasks')),
                ('question', models.CharField(max_length=1000)),
                ('choices', models.TextField(max_length=5000)),
                ('multiple_choices_allowed', models.BooleanField()),
            ],
            bases=('Main.alltasks',),
        ),
        migrations.AddField(
            model_name='peoplegroup',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='SurveyVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.IntegerField()),
                ('people_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.peoplegroup')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.multiplechoicesurveytask')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('question', 'people_group', 'user')},
            },
        ),
    ]
