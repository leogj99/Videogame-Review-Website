from flask_mysqldb import MySQL
import random

class DB:
    def __init__(self, mysql):
        self.mysql = mysql
        

    def gameByGenre(self, genre):
        self.cur = self.mysql.connection.cursor()
        self.cur.execute(f"SELECT GAME_NAME FROM GAMES WHERE GENRE = '{genre}'")
        result = self.cur.fetchall()
        if not result:  
            return None
        else:
            return result
        
    
    def playerByGenre(self, genre):
        self.cur = self.mysql.connection.cursor()
        self.cur.execute(f"SELECT DISTINCT p.PLAYER_ID, p.PLAYER_FULLNAME, p.EMAIL, p.GAMERTAG, g.GAME_NAME "
                 f"FROM PLAYERS p "
                 f"JOIN REVIEWS r ON p.PLAYER_ID = r.PLAYER_ID "
                 f"JOIN GAMES g ON r.GAME_ID = g.GAME_ID "
                 f"WHERE g.GENRE = '{genre}'")
        result = self.cur.fetchall()
        if not result:  
            return None
        else:
            return result
        
        
    def addPlayer(self, fullname, email, gamertag):
        found = False
        # Generates random id for the new player
        while not found: 
            id = random.randint(0,999)
            result = self.findMatch("PLAYER_ID", "PLAYERS", id)
            if not result:
                found = True
        try:
            self.cur = self.mysql.connection.cursor()
            self.cur.execute(f"INSERT INTO PLAYERS VALUES ({id}, '{fullname}', '{email}', '{gamertag}')")
            self.mysql.connection.commit()
            return True
        except Exception:
            print("Error adding player to database")
            return False
        
        
    def addGame(self, name, genre):
        found = False
        # Generates random id for the new game
        while not found: 
            id = random.randint(0,999)
            result = self.findMatch("GAME_ID", "GAMES", id)
            if not result:
                found = True
        try:
            self.cur = self.mysql.connection.cursor()
            self.cur.execute(f"INSERT INTO GAMES VALUES ({id}, '{name}', '{genre}')")
            self.mysql.connection.commit()
            return True
        except Exception:
            print("Error adding game to database")
            return False
    
    
    def addReview(self, player_name, game_name, review_comment, rating):
        found = False
        # Generates random id for the review
        while not found:
            id = random.randint(0,999)
            result = self.findMatch("GAME_ID", "GAMES", id)
            if not result:
                found = True
                
        self.cur = self.mysql.connection.cursor()
        
        # Find the id of the player based on the name 
        self.cur.execute(f"SELECT PLAYER_ID FROM PLAYERS WHERE PLAYER_FULLNAME = '{player_name}'")
        player_id = self.cur.fetchone()[0]
        
        # Find the id of the game based on the name 
        self.cur.execute(f"SELECT GAME_ID FROM GAMES WHERE GAME_NAME = '{game_name}'")
        game_id = self.cur.fetchone()[0]
        
        # Try to add the new review with the inputs
        try:
            self.cur.execute(f"INSERT INTO REVIEWS VALUES ({id}, {player_id}, {game_id}, '{review_comment}', '{rating}')")
            self.mysql.connection.commit()
            return True
        except Exception:
            print("Error adding review to database")
            return False
        
    def findMatch(self, attribute, table, input):
        if input is not None:
            self.cur = self.mysql.connection.cursor()
            self.cur.execute(f"SELECT {attribute} FROM {table} WHERE {attribute} = '{input}'")
            result = self.cur.fetchone()
            if not result:
                return None
            else:
                return result
        else:
            return None
        
    
    def displayPlayers(self):
        self.cur = self.mysql.connection.cursor()
        self.cur.execute("SELECT PLAYER_FULLNAME, EMAIL, GAMERTAG FROM PLAYERS")
        result = self.cur.fetchall()
        if not result:
            return None
        else:
            return result
        
        
    def displayGames(self):
        self.cur = self.mysql.connection.cursor()
        self.cur.execute("SELECT GAME_NAME, GENRE FROM GAMES")
        result = self.cur.fetchall()
        if not result:
            return None
        else:
            return result
        
    
    def displayReviews(self):
        self.cur = self.mysql.connection.cursor()
        self.cur.execute(f"SELECT p.PLAYER_FULLNAME, g.GAME_NAME, p.GAMERTAG, r.REVIEW_COMMENT , r.RATING "
                         f"FROM REVIEWS r "
                         f"JOIN PLAYERS p "
                         f"ON p.PLAYER_ID = r.PLAYER_ID "
                         f"JOIN GAMES g "
                         f"ON g.GAME_ID = r.GAME_ID")
        result = self.cur.fetchall()
        if not result:
            return None
        else:
            return result


    def getNames(self):
        self.cur = self.mysql.connection.cursor()
        self.cur.execute("SELECT PLAYER_FULLNAME FROM PLAYERS")
        result = self.cur.fetchall()
        if not result:
            return None
        else:
            return result
    
    def getGames(self):
        self.cur = self.mysql.connection.cursor()
        self.cur.execute("SELECT GAME_NAME FROM GAMES")
        result = self.cur.fetchall()
        if not result:
            return None
        else:
            return result

    

