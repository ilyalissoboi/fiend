# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from collections import Counter
from functools import reduce

from django.db import models


##########################
# main models
##########################

class Seeker(models.Model):
    # personal information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1)
    married = models.BooleanField()

    # contact information
    location = models.ForeignKey('jobs.Address')
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    # education
    schools = models.ManyToManyField('jobs.School')

    # salary
    expected_salary_lower = models.ForeignKey('jobs.Salary', related_name='+')
    expected_salary_upper = models.ForeignKey('jobs.Salary', related_name='+')

    # job history
    jobs = models.ForeignKey('jobs.Job')

    # skills
    skills = models.ForeignKey('jobs.Skill')

    # languages
    languages = models.ForeignKey('jobs.Language')

    # projects
    projects = models.ForeignKey('jobs.Project')

    # misc
    self_pr = models.TextField()


class Employer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    founded = models.DateField()
    location = models.ForeignKey('jobs.Address')
    employees = models.IntegerField()
    description = models.TextField()
    openings = models.ForeignKey('jobs.Opening')


class Job(models.Model):
    name = models.CharField(max_length=255)
    current = models.BooleanField(default=False)
    started = models.DateField()
    left = models.DateField()
    location = models.ForeignKey('jobs.Address')
    description = models.TextField()
    logo = models.TextField(max_length=255)

    # skills learned
    skills = models.ForeignKey('jobs.Skill')

    def get_years(self):
        start = self.started
        end = datetime.datetime.utcnow().date() if self.current else self.left

        return end.year - start.year

    def get_skills_experience(self):
        skills = self.skills.objects.all()

        for skill in skills:
            skill.years_of_experience = self.get_years()

        return skills

    def get_skills_experience_map(self):
        return dict([(skill.name, skill.years_of_experience) for skill in self.get_skills_experience()])


class School(models.Model):
    name = models.CharField(max_length=255)
    started = models.DateField()
    graduated = models.DateField()
    degree = models.ForeignKey('jobs.AcademicDegree')

    # skills learned
    skills = models.ForeignKey('jobs.Skill')


