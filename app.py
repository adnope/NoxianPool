from datetime import datetime, timezone
from flask import Flask, flash, render_template, request, redirect, session
from config import get_supabase_client
from table.base import Player, Rank, User, Tournament
from table.player_repository import PlayerRepository
from table.rank_repository import RankRepository
from table.user_repository import UserRepository
from table.tournament_repository import TournamentRepository

app = Flask(__name__)
app.secret_key = "thrill_of_the_hunt"

supabase = get_supabase_client()

player_repo = PlayerRepository(supabase)
rank_repo = RankRepository(supabase)
user_repo = UserRepository(supabase)
tournament_repo = TournamentRepository(supabase)

def map_numbers_to_chars(numbers):
    number_to_char = {
        1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 
        7: 'G', 8: 'H', 9: 'I'
    }
    
    char_list = [number_to_char[num] for num in numbers]
    
    return ' - '.join(char_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User("", username, password, "player", str(datetime.now(timezone.utc)))
        user_repo.upsert_user(user)

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        rank_id = Rank(request.form["rank"]).id
        year_of_birth = request.form['year_of_birth']
        citizen_id = request.form['citizen_id']
        email = request.form['email']
        phone_number = request.form['phone_number']
        country = request.form['country']

        user_id = user_repo.get_user_id_from_username(username)
        print(user_id)

        player = Player(user_id, first_name, last_name, rank_id, year_of_birth, citizen_id, email, phone_number, country)
        player_repo.upsert_player(player)

        print("registration successfully")
        return redirect('/login')
    return render_template('player/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = user_repo.get_user(user_repo.get_user_id_from_username(username))
        password_check = user.password

        if user and (password == password_check):
            session['is_logged_in'] = True
            session['user_id'] = user.id
            return redirect('/')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('common/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/', methods=['GET'])
def home():
    if session.get('is_logged_in'): 
        user_id = session.get('user_id')
        user = user_repo.get_user(user_id)
        if user.role == 'player':
            print('player logged in')
            return render_template('player/logged_homepage.html')
        if user.role == 'staff':
            print('staff logged in')
        if user.role == 'admin':
            print('admin logged in')
    else: return render_template('common/unlogged_homepage.html')

@app.route('/tournaments', methods=['GET', 'POST'])
def view_tournaments():
    if session.get('is_logged_in'): 
        user_id = session.get('user_id')
        user = user_repo.get_user(user_id)
        if user.role == 'player':
            tournament_list = tournament_repo.list_ongoing_tournaments()
            tournaments = []
            for t in tournament_list:
                t_name = t.name
                status = t.status
                start_date = t.start_date
                end_date = t.end_date
                number_of_players = t.number_of_players
                description = t.description
                rank_range = map_numbers_to_chars(t.allowed_ranks)

                tournaments.append({
                    'name': t_name,
                    'status': status,
                    'start_date': start_date,
                    'end_date': end_date,
                    'number_of_players': number_of_players,
                    'description': description,
                    'rank_range': rank_range
                })
            return render_template('player/tournaments.html', tournaments=tournaments)
        if user.role == 'staff':
            print('')
        if user.role == 'admin':
            print('')
    else:
        tournament_list = tournament_repo.list_ongoing_tournaments()
        tournaments = []
        for t in tournament_list:
            t_name = t.name
            status = t.status
            start_date = t.start_date
            end_date = t.end_date
            number_of_players = t.number_of_players
            description = t.description
            rank_range = map_numbers_to_chars(t.allowed_ranks)

            tournaments.append({
                'name': t_name,
                'status': status,
                'start_date': start_date,
                'end_date': end_date,
                'number_of_players': number_of_players,
                'description': description,
                'rank_range': rank_range
            })
        return render_template('common/tournaments.html', tournaments=tournaments)

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        if session.get('is_logged_in'):
            user_id = session.get('user_id')
            user = user_repo.get_user(user_id)
            if (user.role == 'player'):

        else: return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)