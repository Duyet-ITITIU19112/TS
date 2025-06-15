# class User:
#     def __init__(self, user_id, name, email, access_token):
#         self.user_id = user_id
#         self.name = name
#         self.email = email
#         self.access_token = access_token
#
#     @classmethod
#     def from_ms_graph(cls, user_data, access_token):
#         return cls(
#             user_id=user_data.get("id"),
#             name=user_data.get("displayName"),
#             email=user_data.get("userPrincipalName"),
#             access_token=access_token
#         )
#
#     def to_dict(self):
#         return {
#             "user_id": self.user_id,
#             "name": self.name,
#             "email": self.email,
#             "access_token": self.access_token
#         }


from datetime import datetime
from src.models import db

from datetime import datetime
from src.models import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    ms_id = db.Column(db.String(64), unique=True, nullable=False)       # <-- add this
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    access_token = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text, nullable=True)
    token_expires = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


