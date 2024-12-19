from typing import List, Optional
from table.base import Tournament
from supabase import Client

class TournamentRepository:
    def __init__(self, client: Client):
        self.client = client

    def upsert_tournament(self, tournament: Tournament):
        """Insert or update a tournament."""
        self.client.table("tournaments").upsert({
            "id": tournament.id,
            "name": tournament.name,
            "description": tournament.description,
            "creator_id": tournament.creator_id,
            "created_at": tournament.created_at,
            "status": tournament.status,
            "start_date": tournament.start_date,
            "end_date": tournament.end_date,
            "number_of_players": tournament.number_of_players,
            "allowed_ranks": tournament.allowed_ranks,
            "play_style": tournament.play_style,
        }).execute()

    def get_tournament(self, tournament_id: int) -> Optional[Tournament]:
        """Retrieve a tournament by its ID."""
        data = self.client.table("tournaments").select("*").eq("id", tournament_id).single().execute()
        if data:
            return Tournament(
                id=data["id"],
                name=data["name"],
                description=data["description"],
                creator_id=data["creator_id"],
                created_at=data["created_at"],
                status=data["status"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                number_of_players=data["number_of_players"],
                allowed_ranks=data["allowed_ranks"],
                play_style=data["play_style"],
            )
        return None

    def delete_tournament(self, tournament_id: int):
        """Delete a tournament by its ID."""
        self.client.table("tournaments").delete().eq("id", tournament_id).execute()

    def list_tournaments(self) -> List[Tournament]:
        """List all tournaments."""
        data = self.client.table("tournaments").select("*").execute()
        return [
            Tournament(
                id=item["id"],
                name=item["name"],
                description=item["description"],
                creator_id=item["creator_id"],
                created_at=item["created_at"],
                status=item["status"],
                start_date=item["start_date"],
                end_date=item["end_date"],
                number_of_players=item["number_of_players"],
                allowed_ranks=item["allowed_ranks"],
                play_style=item["play_style"],
            )
            for item in data
        ]