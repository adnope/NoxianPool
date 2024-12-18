from typing import Optional, List
from supabase import Client
from table.base import Match

class MatchRepository:
    def __init__(self, client: Client):
        self.client = client

    def upsert_match(self, match: Match):
        self.client.table("matches").upsert({
            "first_player_id": match.first_player_id,
            "second_player_id": match.second_player_id,
            "tournament_id": match.tournament_id,
        }).execute()

    def get_match(self, first_player_id: int, second_player_id: int, tournament_id: int) -> Optional[Match]:
        data = (
            self.client.table("matches")
            .select("*")
            .eq("first_player_id", first_player_id)
            .eq("second_player_id", second_player_id)
            .eq("tournament_id", tournament_id)
            .single()
            .execute()
        )
        if data:
            return Match(
                first_player_id=data["first_player_id"],
                second_player_id=data["second_player_id"],
                tournament_id=data["tournament_id"],
            )
        return None

    def delete_match(self, first_player_id: int, second_player_id: int, tournament_id: int):
        self.client.table("matches").delete() \
            .eq("first_player_id", first_player_id) \
            .eq("second_player_id", second_player_id) \
            .eq("tournament_id", tournament_id).execute()

    def list_matches(self) -> List[Match]:
        data = self.client.table("matches").select("*").execute()
        return [
            Match(
                first_player_id=item["first_player_id"],
                second_player_id=item["second_player_id"],
                tournament_id=item["tournament_id"],
            )
            for item in data
        ]
