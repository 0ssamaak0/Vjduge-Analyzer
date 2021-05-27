import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta





def get_contest(contest):
    """ get the contest as a parameter, returns a list of two pandas dataframes, the first contains the problems data, the second contains the submissions data. """
    # Opening the file

    with open (contest, "r", encoding='iso-8859-1') as file:

        page = file.read()
        soup = BeautifulSoup(page, features= "lxml")

        # Getting the table head data

        thead = soup.find(id = "contest-rank-table").find("thead")
        problem_letters = thead.find_all("tr")[0]
        problem_letters.find_all("th")
        problem_letters_list = []

        for problem_letter in list(problem_letters)[8:]:
            problem_letters_list.append(problem_letter.text)
        problem_scores = thead.find_all("tr")[1]
        problem_scores_list = []
        for problem_score in problem_scores:
            problem_scores_list.append((int(problem_score.text.split("/")[0]), int(problem_score.text.split("/")[1])))

        # Getting the table body data

        tbody = soup.find(id = "contest-rank-table").find("tbody").find_all("tr")
        indices = problem_letters_list.copy()
        indices.insert(0, "real_score")
        indices.insert(0, "score")

        # Creating the head dataframe
        df_problems = pd.DataFrame(data = problem_scores_list, index = problem_letters_list, columns= ["accepted", "total"])
        df_problems["percentage"] = df_problems["accepted"] / df_problems["total"]

        # Creating the body dataframe

        df_team = pd.DataFrame(columns = indices)
        for num, person in enumerate(tbody):
            score = int(person.find(class_ = "solved").text)
            lis = []
            all_times = person.find_all(class_ = "prob")
            for time in all_times:
                time = time.text.split(" ")[0].split(":")
                try:
                    times = [int(t) for t in time]
                    delta = timedelta(
                    hours = times[0],
                    minutes = times[1],
                    seconds = times[2],
                    )
                except:
                    delta = ""
                lis.append(delta)
            df_team.loc[num] = [score] + [score] + lis
        df_team.replace("", pd.Timedelta("nat"), inplace = True)

        # Checks if all problems has the same dtype
        for col in df_team.columns[2:]:
            if df_team[col].dtype != "timedelta64[ns]":
                df_team[col] = pd.Timedelta(0)

        # Returning the dataframes in a list
        return [df_problems, df_team]





def verbal_stats(dfs, save = False, filename = "verbalStats"):
    """ Gets the an iterable contains the Dataframes lists as a parameter - which is returned from the get_contest function- and prints some verbal stats.
    the stats can be saved if save is set as True. filename can be also specified.
    """
    if os.path.exists(filename + ".txt"):
        os.remove(filename + ".txt")

    for i in range(len(dfs)):
        verbal_stats = []
        verbal_stats.append(f"Verbal Stats {i + 1}\n")
        
        # Appending verbal stats to the list
        verbal_stats.append(f"Accpeted submissions: {int(dfs[i][0].sum()[0])}")
        verbal_stats.append(f"Total submissions: {int(dfs[i][0].sum()[1])}")
        verbal_stats.append(f"Percentage of accpeted submissions: {round(dfs[i][0].sum()[0] / dfs[i][0].sum()[1] * 100, 1)}%")
        verbal_stats.append(f"Height percentage of accpeted submissions: Problem {dfs[i][0].query('percentage == percentage.max()').index[0]} with {round(dfs[i][0].query('percentage == percentage.max()').percentage[0] * 100, 1)}%")
        verbal_stats.append(f"Lowest percentage of accpeted submissions: Problem {dfs[i][0].query('percentage == percentage.min()').index[0]} with {round(dfs[i][0].query('percentage == percentage.min()').percentage[0] * 100, 1)}%")

        for verbal_stat in verbal_stats:
            print(verbal_stat)

        if save == True:
            with open(filename + ".txt", "a") as file:
                file.writelines("\n".join(verbal_stats))
                file.writelines("\n\n")





