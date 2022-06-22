Project: Investigate a Dataset - [TMDb movie data]
Table of Contents
Introduction
Data Wrangling
Exploratory Data Analysis
Conclusions

Introduction
Dataset Description
This data set contains information about more than 10,000 movies collected from The Movie Database (TMDb), it includes the following 21 columns (which all self explanatory):

['id', 'imdb_id', 'popularity', 'budget', 'revenue', 'original_title', 'cast', 'homepage', 'director', 'tagline', 'keywords', 'overview', 'runtime', 'genres', 'production_companies', 'release_date', 'vote_count', 'vote_average', 'release_year', 'budget_adj', 'revenue_adj']

Certain columns, like ‘cast’, ‘genres’, ‘director’ and ‘production_companies’, contain multiple values separated by pipe (|) characters.
The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.
Questions for Analysis
How Many Movies ...?

Q01.............. Produced Every Year?
Q02.............. For Each Genre?
Q03.............. For Each Runtime Bin?
Q04.............. For Each Budget Bin (Very-Low, Low, Average, High, Very-High)?
Q05.............. Considered as (Super-Flop, Flop, Hit, Super-Hit)?
The Profitable Movies (Hit & Super-Hit Movies):

Q06. How Has The Film Industry Evolved From Year To Year In Relation To Budget, Revenue And Gross Profit?
Q07. What Was The Most Successful Genres, Cast, director ....?
