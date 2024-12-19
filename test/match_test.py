from config import get_supabase_client
from table.base import Match
from table.match_repository import MatchRepository

supabase = get_supabase_client()
repo = MatchRepository(supabase)


