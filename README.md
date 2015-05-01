#Tournament Results

What is it?
--------

This project contains the database schema to store a swiss tournament game match. It is also the code to query this data and determine the winners of various games. Currently it supports a single swiss tournament with an even number of players.


How to Run it?
--------
1.) This project uses the Postgres RDBMS. You will need to create a database named 'Tournament'.<br>
2.) You will need to connect to the database created above.<br>
3.) Import the tournament.sql file into the database(Tournament). Using the command '\i tournament.sql'.<br>
4.) Then run the tournament_test.py file.


tournament.py
---------

This file contains all of the back-end functions necessary to run the test cases in tournament_test.py.

tournament_test.py
----------

This file contains the use test cases for a single Swiss Tournament.

tournament.sql
---------

This file contains the Database Schema.

