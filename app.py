from datetime import datetime, timezone
from flask import Flask, flash, render_template, request, redirect, session
from config import get_supabase_client
from table.base import Player, Rank, User
from table.player_repository import PlayerRepository
from table.rank_repository import RankRepository
from table.user_repository import UserRepository

app = Flask(__name__)

isLoggedIn = False

supabase = get_supabase_client()

player_repo = PlayerRepository(supabase)
rank_repo = RankRepository(supabase)
user_repo = UserRepository(supabase)

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

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#         user = cur.fetchall()
#         cur.close()

#         if user:
#             session['user_id'] = user[0]
#             flash('Login successful!', 'success')
#             return redirect('/')
#         else:
#             flash('Invalid email or password.', 'danger')
#     return render_template('common/login.html')

@app.route('/', methods=['GET'])
def home():
    return render_template('player/unlogged_homepage.html')

@app.route('/tournaments', methods=['GET', 'POST'])
def view_tournaments():

    return render_template('common/tournaments.html', t_name='CG Open')

if __name__ == '__main__':
    app.run(debug=True)