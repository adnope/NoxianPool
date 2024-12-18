from config import get_supabase_client
from table.base import Player, Rank
from table.player_repository import PlayerRepository
from table.rank_repository import RankRepository

supabase = get_supabase_client()
repo = PlayerRepository(supabase)
rankrepo = RankRepository(supabase)

rank = Rank(123, "A")

rankrepo.upsert_rank(rank)

player = Player(
    id=1,
    first_name="John",
    last_name="Doe",
    rank_id=123,
    year_of_birth=1990,
    citizen_identification="123456789",
    email="john.doe@example.com",
    phone_number="555-1234",
    country="USA"
)

repo.upsert_player(player)

retrieved_player = repo.get_player(1)

repo.delete_player(1)