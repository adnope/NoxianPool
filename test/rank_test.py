from config import get_supabase_client
from table.base import Rank
from table.rank_repository import RankRepository

supabase = get_supabase_client()
repo = RankRepository(supabase)

rank = Rank(123, "A")
repo.upsert_rank(rank)
repo.delete_rank(123)