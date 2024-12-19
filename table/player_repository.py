from supabase import Client
from typing import List, Optional
from table.base import Player

class PlayerRepository:
    def __init__(self, client: Client):
        self.client = client

    def upsert_player(self, player: Player):
        """
        Insert or update a player in the database.
        """
        self.client.table("players").upsert({
            "id": player.id,
            "first_name": player.first_name,
            "last_name": player.last_name,
            "rank_id": player.rank_id,
            "year_of_birth": player.year_of_birth,
            "citizen_identification": player.citizen_identification,
            "email": player.email,
            "phone_number": player.phone_number,
            "country": player.country
        }).execute()

    def get_player(self, player_id: int) -> Optional[Player]:
        """
        Retrieve a player by their ID.
        """
        data = self.client.table("players").select("*").eq("id", player_id).single().execute()
        return Player(
            id=data["id"],
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            rank_id=data["rank_id"],
            year_of_birth=data["year_of_birth"],
            citizen_identification=data["citizen_identification"],
            email=data.get("email"),
            phone_number=data["phone_number"],
            country=data["country"]
        ) if data else None

    def delete_player(self, player_id: int):
        """
        Delete a player by their ID.
        """
        self.client.table("players").delete().eq("id", player_id).execute()

    def list_players(self) -> List[Player]:
        """
        Retrieve all players.
        """
        data = self.client.table("players").select("*").execute()
        return [
            Player(
                id=item["id"],
                first_name=item["first_name"],
                last_name=item.get("last_name"),
                rank_id=item["rank_id"],
                year_of_birth=item["year_of_birth"],
                citizen_identification=item["citizen_identification"],
                email=item.get("email"),
                phone_number=item["phone_number"],
                country=item["country"]
            ) for item in data
        ]
