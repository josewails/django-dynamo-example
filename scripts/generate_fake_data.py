import random

from django.utils import timezone
from django.conf import settings

from organisations.serializers import OrganisationSerializer, ProjectSerializer, EmployeeSerializer, \
    ProjectEmployeeSerializer
from organisations.models import Organisation, Project, Employee

from faker import Faker
from pynamodb.connection import Connection

conn = Connection(host='http://localhost:8080', region='localhost')

fake = Faker()


def generate_organisations():
    for _ in range(40):

        print("Generating organisation")
        serializer = OrganisationSerializer(
            data=dict(
                name=fake.word(),
                tier=fake.word()
            )
        )

        if serializer.is_valid():
            serializer.create(serializer.validated_data)


def update_organisation_tiers():
    organisations = Organisation.scan()
    tiers = ['tier_one', 'tier_two', 'tier_three']

    for organisation in organisations:
        conn.put_item('django-dynamo-example', organisation.pk, organisation.sk,
                      attributes=dict(tier=random.choice(tiers)))


def generate_projects():
    organisations = [org for org in Organisation.query('ORG', limit=4)]
    project_types = ['freelance', 'contract', 'full_time']
    project_status = ['pending', 'in_progress', 'on_hold', 'complete']
    for _ in range(40):
        print("Generating a project")
        organisation = random.choice(organisations)
        serializer = ProjectSerializer(
            data=dict(
                organisation_id=organisation.model_id,
                name=fake.word(),
                project_type=random.choice(project_types),
                status=random.choice(project_status)
            )
        )

        if serializer.is_valid():
            serializer.save()


def generate_employees():
    organisations = [org for org in Organisation.query('ORG', limit=4)]

    for _ in range(20):
        print("Generating Employee")
        organisation = random.choice(organisations)

        days = [_ for _ in range(1, 29)]
        months = [_ for _ in range(1, 13)]
        years = [_ for _ in range(1993, 2001)]
        serializer = EmployeeSerializer(
            data=dict(
                organisation_id=organisation.model_id,
                name=f"{fake.first_name()} {fake.last_name()}",
                email=fake.email(),
                date_of_birth=timezone.datetime(
                    year=random.choice(years),
                    month=random.choice(months),
                    day=random.choice(days)
                ).strftime('%Y-%m-%d')
            )
        )

        if serializer.is_valid():
            serializer.save()

        else:
            print(serializer.errors)


def generate_project_employees():
    organisation = Organisation.get("ORG", range_key="ORG#65a7b51dee5049565f65dc6839aa423d")
    projects = [project for project in
                Project.query(organisation.sk, Project.sk.startswith('PRO'))
                ]

    employees = [employee for employee in
                 Employee.query(organisation.sk, Employee.sk.startswith('EMP'))
                 ]

    for employee in employees:
        project = projects[0]
        serializer = ProjectEmployeeSerializer(
            data=dict(
                organisation_id=organisation.model_id,
                employee_id=employee.model_id,
                project_id=project.model_id
            )
        )

        if serializer.is_valid():
            serializer.save()

        else:
            print(serializer.errors)

    for project in projects:
        employee = employees[0]
        serializer = ProjectEmployeeSerializer(
            data=dict(
                organisation_id=organisation.model_id,
                employee_id=employee.model_id,
                project_id=project.model_id
            )
        )

        if serializer.is_valid():
            serializer.save()

        else:
            print(serializer.errors)


def run():
    update_organisation_tiers()
