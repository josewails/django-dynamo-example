from organisations.models import BaseModel
import boto3


def create_table():
    BaseModel.create_table(wait=True)


def delete_table():
    BaseModel.delete_table()


def update_table():
    resource = boto3.resource(
        'dynamodb',
        region_name="localhost",
        aws_access_key_id='vdaoap',
        aws_secret_access_key='y9249',
        endpoint_url='http://localhost:8080')
    table = resource.Table('django-dynamo-example')

    attribute_definitions = [
        {
            'AttributeName': 'pk',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'sk',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'model_id',
            'AttributeType': 'S'
        }

    ]

    indexes = [
        {
            "Create": {
                "IndexName": "gsi_one",
                "KeySchema": [
                    {
                        "AttributeName": "sk",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "pk",
                        "KeyType": "RANGE"
                    }
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 2,
                    "WriteCapacityUnits": 2
                }
            }
        }
    ]

    table.update(
        AttributeDefinitions=attribute_definitions,
        GlobalSecondaryIndexUpdates=indexes
    )


def run():
    create_table()
    update_table()
