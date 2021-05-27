# Vjudge-Contest_Analyzer

### Vjudge: an online tool that allows grab problems from other vritual judges like codeForces, HackerRank, etc. you can also make groups and you can make a contest between the students of this group.

This python library allows you to get useful insights from the contest while it's running or - preferably - after completion, you can also compare contests to see how the levels of the students have changed.

## Here's a small guide about how to use this library.

1- open the contests (rank) webpage in which you see the submissions of all students for each problem in a very huge table.

2- scroll down if you have big number of students, check that you don't see (show more) anymore. *The getter function will crash if you didn't*.

3- save the HTML code of the page.

now open a new jupyter notbook or a python file.
use `get_contest` function to save the contest into a variable. pass the HTML file to this function as a parameter.

congratulations! you can now analyze this contest using  4 functions:

1- `verbal_stats`

2- `graph_submissions_per_problem`

3- `graph_scores_histogram`

4- `graph_submissions_per_hour`


The usage of these functions are very similar, each one takes at least one parameter, that must be an iterable e.g., a list - you may need to compare many contests - and an optional boolean save parameter if you want to save the stats or the graph, and finally the name of this file, it will have a general name if no name is specified.

you can check `Test.ipynb` to see how to use this library.