import secrets

from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute


class GSIOne(GlobalSecondaryIndex):
    class Meta:
        index_name = 'gsi_one'
        write_capacity_units = 2
        read_capacity_units = 2
        projection = AllProjection()

    pk = UnicodeAttribute(null=False, range_key=True)
    sk = UnicodeAttribute(null=False, hash_key=True)


class BaseModel(Model):
    class Meta:
        table_name = 'django-dynamo-example'
        region = 'localhost'
        host = 'http://localhost:8080'
        aws_access_key_id = 'vdaoap'
        aws_secret_access_key = 'y9249'
        write_capacity_units = 10
        read_capacity_units = 10

    pk = UnicodeAttribute(null=False, hash_key=True)
    sk = UnicodeAttribute(null=False, range_key=True)
    model_id = UnicodeAttribute(null=False)

    def get_data(self):
        return dict(
            id=self.model_id
        )


class Organisation(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    name = UnicodeAttribute()
    tier = UnicodeAttribute()

    def get_data(self):
        data = super().get_data()
        data.update(dict(
            name=self.name,
            tier=self.tier
        ))
        return data


class Project(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    name = UnicodeAttribute()
    project_type = UnicodeAttribute()
    status = UnicodeAttribute()

    def get_data(self):
        data = super().get_data()
        data.update(dict(
            name=self.name,
            project_type=self.project_type,
            status=self.status
        ))

        return data


class Employee(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    name = UnicodeAttribute()
    date_of_birth = UnicodeAttribute()
    email = UnicodeAttribute()


class ProjectEmployee(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    employee_id = UnicodeAttribute()
    project_id = UnicodeAttribute()
    date_joined = UnicodeAttribute()
    gsi_one = GSIOne()

    def get_data(self):
        data = super().get_data()
        if "EMP" in self.pk:
            data.update(
                dict(
                    employee_id=self.employee_id
                )
            )

        elif "PRO" in self.pk:
            data = super().get_data()
            data.update(
                dict(
                    project_id=self.project_id
                )
            )

        data.update(
            dict(
                date_joined=self.date_joined
            )
        )

        return data
