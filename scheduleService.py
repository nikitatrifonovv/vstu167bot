import uuid
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
    init_db()

    table = dynamodb.Table(TABLE_NAME)

    return table.scan()['Items']


def save_lesson(date, interval_start, interval_stop, lesson_name, auditory,teacher_name):
    init_db()
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(
        Item={
            'id': str(uuid.uuid4()),
            'date': date,
            'interval_start': interval_start,
            'interval_stop': interval_stop,
            'lesson_name': lesson_name,
            'auditory': auditory,
            'teacher_name': teacher_name
        }
    )


def delete_lesson(_id):
    init_db()
    table = dynamodb.Table(TABLE_NAME)
    table.delete_item(Key={'id': str(_id)})


def init_db():
    try:
        dynamodb.create_table(
            TableName=TABLE_NAME,
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
                {'AttributeName': 'auditory', 'AttributeType': 'S'},
                {'AttributeName': 'teacher_name', 'AttributeType': 'S'}
            ]
        )
    except Exception as ignore: pass