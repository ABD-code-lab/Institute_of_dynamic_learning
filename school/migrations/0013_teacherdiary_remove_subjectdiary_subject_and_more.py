# Generated by Django 5.1.5 on 2025-05-03 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_alter_subject_options_alter_subjectdiary_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherDiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='subjectdiary',
            name='subject',
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={},
        ),
        migrations.RemoveIndex(
            model_name='subject',
            name='school_subj_name_880daa_idx',
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='teacherdiary',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.subject'),
        ),
        migrations.AddField(
            model_name='teacherdiary',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher'),
        ),
        migrations.DeleteModel(
            name='SubjectDiary',
        ),
    ]
