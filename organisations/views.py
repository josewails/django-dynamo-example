from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrganisationSerializer
from .models import Organisation, Project, ProjectEmployee
from .mixins import ListObjectsMixin

import json


class OrganisationCreateView(APIView):
    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)

        if serializer.is_valid():
            organisation = serializer.create(serializer.validated_data)
            return Response(
                organisation.get_data(),
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                dict(
                    errors=serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )


class OrganisationListView(ListObjectsMixin, APIView):
    def get(self, request):
        last_evaluated_key = request.GET.get('last_evaluated_key', '{}')

        last_evaluated_key = json.loads(last_evaluated_key)
        print(last_evaluated_key)

        query = Organisation.scan(last_evaluated_key=last_evaluated_key, limit=10)
        print(query)
        organisations = [organisation.get_data() for organisation in query]
        return Response(dict(
            data=organisations,
            page=dict(
                last_evaluated_key=query.last_evaluated_key
            )
        ))


class ProjectListView(ListObjectsMixin, APIView):

    def get(self, request, organisation_id):
        query = Project.query(f'ORG#{organisation_id}', Project.sk.startswith('PRO'))
        projects = [project.get_data() for project in query]
        return Response(self.get_paginated_response(request, projects))


class ProjectDetailView(APIView):

    def get(self, request, organisation_id, project_type, project_id):
        project = Project.get(f"ORG#{organisation_id}", range_key=f"PRO#{project_type}#{project_id}")
        return Response(
            project.get_data()
        )


class ProjectEmployeeListView(ListObjectsMixin, APIView):

    def get(self, request, organisation_id, project_id):
        query = ProjectEmployee.query(f"#ORG{organisation_id}#PRO{project_id}")
        results = [result.get_data() for result in query]
        return Response(self.get_paginated_response(request, results))


class EmployeeProjectListView(ListObjectsMixin, APIView):

    def get(self, request, organisation_id, employee_id):
        query = ProjectEmployee.gsi_one.query(f"#ORG{organisation_id}#EMP{employee_id}")
        results = [result.get_data() for result in query]
        return Response(self.get_paginated_response(request, results))
