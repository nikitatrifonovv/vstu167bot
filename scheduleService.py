import boto3

import secrets

TABLE_NAME = 'schedule'

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=secrets.YDB_USER_STORAGE_URL,
    region_name='ru-central1',
    aws_access_key_id=secrets.YDB_ACCESS_KEY_ID,
    aws_secret_access_key=secrets.YDB_SECRET_ACCESS_KEY
)


def load_all():
    try:
        create_db()
    except Exception as ignore:
        pass

    table = dynamodb.Table(TABLE_NAME)

    return table.scan()['Items']


def create_db():
    dynamodb.create_table(
        TableName='schedule',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
            {'AttributeName': 'date', 'AttributeType': 'S'},
            {'AttributeName': 'interval_start', 'AttributeType': 'S'},
            {'AttributeName': 'interval_stop', 'AttributeType': 'S'},
            {'AttributeName': 'lesson_name', 'AttributeType': 'S'},
            {'AttributeName': 'teacher_name', 'AttributeType': 'S'}
        ]
    )
