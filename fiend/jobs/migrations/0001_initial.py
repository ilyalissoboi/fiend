# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 04:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicDegree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('bachelor', 'bachelor'), ('master', 'master'), ('doctor', 'doctor')], max_length=50)),
                ('major', models.CharField(max_length=255)),
                ('topic', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('county', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('street1', models.CharField(max_length=255)),
                ('street2', models.CharField(max_length=255)),
                ('street3', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('founded', models.DateField()),
                ('employees', models.IntegerField()),
                ('description', models.TextField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('started', models.DateField()),
                ('left', models.DateField()),
                ('description', models.TextField()),
                ('logo', models.TextField(max_length=255)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('proficiency', models.CharField(choices=[('basic', 'basic'), ('intermediate', 'intermediate'), ('business', 'business'), ('fluent', 'fluent'), ('native', 'native')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Opening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateField()),
                ('valid_until', models.DateField()),
                ('type', models.CharField(choices=[('internship', 'internship'), ('part-time', 'part-time'), ('contract', 'contract'), ('full-time', 'full-time')], max_length=50)),
                ('seniority', models.CharField(choices=[('entry', 'entry'), ('mid', 'mid'), ('senior', 'senior')], max_length=50)),
                ('description', models.TextField()),
                ('responsibilities', models.TextField()),
                ('accept_threshold', models.FloatField()),
                ('review_threshold', models.FloatField()),
                ('email', models.EmailField(max_length=254)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years_of_experience', models.IntegerField()),
                ('other', models.TextField()),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.AcademicDegree')),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('after_tax', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('hourly', 'hourly'), ('weekly', 'weekly'), ('bi-weekly', 'bi-weekly'), ('monthly', 'monthly'), ('yearly', 'yearly'), ('bonus', 'bonus')], max_length=50)),
                ('visible', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('started', models.DateField()),
                ('graduated', models.DateField()),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.AcademicDegree')),
            ],
        ),
        migrations.CreateModel(
            name='Seeker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=1)),
                ('married', models.BooleanField()),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('self_pr', models.TextField()),
                ('expected_salary_lower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jobs.Salary')),
                ('expected_salary_upper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jobs.Salary')),
                ('jobs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Job')),
                ('languages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Language')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Address')),
                ('projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Project')),
                ('schools', models.ManyToManyField(to='jobs.School')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('proficiency', models.CharField(choices=[('beginner', 'beginner'), ('advanced', 'advanced'), ('expert', 'expert')], max_length=50)),
                ('category', models.CharField(max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
                ('years_of_experience', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='seeker',
            name='skills',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Skill'),
        ),
        migrations.AddField(
            model_name='school',
            name='skills',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Skill'),
        ),
        migrations.AddField(
            model_name='qualification',
            name='skills',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Skill'),
        ),
        migrations.AddField(
            model_name='opening',
            name='other_compensation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jobs.Salary'),
        ),
        migrations.AddField(
            model_name='opening',
            name='preferred_qualifications',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jobs.Qualification'),
        ),
        migrations.AddField(
            model_name='opening',
            name='required_qualifications',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jobs.Qualification'),
        ),
        migrations.AddField(
            model_name='opening',
            name='salary_range_lower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jobs.Salary'),
        ),
        migrations.AddField(
            model_name='opening',
            name='salary_range_upper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='jobs.Salary'),
        ),
        migrations.AddField(
            model_name='job',
            name='skills',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Skill'),
        ),
        migrations.AddField(
            model_name='employer',
            name='openings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Opening'),
        ),
    ]