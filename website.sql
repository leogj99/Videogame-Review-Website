DROP DATABASE IF EXISTS `website`;
CREATE DATABASE `website`; 
USE `website`;

CREATE TABLE PLAYERS(
	PLAYER_ID INT PRIMARY KEY NOT NULL,
    PLAYER_FULLNAME VARCHAR(50) NOT NULL,
    EMAIL VARCHAR(50) NOT NULL,
    GAMERTAG VARCHAR(50) NOT NULL
);

CREATE TABLE GAMES(
	GAME_ID INT PRIMARY KEY NOT NULL,
    GAME_NAME VARCHAR(50) NOT NULL,
    GENRE VARCHAR(50) NOT NULL
);

CREATE TABLE REVIEWS(
	REVIEW_ID INT PRIMARY KEY NOT NULL,
    PLAYER_ID INT NOT NULL,
    GAME_ID INT NOT NULL,
    REVIEW_COMMENT VARCHAR(100) NOT NULL,
    RATING INT NOT NULL CHECK (RATING <= 10),
    FOREIGN KEY (PLAYER_ID) REFERENCES PLAYERS(PLAYER_ID) ON DELETE CASCADE,
    FOREIGN KEY (GAME_ID) REFERENCES GAMES(GAME_ID) ON DELETE CASCADE
);

INSERT INTO PLAYERS VALUES (35, 'Michaela Hayes', 'mickyhayes@gmail.com', 'mickythamouse');
INSERT INTO PLAYERS VALUES (66, 'Leonardo Guzman', 'leoguzman123@gmail.com', 'leothalion');
INSERT INTO PLAYERS VALUES (03, 'Nicolas Hidalgo', 'nicolash97@yahoo.com', 'ardillaUchiha');
INSERT INTO PLAYERS VALUES (04, 'Andy Lorente', 'pandyandy@gmail.com', 'panda123');
INSERT INTO PLAYERS VALUES (15, 'Avery Robinson', 'averyrobinson@hotmail.com', 'averyr');
INSERT INTO PLAYERS VALUES (29, 'Alex Garcia', 'alexgarcia@gmail.com', 'alexg');
INSERT INTO PLAYERS VALUES (33, 'David Kim', 'davidkim@yahoo.com', 'davek');
INSERT INTO PLAYERS VALUES (41, 'Sarah Patel', 'sarahpatel@gmail.com', 'sarahp');
INSERT INTO PLAYERS VALUES (52, 'Sophia Singh', 'sophiasingh@outlook.com', 'sophias');
INSERT INTO PLAYERS VALUES (63, 'Liam Davis', 'liamdavis@gmail.com', 'liamd');
INSERT INTO PLAYERS VALUES (71, 'Ethan Chen', 'ethanchen@gmail.com', 'ethanc');
INSERT INTO PLAYERS VALUES (84, 'Emma Wilson', 'emmawilson@yahoo.com', 'emmaw');
INSERT INTO PLAYERS VALUES (92, 'Noah Thompson', 'noahthompson@hotmail.com', 'noaht');
INSERT INTO PLAYERS VALUES (101, 'Ella Brown', 'ellabrown@yahoo.com', 'ellab');

INSERT INTO GAMES VALUES (31, 'World of Warcraft', 'MMORPG');
INSERT INTO GAMES VALUES (53, 'League of Legends', 'MOBA');
INSERT INTO GAMES VALUES (41, 'Counter Strike', 'Shooter');
INSERT INTO GAMES VALUES (66, 'Rust', 'Survival');
INSERT INTO GAMES VALUES (12, 'Minecraft', 'Sandbox');
INSERT INTO GAMES VALUES (22, 'Grand Theft Auto V', 'Action-Adventure');
INSERT INTO GAMES VALUES (87, 'Overwatch', 'Hero Shooter');
INSERT INTO GAMES VALUES (99, 'Fortnite', 'Battle Royale');
INSERT INTO GAMES VALUES (45, 'Hearthstone', 'Collectible Card Game');
INSERT INTO GAMES VALUES (71, 'Apex Legends', 'Battle Royale');
INSERT INTO GAMES VALUES (18, 'The Elder Scrolls V: Skyrim', 'Action RPG');
INSERT INTO GAMES VALUES (63, 'Terraria', 'Sandbox');
INSERT INTO GAMES VALUES (24, 'Rainbow Six Siege', 'Tactical Shooter');
INSERT INTO GAMES VALUES (38, 'Dark Souls', 'Action RPG');

INSERT INTO REVIEWS VALUES (12, 33, 31, "Great game! I love it.", 10);
INSERT INTO REVIEWS VALUES (82, 03, 41, "Not bad. However, I have played better games.", 7);
INSERT INTO REVIEWS VALUES (66, 35, 31, "It is very difficult!", 7);
INSERT INTO REVIEWS VALUES (27, 15, 22, "One of the best open-world games out there!", 9);
INSERT INTO REVIEWS VALUES (43, 29, 99, "Fun gameplay, but the building mechanics can be frustrating.", 4);
INSERT INTO REVIEWS VALUES (58, 33, 38, "Brutally difficult, but very rewarding.", 7);
INSERT INTO REVIEWS VALUES (75, 52, 45, "Addictive and challenging gameplay.", 8);
INSERT INTO REVIEWS VALUES (91, 63, 18, "Epic adventure with tons of content.", 10);
INSERT INTO REVIEWS VALUES (102, 71, 87, "Fast-paced and exciting. Would recommend.", 7);
INSERT INTO REVIEWS VALUES (116, 84, 24, "Intense tactical shooter that requires strategy and teamwork.", 10);
INSERT INTO REVIEWS VALUES (127, 03, 53, "Fun game to play with friends, but can be toxic at times.", 5);
INSERT INTO REVIEWS VALUES (132, 15, 12, "Classic game that never gets old.", 8);
INSERT INTO REVIEWS VALUES (149, 35, 66, "Harsh survival game with a steep learning curve.", 6);

    
    