from supabase import Client
from typing import Optional, List

from table.base import Rank

class RankRepository:
    def __init__(self, client: Client):
        self.client = client

    def upsert_rank(self, rank: Rank):
        self.client.table("ranks").upsert({"id": rank.id, "rank": rank.rank}).execute()

    def get_rank(self, rank_id: int) -> Optional[Rank]:
        data = self.client.table("ranks").select("*").eq("id", rank_id).single().execute().data
        return Rank(data["rank"]) if data else None

    def delete_rank(self, rank_id: int):
        self.client.table("ranks").delete().eq("id", rank_id).execute()

    def list_ranks(self) -> List[Rank]:
        data = self.client.table("ranks").select("*").execute().data
        return [item["rank"] for item in data]