class Opening(models.Model):
    INTERNSHIP = 'internship'
    PART_TIME = 'part-time'
    CONTRACT = 'contract'
    FULL_TIME = 'full-time'

    OPENING_TYPE_CHOICES = (
        (INTERNSHIP, INTERNSHIP),
        (PART_TIME, PART_TIME),
        (CONTRACT, CONTRACT),
        (FULL_TIME, FULL_TIME)
    )

    ENTRY = 'entry'
    MID = 'mid'
    SENIOR = 'senior'

    SENIORITY_CHOICES = (
        (ENTRY, ENTRY),
        (MID, MID),
        (SENIOR, SENIOR)
    )

    # opening information
    location = models.ForeignKey('jobs.Address')
    valid_from = models.DateField()
    valid_until = models.DateField()
    type = models.CharField(max_length=50, choices=OPENING_TYPE_CHOICES)
    seniority = models.CharField(max_length=50, choices=SENIORITY_CHOICES)
    description = models.TextField()
    responsibilities = models.TextField()
    required_qualifications = models.ForeignKey('jobs.Qualification', related_name='+')
    preferred_qualifications = models.ForeignKey('jobs.Qualification', related_name='+')

    # salary
    salary_range_lower = models.ForeignKey('jobs.Salary', related_name='+')
    salary_range_upper = models.ForeignKey('jobs.Salary', related_name='+')
    other_compensation = models.ForeignKey('jobs.Salary', related_name='+')

    # automatic fit parameters
    accept_threshold = models.FloatField()
    review_threshold = models.FloatField()

    # contact information
    email = models.EmailField()

    # fitting methods
    def fit_salary(self, seeker):
        normalized_expected_salary_lower = self.salary_range_lower.normalize_salary(seeker.expected_salary_lower)
        normalized_expected_salary_upper = self.salary_range_lower.normalize_salary(seeker.expected_salary_upper)

        if normalized_expected_salary_upper <= self.salary_range_lower.amount:
            return 10.0

        if normalized_expected_salary_upper <= self.salary_range_upper.amount:
            return 5.0

        if normalized_expected_salary_lower > self.salary_range_upper.amount:
            return 0.0

        if normalized_expected_salary_lower < self.salary_range_upper.amount:
            return 5.0

        return 0.0

    def fit_education(self, seeker):
        education_required = self.required_qualifications.objects.filter(degree__isnull=False)
        seeker_education = seeker.schools.objects.all()

        education_required_exact_fit = []
        education_required_over_fit = []

        for item in education_required:
            education_required_exact_fit.append(
                filter(lambda x: x.level == item.level and x.major == item.major, seeker_education))
            education_required_over_fit.append(
                filter(lambda x: x.level >= item.level and x.major == item.major, seeker_education))

        education_preferred = self.preferred_qualifications.objects.filter(degree__isnull=False)

        education_preferred_exact_fit = []
        education_preferred_over_fit = []

        for item in education_preferred:
            education_preferred_exact_fit.append(
                filter(lambda x: x.level == item.level and x.major == item.major, seeker_education))
            education_preferred_over_fit.append(
                filter(lambda x: x.level >= item.level and x.major == item.major, seeker_education))

        result = 0.0

        if education_required_exact_fit:
            result += 5.0
        if education_required_over_fit:
            result += 1.0
        if education_preferred_exact_fit:
            result += 2.0
        if education_preferred_over_fit:
            result += 2.0

        return result

    def fit_skills(self, seeker):
        def update_counter_in_place(a, b):
            a.update(b)
            return a

        seeker_job_skill_map = reduce(
            update_counter_in_place,
            (Counter(job.get_skills_experience_map()) for job in seeker.jobs.objects.all())
        )

        required_skills_map = reduce(
            update_counter_in_place,
            (Counter(job.get_skills_experience_map()) for job in self.required_qualifications.objects.filter(skills__isnull=False))
        )

        preferred_skills_map = reduce(
            update_counter_in_place,
            (Counter(job.get_skills_experience_map()) for job in self.preferred_qualifications.objects.filter(skills__isnull=False))
        )

        seeker_required_skills = set(seeker_job_skill_map.keys()) & set(required_skills_map.keys())
        seeker_preferred_skills = set(seeker_job_skill_map.keys()) & set(preferred_skills_map.keys())

        result = 0.0

        for skill in seeker_required_skills:
            if seeker_job_skill_map[skill] >= required_skills_map[skill]:
                result += 1.0
            else:
                result += 0.5

        for skill in seeker_preferred_skills:
            if seeker_job_skill_map[skill] >= preferred_skills_map[skill]:
                result += 1.0
            else:
                result += 0.5

        def normalize_result():
            return result / float(len(required_skills_map.keys()) + len(preferred_skills_map.keys())) * 10.0

        return normalize_result()

    def fit_languages(self, seeker):
        languages_required = self.required_qualifications.objects.filter(languages__isnull=False)
        languages_preferred = self.preferred_qualifications.objects.filter(languages__isnull=False)

        seeker_languages = seeker.languages.objects.all()

        languages_required_fit = []
        languages_preferred_fit = []

        for item in languages_required:
            languages_required_fit.append(
                filter(lambda x: x.proficiency >= item.proficiency and x.name == item.name, seeker_languages)
            )

        for item in languages_preferred:
            languages_preferred_fit.append(
                filter(lambda x: x.proficiency >= item.proficiency and x.name == item.name, seeker_languages)
            )

        result = 0.0

        for item in languages_required_fit:
            result += 1.0

        for item in languages_preferred_fit:
            result += 1.0

        def normalize_result():
            return result / float(len(languages_required) + len(languages_preferred)) * 10.0

        return normalize_result()

    def normalize_fit(self, score):
        return float(score) / 40.0 * 100.0

    def calculate_fit(self, seeker):
        return self.normalize_fit(
            self.fit_salary(seeker) +
            self.fit_education(seeker) +
            self.fit_skills(seeker) +
            self.fit_languages(seeker)
        )


