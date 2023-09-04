import uuid
import boto3
import secrets

TABLE_NAME = 'users'

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=secrets.YDB_USER_STORAGE_URL,
    region_name='ru-central1',
    aws_access_key_id=secrets.YDB_ACCESS_KEY_ID,
    aws_secret_access_key=secrets.YDB_SECRET_ACCESS_KEY
)


def is_admin(id):
    init_db()
    table = dynamodb.Table(TABLE_NAME)
    item = table.get_item(Key={'id': str(id)})
    if 'Item' in item:
        if item['Item']['role'] == 'admin' or "god":
            return True
    return False


def contains(id):
    init_db()
    table = dynamodb.Table(TABLE_NAME)
    item = table.get_item(Key={'id': str(id)})
    if 'Item' in item:
        if item['Item']['id'] == str(id):
            return True
    return False


def save_user(id, username, role):
    init_db()
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(
        Item={
            'id': str(id),
            'username': username,
            'role': role
        }
    )


def load_all():
    init_db()

    table = dynamodb.Table(TABLE_NAME)

    return table.scan()['Items']

def init_db():
    try:
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'username', 'AttributeType': 'S'},
                {'AttributeName': 'role', 'AttributeType': 'S'}
            ]
        )
    except Exception as ignore: pass