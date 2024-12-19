class Rank:
    rank_map = {chr(i + 65): i + 1 for i in range(9)}
    def __init__(self, rank):
        self.id = self.rank_map[rank]
        self.rank = rank
        
class Player:
    def __init__(self, id, first_name, last_name, rank_id, year_of_birth, 
                 citizen_identification, email, phone_number, country):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.rank_id = rank_id
        self.year_of_birth = year_of_birth
        self.citizen_identification = citizen_identification
        self.email = email
        self.phone_number = phone_number
        self.country = country


class User:
    def __init__(self, id, username, password, role, created_at):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.created_at = created_at


class Staff:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


class Tournament:
    def __init__(self, id, name, description, creator_id, created_at, status, 
                 start_date, end_date, number_of_players, allowed_ranks, play_style):
        self.id = id
        self.name = name
        self.description = description
        self.creator_id = creator_id
        self.created_at = created_at
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_players = number_of_players
        self.allowed_ranks = allowed_ranks
        self.play_style = play_style


class Match:
    def __init__(self, first_player_id, second_player_id, tournament_id):
        self.first_player_id = first_player_id
        self.second_player_id = second_player_id
        self.tournament_id = tournament_id