class Qualification(models.Model):
    degree = models.ForeignKey('jobs.AcademicDegree')
    skills = models.ForeignKey('jobs.Skill')
    languages = models.ForeignKey('jobs.Language')
    other = models.TextField()

    def get_skills_experience_map(self):
        return dict([(skill.name, skill.years_of_experience) for skill in self.skills.objects.all()])


class Skill(models.Model):
    BEGINNER = '1_beginner'
    ADVANCED = '2_advanced'
    EXPERT = '3_expert'

    SKILL_PROFICIENCY_CHOICES = (
        (BEGINNER, BEGINNER),
        (ADVANCED, ADVANCED),
        (EXPERT, EXPERT)
    )

    def __lt__(self, other):
        if isinstance(other, Skill):
            return self.proficiency < other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __le__(self, other):
        if isinstance(other, Skill):
            return self.proficiency <= other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __eq__(self, other):
        if isinstance(other, Skill):
            return self.proficiency == other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __ne__(self, other):
        if isinstance(other, Skill):
            return self.proficiency != other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __gt__(self, other):
        if isinstance(other, Skill):
            return self.proficiency > other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __ge__(self, other):
        if isinstance(other, Skill):
            return self.proficiency >= other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    name = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=50, choices=SKILL_PROFICIENCY_CHOICES)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    years_of_experience = models.IntegerField()


class Language(models.Model):
    BASIC = '1_basic'
    INTERMEDIATE = '2_intermediate'
    BUSINESS = '3_business'
    FLUENT = '4_fluent'
    NATIVE = '5_native'

    LANGUAGE_PROFICIENCY_CHOICES = (
        (BASIC, BASIC),
        (INTERMEDIATE, INTERMEDIATE),
        (BUSINESS, BUSINESS),
        (FLUENT, FLUENT),
        (NATIVE, NATIVE)
    )

    def __lt__(self, other):
        if isinstance(other, Language):
            return self.proficiency < other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __le__(self, other):
        if isinstance(other, Language):
            return self.proficiency <= other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __eq__(self, other):
        if isinstance(other, Language):
            return self.proficiency == other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __ne__(self, other):
        if isinstance(other, Language):
            return self.proficiency != other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __gt__(self, other):
        if isinstance(other, Language):
            return self.proficiency > other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    def __ge__(self, other):
        if isinstance(other, Language):
            return self.proficiency >= other.proficiency
        else:
            raise NotImplementedError('not implemented yet')

    name = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=50, choices=LANGUAGE_PROFICIENCY_CHOICES)


class AcademicDegree(models.Model):
    BACHELOR = '1_bachelor'
    MASTER = '2_master'
    DOCTOR = '3_doctor'

    DEGREE_LEVEL_CHOICES = (
        (BACHELOR, BACHELOR),
        (MASTER, MASTER),
        (DOCTOR, DOCTOR)
    )

    def __lt__(self, other):
        if isinstance(other, AcademicDegree):
            return self.level < other.level
        else:
            raise NotImplementedError('not implemented yet')

    def __le__(self, other):
        if isinstance(other, AcademicDegree):
            return self.level <= other.level
        else:
            raise NotImplementedError('not implemented yet')

    def __eq__(self, other):
        if isinstance(other, AcademicDegree):
            return self.level == other.level
        else:
            raise NotImplementedError('not implemented yet')

    def __ne__(self, other):
        if isinstance(other, AcademicDegree):
            return self.level != other.level
        else:
            raise NotImplementedError('not implemented yet')

    def __gt__(self, other):
        if isinstance(other, AcademicDegree):
            return self.level > other.level
        else:
            raise NotImplementedError('not implemented yet')

    def __ge__(self, other):
        if isinstance(other, AcademicDegree):
            return self.level >= other.level
        else:
            raise NotImplementedError('not implemented yet')

    name = models.CharField(max_length=255)
    level = models.CharField(max_length=50, choices=DEGREE_LEVEL_CHOICES)
    major = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)


