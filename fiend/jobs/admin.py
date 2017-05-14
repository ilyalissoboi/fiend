# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from fiend.jobs.models import Seeker, Employer, Job, School, Opening, Qualification, Skill, Language, AcademicDegree, \
    Salary, Address, Project

# Register your models here.

admin.site.register(Seeker)
admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(School)
admin.site.register(Opening)
admin.site.register(Qualification)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(AcademicDegree)
admin.site.register(Salary)
admin.site.register(Address)
admin.site.register(Project)
