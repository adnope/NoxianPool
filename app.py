from datetime import datetime, timezone
from flask import Flask, flash, render_template, request, redirect, session, jsonify
from config import get_supabase_client
from table.base import Player, Rank, User, Tournament, Enrollment
from table.player_repository import PlayerRepository
from table.rank_repository import RankRepository
from table.user_repository import UserRepository
from table.tournament_repository import TournamentRepository
from table.enrollment_repository import EnrollmentRepository

app = Flask(__name__)
app.secret_key = "thrill_of_the_hunt"

supabase = get_supabase_client()

player_repo = PlayerRepository(supabase)
rank_repo = RankRepository(supabase)
user_repo = UserRepository(supabase)
tournament_repo = TournamentRepository(supabase)
enrollment_repo = EnrollmentRepository(supabase) 

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
            return render_template('admin/logged_homepage.html')
    else: return render_template('common/unlogged_homepage.html')

@app.route('/tournaments', methods=['GET', 'POST'])
def view_tournaments():
    tournament_list = tournament_repo.list_ongoing_tournaments()
    tournaments = []
    for t in tournament_list:
        tournament_id = t.id
        t_name = t.name
        status = t.status
        start_date = t.start_date
        end_date = t.end_date
        number_of_players = t.number_of_players
        description = t.description
        rank_range = map_numbers_to_chars(t.allowed_ranks)

        tournaments.append({
            'id': tournament_id,
            'name': t_name,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
            'number_of_players': number_of_players,
            'description': description,
            'rank_range': rank_range
        })
    
    if session.get('is_logged_in'):
        user_id = session.get('user_id')
        user = user_repo.get_user(user_id)
        if user.role == 'player':
            return render_template('player/tournaments.html', tournaments=tournaments)
        if user.role == 'admin':
            print(1)
        if user.role == 'staff':
            print(2)

    else: return render_template('common/tournaments.html', tournaments=tournaments)


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if not session.get('is_logged_in'):
        return redirect('/login')

    user_id = session.get('user_id')
    tournament_id = request.args.get('tournament_id')

    user = user_repo.get_user(user_id)

    if not tournament_id:
        return jsonify({"message": "Tournament ID is missing"}), 400
    
    if user and (user.role == 'player'):
        try:
            tournament = tournament_repo.get_tournament(tournament_id=tournament_id)
            if not tournament:
                return jsonify({"message": "Tournament not found"}), 404

            enrollment = Enrollment(player_id=user_id, tournament_id=tournament.id)
            if enrollment_repo.get_enrollment(user_id, tournament.id):
                return jsonify({"message": "You have already enrolled in this tournament"}), 400
            else:
                enrollment_repo.upsert_enrollment(enrollment)
                return redirect('/tournaments')
        except Exception as e:
            return jsonify({"message": "Enrollment failed", "error": str(e)}), 500

    else: return jsonify({"message": "Unauthorized role"}), 403

@app.route('/profile', methods=['GET', 'POST'])
def view_profile():
    if not session.get('is_logged_in'):
        return redirect('/login')
    
    user_id = session.get('user_id')
    user = user_repo.get_user(user_id)

    if user.role == 'player':
        if request.method == 'POST':
            first_name = request.form['firstname']
            last_name = request.form['lastname']
            year_of_birth = request.form['yearOfBirth']
            country = request.form['country']
            email = request.form['email']
            phone_number = request.form['phone']
            rank = request.form['rank']
            
            updates = {
                "first_name": first_name,
                "last_name": last_name,
                "year_of_birth": year_of_birth,
                "rank_id": Rank(rank).id,
                "email": email,
                "country": country,
                "phone_number": phone_number
            }
            
            supabase.table("players").update(updates).eq("id", user_id).execute()
            return redirect("/profile")
            
        player = player_repo.get_player(user_id)
        first_name = player.first_name
        last_name = player.last_name
        year_of_birth = player.year_of_birth
        country = player.country
        email = player.email
        phone_number = player.phone_number
        rank = rank_repo.get_rank(player.rank_id).rank

        return render_template("player/profile.html", first_name=first_name, last_name=last_name,
                                year_of_birth=year_of_birth, country=country, email=email,
                                phone_number=phone_number, rank=rank)
    return None



if __name__ == '__main__':
    app.run(debug=True)