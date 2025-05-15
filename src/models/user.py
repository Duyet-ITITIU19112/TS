class User:
    def __init__(self, user_id, name, email, access_token):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.access_token = access_token

    @classmethod
    def from_ms_graph(cls, user_data, access_token):
        return cls(
            user_id=user_data.get("id"),
            name=user_data.get("displayName"),
            email=user_data.get("userPrincipalName"),
            access_token=access_token
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "access_token": self.access_token
        }
