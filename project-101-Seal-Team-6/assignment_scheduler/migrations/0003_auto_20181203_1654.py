# Generated by Django 2.1.1 on 2018-12-03 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_scheduler', '0002_auto_20181203_1649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='class_num',
            new_name='course_num2',
        ),
    ]
