from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL
from DB import DB

#------Connection of database to flask website------
app = Flask(__name__)        
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Calzones12!'
app.config['MYSQL_DB'] = 'website'
#---------------------------------------------------
mysql = MySQL(app)
database = DB(mysql)
#---------------------------------------------------
@app.route("/search_game", methods= ['post', 'get'])
def searchGame():
    if request.method == 'POST':
        game_genre = request.form.get("game_genre")
        result = database.gameByGenre(game_genre)
        if result is not None:
            return render_template('search_game.html', games=result)
        else:
            error_message = f"No games found"        # Player does not exist, display an error message
            return render_template('search_game.html', error_message=error_message)

    return render_template('search_game.html')

@app.route("/search_player", methods= ['post', 'get'])
def searchPlayer():
    if request.method == 'POST':
        game_genre = request.form.get("game_genre")
        result = database.playerByGenre(game_genre)
        if result is not None:
            return render_template('search_player.html', players=result)
        else:
            error_message = f"No players found"
            return render_template('search_player.html', error_message=error_message)

    return render_template('search_player.html')

@app.route("/add_player", methods=['get', 'post'])
def newPlayer():
    error_message = None
    
    if request.method == 'POST':
        fullname = request.form.get('player_fullname')
        email = request.form.get('email')
        gamertag = request.form.get('gamertag')

        # Check if the player name exists in the database
        existing_player = database.findMatch("PLAYER_FULLNAME", "PLAYERS", fullname)
        if existing_player:
            error_message = f"Player '{fullname}' already exists in the database."
            return render_template('add_player.html', error_message=error_message)

        # Checks if the player email exists in the database
        existing_email = database.findMatch("EMAIL", "PLAYERS", email)
        if existing_email:
            error_message = f"Email '{email}' already exists in the database."
            return render_template('add_player.html', error_message=error_message)

        # Checks if the player gamertag exists in the database
        existing_gamertag = database.findMatch("GAMERTAG", "PLAYERS", gamertag)
        if existing_gamertag:
            error_message = f"Gamertag '{gamertag}' already exists in the database."
            return render_template('add_player.html', error_message=error_message)

        # Check if any of the fields are missing
        if not fullname or not email or not gamertag:
            error_message = "Please enter all fields to add a player."

        # If all fields are entered, add the new player to the database
        else:
            database.addPlayer(fullname, email, gamertag)
            success_message = "Player added successfully!"
            return render_template('add_player.html', success_message=success_message)

    return render_template('add_player.html', error_message=error_message)

@app.route("/view_all_players", methods=['get', 'post'])
def listPlayers():
    result = database.displayPlayers()
    if result:
        return render_template("view_all_players.html", players=result)
    else:
        error_message = f"No players found in database."
        return render_template('view_all_players.html', error_message=error_message)

@app.route("/view_all_games", methods=['get', 'post'])  
def listGames():
    result = database.displayGames()
    if result:
        return render_template("view_all_games.html", games=result)
    else:
        error_message = f"No games found in database."
        return render_template('view_all_games.html', error_message=error_message)
       
#----Handles all redirects to the other pages----
@app.route("/redirect/<redirect_type>")
def allRedirects(redirect_type):
    if redirect_type == "search_game":
        return redirect("/search_game")
    elif redirect_type == "search_player":
        return redirect("/search_player")
    elif redirect_type == "menu":
        return redirect("/")
    elif redirect_type == "add_player":
        return redirect("/add_player")
    elif redirect_type == "view_all_players":
        return redirect("/view_all_players")
    elif redirect_type == "view_all_games":
        return redirect("/view_all_games")
    else:
        return "Invalid redirect type"
#------------------------------------------------
    
@app.route("/")               # Basic route
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
