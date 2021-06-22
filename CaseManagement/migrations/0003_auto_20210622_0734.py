# Generated by Django 2.2 on 2021-06-21 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CaseManagement', '0002_auto_20210622_0731'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DB_module2',
        ),
        migrations.RemoveField(
            model_name='db_testcase',
            name='fk_module',
        ),
        migrations.AlterField(
            model_name='db_testcase',
            name='t_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CaseManagement.DB_module', verbose_name='所属模块'),
        ),
    ]