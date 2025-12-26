from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit, join_room
import uuid
import random
import sqlite3
import os
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'dev-secret-key-change-in-production')
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Game data storage
games = {}

# Sample questions (you can fetch these from a database or API)
quiz_questions = [
    # Math Questions (25)
    {
        "question": "What is 5 + 3?",
        "answer": "8",
        "category": "math"
    },
    {
        "question": "What is the square root of 16?",
        "answer": "4",
        "category": "math"
    },
    {
        "question": "What is 7 * 6?",
        "answer": "42",
        "category": "math"
    },
    {
        "question": "What is the sum of the angles in a triangle?",
        "answer": "180",
        "category": "math"
    },
    {
        "question": "What is 12 divided by 4?",
        "answer": "3",
        "category": "math"
    },
    {
        "question": "What is 9 squared?",
        "answer": "81",
        "category": "math"
    },
    {
        "question": "What is 15 - 7?",
        "answer": "8",
        "category": "math"
    },
    {
        "question": "What is 3.14 commonly known as?",
        "answer": "Pi",
        "category": "math"
    },
    {
        "question": "What is 10% of 50?",
        "answer": "5",
        "category": "math"
    },
    {
        "question":
        "What is the next number in the sequence: 2, 4, 6, 8, ...?",
        "answer": "10",
        "category": "math"
    },
    {
        "question":
        "What is the area of a rectangle with length 5 and width 4?",
        "answer": "20",
        "category": "math"
    },
    {
        "question": "What is the value of 2^5?",
        "answer": "32",
        "category": "math"
    },
    {
        "question": "What is the perimeter of a square with side length 3?",
        "answer": "12",
        "category": "math"
    },
    {
        "question": "What is 20 multiplied by 5?",
        "answer": "100",
        "category": "math"
    },
    {
        "question": "What is the cube root of 27?",
        "answer": "3",
        "category": "math"
    },
    {
        "question": "What is 100 divided by 25?",
        "answer": "4",
        "category": "math"
    },
    {
        "question": "What is the sum of 45 and 55?",
        "answer": "100",
        "category": "math"
    },
    {
        "question": "What is the difference between 100 and 47?",
        "answer": "53",
        "category": "math"
    },
    {
        "question": "What is the product of 9 and 7?",
        "answer": "63",
        "category": "math"
    },
    {
        "question": "What is the value of 5 factorial (5!)?",
        "answer": "120",
        "category": "math"
    },
    {
        "question": "What is the square of 12?",
        "answer": "144",
        "category": "math"
    },
    {
        "question": "What is 3/4 as a decimal?",
        "answer": "0.75",
        "category": "math"
    },
    {
        "question": "What is the greatest common divisor of 12 and 18?",
        "answer": "6",
        "category": "math"
    },
    {
        "question": "What is the least common multiple of 4 and 6?",
        "answer": "12",
        "category": "math"
    },
    {
        "question": "What is the value of 8 + 9 * 2?",
        "answer": "26",
        "category": "math"
    },

    # Geography Questions (25)
    {
        "question": "What is the capital of France?",
        "answer": "Paris",
        "category": "geography"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "answer": "Pacific Ocean",
        "category": "geography"
    },
    {
        "question": "What is the primary language spoken in Brazil?",
        "answer": "Portuguese",
        "category": "geography"
    },
    {
        "question": "What is the capital of Japan?",
        "answer": "Tokyo",
        "category": "geography"
    },
    {
        "question": "What is the longest river in the world?",
        "answer": "Nile",
        "category": "geography"
    },
    {
        "question": "What is the smallest country in the world?",
        "answer": "Vatican City",
        "category": "geography"
    },
    {
        "question": "What is the capital of Canada?",
        "answer": "Ottawa",
        "category": "geography"
    },
    {
        "question": "What is the largest desert in the world?",
        "answer": "Sahara",
        "category": "geography"
    },
    {
        "question": "What is the capital of Australia?",
        "answer": "Canberra",
        "category": "geography"
    },
    {
        "question": "What is the highest mountain in the world?",
        "answer": "Mount Everest",
        "category": "geography"
    },
    {
        "question": "What is the capital of Italy?",
        "answer": "Rome",
        "category": "geography"
    },
    {
        "question": "What is the largest country by land area?",
        "answer": "Russia",
        "category": "geography"
    },
    {
        "question": "What is the capital of Germany?",
        "answer": "Berlin",
        "category": "geography"
    },
    {
        "question": "What is the capital of China?",
        "answer": "Beijing",
        "category": "geography"
    },
    {
        "question": "What is the capital of India?",
        "answer": "New Delhi",
        "category": "geography"
    },
    {
        "question": "What is the capital of Spain?",
        "answer": "Madrid",
        "category": "geography"
    },
    {
        "question": "What is the capital of Argentina?",
        "answer": "Buenos Aires",
        "category": "geography"
    },
    {
        "question": "What is the capital of South Africa?",
        "answer": "Pretoria",
        "category": "geography"
    },
    {
        "question": "What is the capital of Egypt?",
        "answer": "Cairo",
        "category": "geography"
    },
    {
        "question": "What is the capital of Mexico?",
        "answer": "Mexico City",
        "category": "geography"
    },
    {
        "question": "What is the capital of Russia?",
        "answer": "Moscow",
        "category": "geography"
    },
    {
        "question": "What is the capital of the United Kingdom?",
        "answer": "London",
        "category": "geography"
    },
    {
        "question": "What is the capital of South Korea?",
        "answer": "Seoul",
        "category": "geography"
    },
    {
        "question": "What is the capital of Thailand?",
        "answer": "Bangkok",
        "category": "geography"
    },
    {
        "question": "What is the capital of Brazil?",
        "answer": "Brasília",
        "category": "geography"
    },

    # Science Questions (25)
    {
        "question": "What is the chemical symbol for water?",
        "answer": "H2O",
        "category": "science"
    },
    {
        "question": "What planet is known as the Red Planet?",
        "answer": "Mars",
        "category": "science"
    },
    {
        "question": "Who discovered penicillin?",
        "answer": "Alexander Fleming",
        "category": "science"
    },
    {
        "question": "What is the powerhouse of the cell?",
        "answer": "Mitochondria",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for gold?",
        "answer": "Au",
        "category": "science"
    },
    {
        "question": "What is the closest star to Earth?",
        "answer": "Sun",
        "category": "science"
    },
    {
        "question": "What is the atomic number of hydrogen?",
        "answer": "1",
        "category": "science"
    },
    {
        "question": "What is the speed of light?",
        "answer": "299,792 km/s",
        "category": "science"
    },
    {
        "question": "What is the chemical formula for table salt?",
        "answer": "NaCl",
        "category": "science"
    },
    {
        "question": "What is the largest planet in the solar system?",
        "answer": "Jupiter",
        "category": "science"
    },
    {
        "question": "What is the process by which plants make food?",
        "answer": "Photosynthesis",
        "category": "science"
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "answer": "Diamond",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for oxygen?",
        "answer": "O",
        "category": "science"
    },
    {
        "question": "What is the unit of electrical resistance?",
        "answer": "Ohm",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for carbon?",
        "answer": "C",
        "category": "science"
    },
    {
        "question": "What is the freezing point of water in Celsius?",
        "answer": "0",
        "category": "science"
    },
    {
        "question": "What is the boiling point of water in Celsius?",
        "answer": "100",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for silver?",
        "answer": "Ag",
        "category": "science"
    },
    {
        "question": "What is the study of fossils called?",
        "answer": "Paleontology",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for iron?",
        "answer": "Fe",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for sodium?",
        "answer": "Na",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for potassium?",
        "answer": "K",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for nitrogen?",
        "answer": "N",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for helium?",
        "answer": "He",
        "category": "science"
    },
    {
        "question": "What is the chemical symbol for calcium?",
        "answer": "Ca",
        "category": "science"
    },

    # History Questions (25)
    {
        "question": "Who was the first President of the United States?",
        "answer": "George Washington",
        "category": "history"
    },
    {
        "question": "What year did the Titanic sink?",
        "answer": "1912",
        "category": "history"
    },
    {
        "question":
        "Who was the leader of the Soviet Union during World War II?",
        "answer": "Joseph Stalin",
        "category": "history"
    },
    {
        "question": "What year did World War I begin?",
        "answer": "1914",
        "category": "history"
    },
    {
        "question": "Who wrote the Declaration of Independence?",
        "answer": "Thomas Jefferson",
        "category": "history"
    },
    {
        "question": "What year did the Berlin Wall fall?",
        "answer": "1989",
        "category": "history"
    },
    {
        "question": "Who was the first woman to fly solo across the Atlantic?",
        "answer": "Amelia Earhart",
        "category": "history"
    },
    {
        "question": "What year did the United States land on the moon?",
        "answer": "1969",
        "category": "history"
    },
    {
        "question": "Who was the first emperor of Rome?",
        "answer": "Augustus",
        "category": "history"
    },
    {
        "question": "What year did the American Civil War end?",
        "answer": "1865",
        "category": "history"
    },
    {
        "question":
        "Who was the first female Prime Minister of the United Kingdom?",
        "answer": "Margaret Thatcher",
        "category": "history"
    },
    {
        "question": "What year did the French Revolution begin?",
        "answer": "1789",
        "category": "history"
    },
    {
        "question": "Who was the first President of the Russian Federation?",
        "answer": "Boris Yeltsin",
        "category": "history"
    },
    {
        "question": "What year did the Cold War end?",
        "answer": "1991",
        "category": "history"
    },
    {
        "question":
        "Who was the first African American President of the United States?",
        "answer": "Barack Obama",
        "category": "history"
    },
    {
        "question": "What year did the Industrial Revolution begin?",
        "answer": "1760",
        "category": "history"
    },
    {
        "question": "Who was the first explorer to circumnavigate the globe?",
        "answer": "Ferdinand Magellan",
        "category": "history"
    },
    {
        "question": "What year did the United States declare independence?",
        "answer": "1776",
        "category": "history"
    },
    {
        "question": "Who was the first female pharaoh of Egypt?",
        "answer": "Hatshepsut",
        "category": "history"
    },
    {
        "question": "What year did the Renaissance begin?",
        "answer": "14th century",
        "category": "history"
    },
    {
        "question":
        "Who was the first President of South Africa after apartheid?",
        "answer": "Nelson Mandela",
        "category": "history"
    },
    {
        "question": "What year did the Black Death pandemic occur?",
        "answer": "1347",
        "category": "history"
    },
    {
        "question": "Who was the first European to reach India by sea?",
        "answer": "Vasco da Gama",
        "category": "history"
    },
    {
        "question": "What year did the American Revolutionary War begin?",
        "answer": "1775",
        "category": "history"
    },
    {
        "question": "Who was the first female astronaut?",
        "answer": "Valentina Tereshkova",
        "category": "history"
    },

    # Test Questions (10)
    {
        "question": "What is the capital of France?",
        "answer": "Paris",
        "category": "test"
    },
    {
        "question": "What year did the Titanic sink?",
        "answer": "1912",
        "category": "test"
    },
    {
        "question": "What is the capital of Italy?",
        "answer": "Rome",
        "category": "test"
    },
    {
        "question": "What year did World War I begin?",
        "answer": "1914",
        "category": "test"
    },
    {
        "question": "What is 3.14 commonly known as?",
        "answer": "Pi",
        "category": "test"
    },
    {
        "question": "Square root of 16",
        "answer": "4",
        "category": "test"
    },
    {
        "question": "7 + 7",
        "answer": "14",
        "category": "test"
    },
]


