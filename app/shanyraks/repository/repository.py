from datetime import datetime
from typing import List, Any
from typing import BinaryIO

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

    def add_shanyrak_post(self, shanyrak_id: str, user_id: str, media: str) -> dict | None:
        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$push": {
                    "media": media,
                }
            },
        )

        return result

    def delete_shanyrak_post(self, shanyrak_id: str, user_id: str, media: str) -> dict | None:
        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$pull": {
                    "media": media,
                }
            },
        )

        return result

    def add_comment(self, shanyrak_id: str, user_id: str, comment: str) -> dict | None:

        payload = {
            "id": ObjectId(),
            "content": comment,
            "created_at": datetime.now(),
            "author_id": ObjectId(user_id)
        }

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$push": {
                    "comment": payload,
                }
            },
        )

        return result

    def update_comment(self, shanyrak_id: str, user_id: str, comment_id: str, comment: str) -> dict | None:

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "comment.author_id": ObjectId(user_id), "comment.id": ObjectId(comment_id)},
            update={
                "$set": {
                    "comment.$.content": comment,
                }
            },
        )

        return result

    def delete_comment(self, shanyrak_id: str, user_id: str, comment_id: str) -> dict | None:
        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$pull": {
                    "comment": {
                        "id": ObjectId(comment_id),
                        "author_id": ObjectId(user_id),
                    },
                }
            },
        )

        return result

