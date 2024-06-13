import boto3
from boto3.dynamodb.conditions import Key, AttributeBase
import json
from src.config.utils import *


class DynamoDBConnector:
    def __init__(self, profile_name='default', **kwargs):
        sesh = boto3.Session(profile_name=profile_name)

        self._client = sesh.client('dynamodb')

    def listTables(self):
        return self._client.list_tables()

    def createTable(self, table_name, secondary_key_name='createdAt', secondary_key_type='S', **kwargs):
        id_field = getDictKey(kwargs, 'id_field')
        id_field = 'id' if id_field is None else id_field

        id_field_type = getDictKey(kwargs, 'id_field_type')
        id_field_type = 'S' if id_field_type is None else id_field_type

        res = self._client.create_table(**{
            "TableName": table_name,
            "AttributeDefinitions": [
                {"AttributeName": id_field, "AttributeType": id_field_type},
                {"AttributeName": secondary_key_name, "AttributeType": secondary_key_type}
            ],
            "KeySchema": [
                {'AttributeName': id_field, 'KeyType': 'HASH'},
                {'AttributeName': secondary_key_name, 'KeyType': 'RANGE'}
            ],
            "BillingMode": "PAY_PER_REQUEST",
            **kwargs
        })

        return res

    def scan(self, table_name):
        res = self._client.scan(TableName=table_name)

        return {
            'count': res['Count'],
            'records': res['Items']
        }

    def deleteTable(self, table_name):
        self._client.delete_table(TableName=table_name)

    def putItem(self, table_name, item):
        self._client.put_item(
            TableName=table_name,
            Item=item
        )
