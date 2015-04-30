#!/usr/bin/env python
#
# Calvin Miller
# 4/30/15
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    try:
        con = connect()
        cur = con.cursor()
        cur.execute('DELETE FROM MATCHES')
        con.commit()
        
    except psycopg2.DatabaseError, e:
        print 'Error %s' %e
        sys.exit(1)

    finally:
        if con:
            con.close()


def deletePlayers():
    """Remove all the player records from the database."""

    try:
        con = connect()
        cur = con.cursor()
        cur.execute('DELETE FROM PLAYERS')
        con.commit()
        
    except psycopg2.DatabaseError, e:
        print 'Error %s' %e
        sys.exit(1)

    finally:
        if con:
            con.close()


def countPlayers():
    """Returns the number of players currently registered."""

    try:
        con = connect()
        cur = con.cursor()
        cur.execute('SELECT COUNT(*) FROM PLAYERS')
        return cur.fetchone()[0]

    except psycopg2.DatabaseError, e:
        print 'Error %s' %e
        sys.exit(1)

    finally:
        if con:
            con.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    try:
        con = connect()
        cur = con.cursor()
        cur.execute("INSERT INTO PLAYERS(NAME) VALUES (%s)" , (name,))
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' %e
        sys.exit(1)

    finally:
        if con:
            con.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    try:
        con = connect()
        cur = con.cursor()
        cur.execute('''SELECT P.PLAYER_ID, P.NAME, COALESCE(W.WINS,0) as Wins, COALESCE(W.WINS, 0) + COALESCE(L.LOSSES,0) AS MATCHES
                        FROM PLAYERS P
                        FULL OUTER JOIN WINS_V W
                        ON WINNER = P.PLAYER_ID
                        FULL OUTER JOIN LOSSES_V L
                        ON LOSER = P.PLAYER_ID
                        ORDER BY W.WINS;''')
        standings = cur.fetchall()
        return standings

    except psycopg2.DatabaseError, e:
        print 'Error %s' %e
        sys.exit(1)

    finally:
        if con:
            con.close()
    


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("INSERT INTO MATCHES(WINNER, LOSER) VALUES (%s,%s)", (winner, loser))
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' %e
        sys.exit(1)
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    try:
        con = connect()
        cur = con.cursor()
        cur.execute('''SELECT P.PLAYER_ID, P.NAME
                        FROM PLAYERS P
                        FULL OUTER JOIN WINS_V W
                        ON WINNER = P.PLAYER_ID
                        FULL OUTER JOIN LOSSES_V L
                        ON LOSER = P.PLAYER_ID
                        ORDER BY W.WINS''')
        
        #Change the format of the data
        while True:

            rowEven = cur.fetchone()
            rowOdd = cur.fetchone()

            try:
                pairings.append((rowEven[0],rowEven[1],rowOdd[0],rowOdd[1]))
            except NameError:
                pairings = [(rowEven[0],rowEven[1],rowOdd[0],rowOdd[1])]

            if cur.rownumber == cur.rowcount:
                break
        
        
        return pairings

    except psycopg2.DatabaseError, e:
        print 'Error %s' %e
        sys.exit(1)


