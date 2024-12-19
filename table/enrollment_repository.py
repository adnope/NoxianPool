from typing import Optional, List
from table.base import Enrollment
from supabase import Client

class EnrollmentRepository:
    def __init__(self, client: Client):
        self.client = client

    def upsert_enrollment(self, enrollment: Enrollment):
        self.client.table("enrollments").upsert({
            "player_id": enrollment.player_id,
            "tournament_id": enrollment.tournament_id
        }).execute()

    def get_enrollment(self, player_id:int, tournament_id: int) -> Optional[Enrollment]:
        data = self.client.table("enrollments").select("*").eq("player_id", player_id).eq("tournament_id", tournament_id).execute().data
        if data:
            return Enrollment(
                player_id=data["player_id"],
                tournament_id=data["tournament_id"]
            )
        return None

    def delete_enrollment(self, player_id: int, tournament_id: int):
        self.client.table("tournaments").delete().eq("tournament_id", tournament_id).eq("player_id", player_id).execute()

    def list_enrollments(self) -> List[Enrollment]:
        data = self.client.table("enrollments").select("*").execute().data
        return [
            Enrollment(
                player_id=item["player_id"],
                tournament_id=item["tournament_id"]
            )
            for item in data
        ]
