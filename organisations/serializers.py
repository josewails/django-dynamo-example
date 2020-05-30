from django.utils import timezone

from rest_framework import serializers
from .utils import generate_model_id
from .models import Organisation, Project, Employee, ProjectEmployee


class BaseSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        instance.update_item(**validated_data)
        instance.refresh()


class OrganisationSerializer(BaseSerializer):
    name = serializers.CharField()
    tier = serializers.CharField()

    def create(self, validated_data):
        data = validated_data
        model_id = generate_model_id()
        data.update(
            model_id=model_id,
            pk=f"ORG",
            sk=f"ORG#{model_id}"
        )

        organisation = Organisation(**data)
        organisation.save()
        return organisation


class ProjectSerializer(BaseSerializer):
    organisation_id = serializers.CharField()
    name = serializers.CharField()
    project_type = serializers.CharField()
    status = serializers.CharField()

    def create(self, validated_data):
        data = validated_data
        model_id = generate_model_id()
        organisation_id = data['organisation_id']
        project_type = data['project_type']

        data.pop('organisation_id')

        data.update(
            model_id=model_id,
            pk=f"ORG#{organisation_id}",
            sk=f"PRO#{project_type}#{model_id}"
        )

        project = Project(**data)
        project.save()

        return project


class EmployeeSerializer(serializers.Serializer):
    organisation_id = serializers.CharField()
    name = serializers.CharField()
    date_of_birth = serializers.CharField()
    email = serializers.EmailField()

    def create(self, validated_data):
        data = validated_data
        model_id = generate_model_id()
        organisation_id = data.pop('organisation_id')

        data.update(
            model_id=model_id,
            pk=f"ORG#{organisation_id}",
            sk=f"EMP#{model_id}"
        )

        employee = Employee(**data)
        employee.save()

        return employee


class ProjectEmployeeSerializer(serializers.Serializer):
    organisation_id = serializers.CharField()
    employee_id = serializers.CharField()
    project_id = serializers.CharField()

    def create(self, validated_data):
        data = validated_data
        model_id = generate_model_id()
        date_joined = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        project_id = data.get('project_id')
        employee_id = data.get('employee_id')
        organisation_id = data.pop('organisation_id')

        data.update(
            dict(
                pk=f"#ORG{organisation_id}#PRO{project_id}",
                sk=f"#ORG{organisation_id}#EMP{employee_id}",
                model_id=model_id,
                date_joined=date_joined
            )
        )

        project_employee = ProjectEmployee(**data)
        project_employee.save()

        return project_employee
