from supabase import Client
from typing import Optional, List

from table.base import User

class UserRepository:
    def __init__(self, client: Client):
        self.client = client

    def upsert_user(self, user: User):
        self.client.table("users").upsert({
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "created_at": user.created_at
        }).execute()

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID."""
        data = self.client.table("users").select("*").eq("id", user_id).single().execute()
        return User(
            id=data["id"],
            username=data["username"],
            password=data["password"],
            role=data["role"],
            created_at=data["created_at"]
        ) if data else None
    
    def get_user_id_from_username(self, username) -> Optional[User]:
        data = self.client.table("users").select("*").eq("username", username).single().execute().data
        print(data)
        return data['id']

    def delete_user(self, user_id: int):
        """Delete a user by their ID."""
        self.client.table("users").delete().eq("id", user_id).execute()

    def list_users(self) -> List[User]:
        """Retrieve a list of all users."""
        data = self.client.table("users").select("*").execute()
        return [
            User(
                id=item["id"],
                username=item["username"],
                password=item["password"],
                role=item["role"],
                created_at=item["created_at"]
            ) for item in data
        ]