def graph_submissions_per_problem(dfs, save = False, filename = "Submissions per problem"):
    """ This is a graphing funcion, it gets the an iterable contains the Dataframes lists as a parameter - which is returned from the get_contest function- and returns the graph
    The graph can be saved, and the name can be specified.
    """


    plt.figure(figsize = (15, 7));
    for i in range(len(dfs)):
        plt.bar(x = dfs[i][0].index, bottom = dfs[i][0]["accepted"], height = dfs[i][0]["total"] - dfs[i][0]["accepted"], width = 0.5, alpha = 0.5, label = f"failed {i + 1}");
        plt.bar(x = dfs[i][0].index, height = dfs[i][0]["accepted"], width = 0.5, alpha = 0.5, label = f"accepted {i + 1}")
        # plt.yticks(np.arange(0,dfs[i][0]["total"].max(), 25));
        plt.title("Sbmissions for each problem", fontsize = 35);
        plt.xlabel("Problems", fontsize = 20);
        plt.ylabel("Submissions", fontsize = 20);
        plt.legend(fontsize = 15);
        if len(dfs) == 1:
            for n, problem in enumerate(dfs[i][0].values):
                if problem[1] == 0:
                    text = "0"
                else:
                    text = str(round(problem[0] / problem[1] * 100, 1))
                plt.text(y = problem[1] + 4, x = n - 0.4, s =  text + "%", fontsize = 9);

    if save == True:
        plt.savefig(filename +".jpg")
    else:
        plt.show()





def graph_scores_histogram(dfs, save = False, filename = "Scores Histogram"):
    """ This is a graphing funcion, it gets the an iterable contains the Dataframes lists as a parameter - which is returned from the get_contest function- and returns the graph
    The graph can be saved, and the name can be specified.
    """

    plt.figure(figsize=(15,7));
    for i in range(len(dfs)):
        plt.hist(x = dfs[i][1]["score"], bins = np.arange(28) - 0.35, width = 0.7, align = "mid", alpha = 0.5, label = f"Scores {i + 1}");
        plt.title("Students Scores Histogram", fontsize = 35);
        plt.xlabel("Scores", fontsize = 20);
        plt.ylabel("Students", fontsize = 20);
        plt.xticks(np.arange(len(dfs[i][0]) + 1));
        plt.legend();
        # plt.yticks(np.arange(dfs[i][1]["score"].value_counts().max() + 1));

    if save == True:
        plt.savefig(filename +".jpg")
    else:
        plt.show()





def graph_submissions_per_hour(dfs, save = False, filename = "Submissions per hour"):
    """ This is a graphing funcion, it gets the an iterable contains the Dataframes lists as a parameter - which is returned from the get_contest function- and returns the graph
    The graph can be saved, and the name can be specified.
    """

    total_time = 0
    for df in dfs:
        temp_time = df[1][df[1].columns[2:]].max().dropna().max()
        temp_time = temp_time.days * 24 + temp_time.seconds / 3600
        temp_time = round(temp_time + 0.5)
        if(temp_time > total_time):
            total_time = temp_time

    plt.figure(figsize = (15,7));
    for i in range(len(dfs)):

        submission_before = []
        to_be_deleted = dfs[i][1][dfs[i][1][dfs[i][1].columns[2:]] == timedelta(0)].notna().sum().sum()

        for j in range(1, total_time + 1):
            submission_before.append(dfs[i][1][dfs[i][1][dfs[i][1].columns[2:]] < timedelta(hours = j)].notna().sum().sum() - to_be_deleted)

        plt.plot(np.arange(1, total_time + 1), submission_before, lw = 3, label = f"Submissions {i + 1}");
        plt.xticks(np.arange(0, total_time + 1, 10));
        plt.title("Accepted submissions per hour (cumulative)", fontsize = 35);
        plt.xlabel("Total hours", fontsize = 20, y = -100);
        plt.ylabel("Total accepted submissions", fontsize = 20);
        plt.legend();

    if save == True:
        plt.savefig(filename +".jpg")
    else:
        plt.show()

        