class Salary(models.Model):
    HOURS_IN_WEEK = 8 * 5
    WEEKS_IN_MONTH = 4
    MONTHS_IN_YEAR = 12

    HOURLY = 'hourly'
    WEEKLY = 'weekly'
    BI_WEEKLY = 'bi-weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    BONUS = 'bonus'

    SALARY_TYPE_CHOICES = (
        (HOURLY, HOURLY),
        (WEEKLY, WEEKLY),
        (BI_WEEKLY, BI_WEEKLY),
        (MONTHLY, MONTHLY),
        (YEARLY, YEARLY),
        (BONUS, BONUS)
    )

    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    after_tax = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=SALARY_TYPE_CHOICES)
    visible = models.BooleanField()

    # conversion methods (logic mostly placeholder)
    # TODO: implement proper conversion logic if building a full-fledged demo
    def normalize_salary(self, other):
        if self.type == self.HOURLY:
            return other.to_hourly()
        elif self.type == self.WEEKLY:
            return other.to_weekly()
        elif self.type == self.BI_WEEKLY:
            return other.to_bi_weekly()
        elif self.type == self.MONTHLY:
            return other.to_monthly()
        elif self.type == self.YEARLY:
            return other.to_yearly()

    def to_hourly(self):
        if self.type == self.HOURLY:
            return self.amount
        elif self.type == self.WEEKLY:
            return float(self.amount) / float(self.HOURS_IN_WEEK)
        elif self.type == self.BI_WEEKLY:
            return float(self.amount) / (float(self.HOURS_IN_WEEK) * 2)
        elif self.type == self.MONTHLY:
            return float(self.amount) / (float(self.HOURS_IN_WEEK * self.WEEKS_IN_MONTH))
        elif self.type == self.YEARLY:
            return float(self.amount) / (float(self.HOURS_IN_WEEK * self.WEEKS_IN_MONTH * self.MONTHS_IN_YEAR))

    def to_weekly(self):
        if self.type == self.HOURLY:
            return self.amount * self.HOURS_IN_WEEK
        elif self.type == self.WEEKLY:
            return self.amount
        elif self.type == self.BI_WEEKLY:
            return float(self.amount) / 2
        elif self.type == self.MONTHLY:
            return float(self.amount) / self.WEEKS_IN_MONTH
        elif self.type == self.YEARLY:
            return float(self.amount) / (self.WEEKS_IN_MONTH * self.MONTHS_IN_YEAR)

    def to_bi_weekly(self):
        if self.type == self.HOURLY:
            return self.amount * self.HOURS_IN_WEEK * 2
        elif self.type == self.WEEKLY:
            return self.amount * 2
        elif self.type == self.BI_WEEKLY:
            return self.amount
        elif self.type == self.MONTHLY:
            return float(self.amount) / (self.WEEKS_IN_MONTH / 2)
        elif self.type == self.YEARLY:
            return float(self.amount) / (self.WEEKS_IN_MONTH / 2 * self.MONTHS_IN_YEAR)

    def to_monthly(self):
        if self.type == self.HOURLY:
            return self.amount * self.HOURS_IN_WEEK * self.WEEKS_IN_MONTH
        elif self.type == self.WEEKLY:
            return self.amount * self.WEEKS_IN_MONTH
        elif self.type == self.BI_WEEKLY:
            return float(self.amount) * self.WEEKS_IN_MONTH / 2
        elif self.type == self.MONTHLY:
            return self.amount
        elif self.type == self.YEARLY:
            return float(self.amount) / self.MONTHS_IN_YEAR

    def to_yearly(self):
        if self.type == self.HOURLY:
            return self.amount * self.HOURS_IN_WEEK * self.WEEKS_IN_MONTH * self.MONTHS_IN_YEAR
        elif self.type == self.WEEKLY:
            return self.amount * self.WEEKS_IN_MONTH * self.MONTHS_IN_YEAR
        elif self.type == self.BI_WEEKLY:
            return float(self.amount) * self.WEEKS_IN_MONTH / 2 * self.MONTHS_IN_YEAR
        elif self.type == self.MONTHLY:
            return self.amount * self.MONTHS_IN_YEAR
        elif self.type == self.YEARLY:
            return self.amount

##########################
# helper models
##########################


class Address(models.Model):
    country = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255)
    street3 = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=50)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
