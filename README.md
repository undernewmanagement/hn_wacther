## What is this?

This script is used to "measure the weather" on HAcker news.

Just like in real life we don't simply look at the last temperature at 11:59 and say, "This is 
how the day was." That would be wrong and inaccurate. We take multiple readings on multiple variables
per day to get a more complete story.

That is the idea with this little project. Here, we will mesaure the weather on Hacker News across
a number of variables. My hope is that over time the collection and publication os this data would
prove valuable, or at least interesting to some folds.

This is a python script and docker image which will collect bookmark rankings from Hacker News 
(http://news.ycombinator.com).

It measues the top 150 links for ranking, number of comments, and "karma score."

## Requirements
  1. Python 3+
  2. Docker / DOcker compose (optional)

**NOTE**: you do not have to have docker to get this thing going. I'm just lazy and

**NOTE**: I do not believe that postges is required -- it is just what I chose.

## Getting started
  1. Setup your database
  2. Build your database url string and put that into you `.env` file
     eg - postgres://user:pass@host/dbname
  3. source .env file and run python db.py to setup the tables in your DB
  4. run docker-compose up -d to run in backgroundo

## Todo:
  1. postgresql or other db (mysql, mysq lite) as configure in docker-compose.yml

