from datetime import datetime
from typing import List, Any

from bson.objectid import ObjectId
from pymongo.database import Database


from pymongo.results import DeleteResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_pater(self, user_id, input: dict[str, Any]):
        input["user_id"] = ObjectId(user_id)

        temp = self.database["shanyraks"].insert_one(input)
        print(temp.inserted_id)

    def get_shanyrak(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def update_shanyrak(self, shanyrak_id: str, user_id: str, input: dict[str, Any]):
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": input,
            },
        )

    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )