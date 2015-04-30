-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.

create table Players (PLAYER_ID SERIAL PRIMARY KEY, NAME TEXT);

create table Matches (MATCH_ID SERIAL PRIMARY KEY, WINNER INTEGER REFERENCES PLAYERS(PLAYER_ID), LOSER INTEGER REFERENCES PLAYERS(PLAYER_ID));

create or replace view wins_v as SELECT DISTINCT WINNER, COUNT(WINNER) AS WINS FROM MATCHES GROUP BY WINNER;

create or replace view losses_v as SELECT DISTINCT LOSER, COUNT(LOSER) AS LOSSES FROM MATCHES GROUP BY LOSER;