# Database setup
def init_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0

            )
        """)
        conn.commit()


init_db()


# Render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?",
                           (username, ))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['user'] = user[1]
                flash("Login successful!", "success")
                if remember:
                    session.permanent = True  # Keep the user logged in
                return redirect(url_for('index'))
            else:
                error = "Invalid username or password."

    return render_template('login.html', error=error)


# Register a new user
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return redirect(url_for('login'))

    hashed_password = generate_password_hash(password)

    try:
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
    except sqlite3.IntegrityError:
        flash("Username already exists.", "error")

    return redirect(url_for('login'))


# Logout user
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/select_category')
def select_category():
    return render_template('select_category.html')


@app.route('/create_game', methods=['POST'])
def create_game():
    data = request.get_json()
    category = data.get(
        'category')  # Get the selected category from the request
    game_id = str(uuid.uuid4())[:8]  # Generate a unique game ID
    games[game_id] = {
        'board': [''] * 9,
        'players': {},
        'question':
        get_new_question(category),  # Pass the category to get_new_question
        'streaks': {
            'X': 0,
            'O': 0
        },
        'eligible_player': None,
        'attempts': {
            'X': False,
            'O': False
        },
        'category': category  # Store the selected category in the game state
    }
    return jsonify({'game_id': game_id})


@app.route('/create_game_classic', methods=['POST'])
def create_game_classic():
    game_id = str(uuid.uuid4())[:8]
    games[game_id] = {'board': [''] * 9, 'current_turn': 'X', 'players': {}}
    return jsonify({'game_id': game_id})


@app.route('/join_game_classic/<game_id>')
def join_game_classic(game_id):
    if game_id in games:
        return render_template('classic_game.html', game_id=game_id)
    return "Game not found", 404


@socketio.on('join_classic')
def on_join_classic(data):
    game_id = data['game_id']
    join_room(game_id)

    # Assign player roles
    game = games[game_id]
    if len(game['players']) == 0:
        role = 'X'
        game['players']['X'] = request.sid
    elif len(game['players']) == 1:
        role = 'O'
        game['players']['O'] = request.sid
    else:
        role = None  # If the game is full, no role is assigned

    # Notify the client about their role
    emit('player_role', {'role': role}, room=request.sid)

    # Broadcast the current game state
    emit('update_board', game, room=game_id)


@app.route('/join_game/<game_id>')
def join_game(game_id):
    if game_id in games:
        return render_template('game.html', game_id=game_id)
    return "Game not found", 404


@socketio.on('join')
def on_join(data):
    game_id = data['game_id']
    join_room(game_id)  # Join the game room

    game = games[game_id]
    username = session.get('user',
                           'Player')  # Get the username from the session

    if len(game['players']) == 0:
        role = 'X'  # First player to join gets 'X'
        game['players']['X'] = {'sid': request.sid, 'username': username}
    elif len(game['players']) == 1:
        role = 'O'  # Second player to join gets 'O'
        game['players']['O'] = {'sid': request.sid, 'username': username}
    else:
        role = None  # If the game is full, no role is assigned

    # Notify the client about their role
    emit('player_role', {'role': role, 'username': username}, room=request.sid)

    # Broadcast the updated player list to all participants in the room
    emit('update_players', {
        'playerX': game['players'].get('X', {}).get('username', 'Waiting...'),
        'playerO': game['players'].get('O', {}).get('username', 'Waiting...')
    },
         room=game_id)

    # Broadcast the current game state
    emit('update_board', game, room=game_id)

    # Only emit new_question if the game is a quiz multiplayer game
    if 'question' in game:
        emit('new_question', {'question': game['question']}, room=game_id)


@socketio.on('disconnect')
def on_disconnect():
    username = session.get('user', 'Player')
    # Find the game this player was in
    for game_id, game in games.items():
        if 'question' in game:  # This is a quiz game
            for role, player_data in game['players'].items():
                if isinstance(player_data,
                              dict) and player_data.get('sid') == request.sid:
                    # Remove the player
                    game['players'].pop(role, None)
                    # Notify remaining players with better information
                    emit('player_disconnected', {
                        'username': username,
                        'playerName': username,
                        'role': role
                    },
                         room=game_id)
                    # Update player list
                    emit('update_players', {
                        'playerX':
                        game['players'].get('X', {}).get(
                            'username', 'Waiting...'),
                        'playerO':
                        game['players'].get('O', {}).get(
                            'username', 'Waiting...')
                    },
                         room=game_id)
                    break


def check_winner(board, player):
    # Possible winning combinations
    win_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],  # Rows
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],  # Columns
        [0, 4, 8],
        [2, 4, 6]  # Diagonals
    ]
    for combination in win_combinations:
        if all(board[i] == player for i in combination):
            return True
    return False


def check_draw(board):
    return all(cell != '' for cell in board)  # Check if the board is full


def get_new_question(category=None):
    if category:
        # Filter questions by the selected category
        filtered_questions = [
            q for q in quiz_questions if q['category'] == category
        ]
        if filtered_questions:
            return random.choice(filtered_questions)
        else:
            # If no questions are found for the category, return a default question
            return {
                "question": "No questions available for this category.",
                "answer": "N/A",
                "category": "default"
            }
    # If no category is specified, return a random question from all categories
    return random.choice(quiz_questions) if quiz_questions else None


@socketio.on('answer_question')
def on_answer_question(data):
    game_id = data['game_id']
    player = data['player']
    answer = data['answer']

    if game_id in games:
        game = games[game_id]

        if game['attempts'][player]:
            emit('attempted_already', {'player': player}, room=request.sid)
            return

        correct_answer = game['question']['answer']

        if answer.lower() == correct_answer.lower():
            game['eligible_player'] = player
            emit('answer_correct', {'player': player}, room=game_id)

            # Broadcast the next question after a correct answer
            game['question'] = get_new_question(
                game['category'])  # Use the stored category
            game['attempts'] = {'X': False, 'O': False}
            emit('new_question', {'question': game['question']}, room=game_id)
        else:
            game['attempts'][player] = True
            emit('answer_wrong', {'player': player}, room=game_id)


@socketio.on('make_move')
def on_make_move(data):
    game_id = data['game_id']
    index = data['index']
    player = data['player']

    if game_id in games:
        game = games[game_id]

        if game['board'][index] == '' and game['eligible_player'] == player:
            game['board'][index] = player
            game['eligible_player'] = None

            if check_winner(game['board'], player):
                emit('game_over', {'winner': player}, room=game_id)
                update_leaderboard(player, game['players'])
                return

            if check_draw(game['board']):
                emit('game_over', {'draw': True}, room=game_id)
                return

            emit('update_board', game, room=game_id)
        else:
            emit('invalid_move', {'message': 'Invalid move!'},
                 room=request.sid)


def update_leaderboard(winner, players):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        for role, player_data in players.items():
            username = player_data['username']
            if role == winner:
                cursor.execute(
                    "UPDATE users SET wins = wins + 1 WHERE username = ?",
                    (username, ))
            else:
                cursor.execute(
                    "UPDATE users SET losses = losses + 1 WHERE username = ?",
                    (username, ))
        conn.commit()


@app.route('/leaderboard')
def leaderboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, wins, losses FROM users ORDER BY wins DESC")
        leaderboard_data = cursor.fetchall()

    return render_template('leaderboard.html', leaderboard=leaderboard_data)


@socketio.on('move')
def on_move(data):
    game_id = data['game_id']
    index = data['index']
    player = data['player']

    if game_id in games:
        game = games[game_id]

        if game['board'][index] == '' and game['current_turn'] == player:
            game['board'][index] = player
            game['current_turn'] = 'O' if player == 'X' else 'X'

            if check_winner(game['board'], player):
                emit('game_over', {'winner': player}, room=game_id)
                return

            if check_draw(game['board']):
                emit('game_over', {'draw': True}, room=game_id)
                return

            emit('update_board', game, room=game_id)
        else:
            emit('invalid_move', {'message': 'Invalid move!'},
                 room=request.sid)


@socketio.on('reset_game')
def reset_game(data):
    game_id = data['game_id']
    if game_id in games:
        game = games[game_id]
        # Preserve existing players
        existing_players = game.get('players', {})
        games[game_id] = {
            'board': [''] * 9,
            'players': existing_players,  # Keep the existing players
            'question':
            get_new_question(game['category']),  # Use the stored category
            'streaks': {
                'X': 0,
                'O': 0
            },
            'eligible_player': None,
            'attempts': {
                'X': False,
                'O': False
            },
            'category': game['category']  # Preserve the category
        }

        emit('game_over', {'reset': True}, room=game_id)
        emit('update_board', games[game_id], room=game_id)
        # Send new question immediately after reset
        emit('new_question', {'question': games[game_id]['question']}, room=game_id)


@socketio.on('reset_question')
def reset_question(data):
    game_id = data['game_id']
    if game_id in games:
        game = games[game_id]
        game['question'] = get_new_question(
            game['category'])  # Use the stored category
        game['attempts'] = {'X': False, 'O': False}
        emit('new_question', {'question': game['question']}, room=game_id)


@socketio.on('reset_classic_game')
def reset_classic_game(data):
    game_id = data['game_id']
    if game_id in games:
        games[game_id] = {
            'board': [''] * 9,
            'current_turn': 'X',
            'players': {}
        }
        emit('game_over', {'reset': True}, room=game_id)  # Reset overlay
        emit('update_board', games[game_id], room=game_id)  # Reset board


@app.route('/quiz_multiplayer')
def quiz_multiplayer():
    return render_template('quiz_multiplayer.html')


@app.route('/classic_multiplayer')
def classic_multiplayer():
    return render_template('classic_multiplayer.html')


@app.route('/singleplayer')
def singleplayer():
    return render_template('singleplayer.html')


if __name__ == '__main__':
    try:
        logger.info("Starting Flask-SocketIO server...")
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
