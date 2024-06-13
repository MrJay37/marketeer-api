from src.config import getDictKey, DynamoDBConnector, getNow
from uuid import uuid4


class AppObject:
    _SEGMENT = ''

    def __init__(self, db: DynamoDBConnector, **kwargs):
        self._db = db

        self.id = getDictKey(kwargs, 'id')
        self.created_at = getDictKey(kwargs, 'createdAt')
        self.created_by = getDictKey(kwargs, 'createdBy')
        self.modified_at = getDictKey(kwargs, 'modifiedAt')
        self.modified_by = getDictKey(kwargs, 'modifiedBy')

    def _generateID(self):
        obj_id = str(uuid4()).split('-')
        return '-'.join([obj_id[0], self._SEGMENT, *obj_id[2:]])

    @staticmethod
    def getTimestamps(created_at=None, created_by=None, modified_at=None, modified_by=None):
        timestamps = {
            "created_at": created_at,
            "created_by": created_by,
            "modified_at": modified_at,
            "modified_by": modified_by
        }

        if created_by is not None and created_at is None:
            timestamps['created_by'] = getNow()

        if modified_by is not None and modified_at is None:
            timestamps['modified_at'] = getNow()

        return timestamps
