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
        while not found: # generates random number between 0 and 999 until it generates one that is not in the database already
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


    

