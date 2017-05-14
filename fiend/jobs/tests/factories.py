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

class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Address

    country = factory.Faker('address.country')
    county = factory.Faker('address.state')
    city = factory.Faker('address.city')
    street1 = factory.Faker('address.street_address')
    street2 = factory.Faker('address.street_address')
    street3 = factory.Faker('address.street_address')
    postal_code = factory.Faker('address.postalcode')


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    name = factory.Faker('company.bs')
    description = factory.Faker('text')
    url = factory.Faker('internet.url')


class SalaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Salary

    name = factory.Sequence(lambda n: "Salary %03d" % n)
    amount = random.random() * 1000.0
    after_tax = random.random() >= 0.5
    type = random.choice(models.Salary.SALARY_TYPE_CHOICES)
    visible = random.random() >= 0.5


class AcademicDegreeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AcademicDegree

    name = factory.Faker('job')
    level = random.choice(models.AcademicDegree.DEGREE_LEVEL_CHOICES)
    major = random.choice(DEGREE_MAJORS)
    topic = factory.Faker('company.bs')


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Language

    name = random.choice(LANGUAGES)
    proficiency = random.choice(models.Language.LANGUAGE_PROFICIENCY_CHOICES)


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Skill

    name = random.choice(SKILLS)
    proficiency = random.choice(models.Skill.SKILL_PROFICIENCY_CHOICES)
    category = factory.Sequence(lambda n: "Category %03d" % n)
    sub_category = factory.Sequence(lambda n: "Sub-category %03d" % n)
    years_of_experience = 0
