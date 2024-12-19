from typing import List, Optional
from supabase import Client
from table.base import Staff

class StaffRepository:
    def __init__(self, client: Client):
        self.client = client

    def upsert_staff(self, staff: Staff):
        """
        Inserts or updates a staff record in the database.
        """
        self.client.table("staffs").upsert({
            "id": staff.id,
            "first_name": staff.first_name,
            "last_name": staff.last_name
        }).execute()

    def get_staff(self, staff_id: int) -> Optional[Staff]:
        """
        Fetches a staff record by ID.
        """
        data = self.client.table("staffs").select("*").eq("id", staff_id).single().execute()
        return Staff(id=data["id"], first_name=data["first_name"], last_name=data["last_name"]) if data else None

    def delete_staff(self, staff_id: int):
        """
        Deletes a staff record by ID.
        """
        self.client.table("staffs").delete().eq("id", staff_id).execute()

    def list_staffs(self) -> List[Staff]:
        """
        Lists all staff records in the database.
        """
        data = self.client.table("staffs").select("*").execute()
        return [Staff(id=item["id"], first_name=item["first_name"], last_name=item["last_name"]) for item in data]
