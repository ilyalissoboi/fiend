from datetime import datetime

import arrow
import factory
import random

from fiend.jobs import models

DEGREE_MAJORS = (
    'computer science',
    'information systems',
    'medicine',
    'business administration',
    'international law',
    'material science',
    'chemical engineering',
    'film',
    'music',
    'corporate law',
    'political science',
    'history'
)

LANGUAGES = (
    'english',
    'german',
    'french',
    'russian',
    'mandarin',
    'japanese'
)

SKILLS = (
    'python',
    'java',
    'c++',
    'linux',
    'business administration',
    'sales',
    'law',
    'team management',
    'sales'
)


class SkillsMixin(object):
    @factory.post_generation
    def skills(self, create, count, **kwargs):
        if count is None:
            count = 0

        make = getattr(models.Skill, 'create' if create else 'build')
        items = [make() for i in range(count)]

        if not create:
            self._prefetched_objects_cache = {'skills': items}


class LanguagesMixin(object):
    @factory.post_generation
    def languages(self, create, count, **kwargs):
        if count is None:
            count = 0

        make = getattr(models.Language, 'create' if create else 'build')
        items = [make() for i in range(count)]

        if not create:
            self._prefetched_objects_cache = {'languages': items}


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Address

    id = factory.Sequence(lambda n: n)
    country = factory.Faker('country')
    county = factory.Faker('state')
    city = factory.Faker('city')
    street1 = factory.Faker('street_address')
    street2 = factory.Faker('street_address')
    street3 = factory.Faker('street_address')
    postal_code = factory.Faker('postalcode')


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('bs')
    description = factory.Faker('text')
    url = factory.Faker('url')


class SalaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Salary

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Salary %03d" % n)
    amount = random.random() * 1000.0
    after_tax = random.random() >= 0.5
    type = random.choice(models.Salary.SALARY_TYPE_CHOICES)
    visible = random.random() >= 0.5


class AcademicDegreeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AcademicDegree

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('job')
    level = random.choice(models.AcademicDegree.DEGREE_LEVEL_CHOICES)
    major = random.choice(DEGREE_MAJORS)
    topic = factory.Faker('bs')


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Language

    id = factory.Sequence(lambda n: n)
    name = random.choice(LANGUAGES)
    proficiency = random.choice(models.Language.LANGUAGE_PROFICIENCY_CHOICES)


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Skill

    id = factory.Sequence(lambda n: n)
    name = random.choice(SKILLS)
    proficiency = random.choice(models.Skill.SKILL_PROFICIENCY_CHOICES)
    category = factory.Sequence(lambda n: "Category %03d" % n)
    sub_category = factory.Sequence(lambda n: "Sub-category %03d" % n)
    years_of_experience = 0


class QualificationFactory(factory.django.DjangoModelFactory, SkillsMixin):
    class Meta:
        model = models.Qualification

    id = factory.Sequence(lambda n: n)
    degree = factory.SubFactory(AcademicDegreeFactory)
    skills = factory.SubFactory(SkillFactory)
    languages = factory.SubFactory(LanguageFactory)
    other = factory.Faker('text')




class OpeningFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Opening

    id = factory.Sequence(lambda n: n)
    location = factory.SubFactory(AddressFactory)
    valid_from = datetime.utcnow().date()
    valid_until = arrow.get(valid_from).replace(months=+3).date()
    type = random.choice(models.Opening.OPENING_TYPE_CHOICES)
    seniority = random.choice(models.Opening.SENIORITY_CHOICES)
    description = factory.Faker('text')
    responsibilities = factory.Faker('text')
    required_qualifications = factory.SubFactory(QualificationFactory)
    preferred_qualifications = factory.SubFactory(QualificationFactory)
    salary_range_lower = factory.SubFactory(SalaryFactory)
    salary_range_upper = factory.SubFactory(SalaryFactory)
    other_compensation = factory.SubFactory(SalaryFactory)
    accept_threshold = 80.0
    review_threshold = 50.0
    email = factory.Faker('email')


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.School

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "School %03d" % n)
    started = arrow.get(datetime.utcnow()).replace(years=-10).date()
    graduated = arrow.get(datetime.utcnow()).replace(years=-7).date()
    degree = factory.SubFactory(AcademicDegreeFactory)
    skills = factory.SubFactory(SkillFactory)


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Job

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('job')
    started = arrow.get(datetime.utcnow()).replace(years=-10).date()
    left = arrow.get(datetime.utcnow()).replace(years=-7).date()
    location = factory.SubFactory(AddressFactory)
    description = factory.Faker('text')
    logo = 'logo.jpg'
    skills = factory.SubFactory(SkillFactory)


class EmployerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Employer

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Employer %03d" % n)
    email = factory.Faker('email')
    founded = arrow.get(datetime.utcnow()).replace(years=-10).date()
    location = factory.SubFactory(AddressFactory)
    employees = 100
    description = factory.Faker('text')
    openings = factory.SubFactory(OpeningFactory)


class SeekerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Seeker

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker('first_name_male')
    last_name = factory.Faker('last_name_male')
    gender = 'M'
    married = random.random() > 0.5
    location = factory.SubFactory(AddressFactory)
    phone = factory.Faker('phone_number')
    email = factory.Faker('email')
    schools = factory.SubFactory(SchoolFactory)
    expected_salary_lower = factory.SubFactory(SalaryFactory)
    expected_salary_upper = factory.SubFactory(SalaryFactory)
    jobs = factory.SubFactory(JobFactory)
    skills = factory.SubFactory(SkillFactory)
    languages = factory.SubFactory(LanguageFactory)
    projects = factory.SubFactory(ProjectFactory)
    self_pr = factory.Faker('text')
