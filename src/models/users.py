from src.models.__object__ import *


class User(AppObject):
    _SEGMENT = 'aee0'
    _TABLE_NAME = 'marketeer-app-users'

    def __init__(self, db: DynamoDBConnector, first_name, last_name, email, **kwargs):
        super().__init__(db, **kwargs)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def createRecord(self, created_by=None, user_id=None):
        # Check if record exists
        users = self._db.scan(self._TABLE_NAME)

        try:
            return list(filter(lambda x: x['email'] == self.email, users))[0]

        except IndexError:
            pass

        if created_by is None:
            raise Exception(f"User ID for createdBy not provided")

        user_id = user_id if user_id is not None else self._generateID()

        self._db.putItem(
            self._TABLE_NAME,
            {
                "id": user_id,
                "firstName": self.first_name,
                "lastName": self.last_name,
                "email": self.email,
                **self.getTimestamps(created_by=created_by)
            }
        )
