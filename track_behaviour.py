import numpy as np
import csv
import sys
import os
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import pandas as pd
from datetime import date, timedelta
import pickle

#CONSTANTS
DATE_ID = 10

questions = [
    "Did you sleep in today?", # 1
    "Did you get more than 8 hours of sleep?", #2
    "Did you drink a cup of coffee?", #3
    "Did you go to bed on time?", #4
    "Have you smoked weed today?", #5
    "Have you worked out today?", #6
    "How many jobs have you applied to today?", #7
    "How many meals were/will be homemade today?", #8
    "How are you feeling out of 10?", #9
    "What day is it today? (Automatically generated, press enter)"] #10

def query():

    answers = []
    for q in questions:
        ans = raw_input(q + " ")
        if 'y' in ans: ans = 1
        elif 'n' in ans: ans = 0
        elif ans.isdigit(): ans = int(ans)
        if len(answers) == len(questions) - 1:
            current_date = date.today()
            answers.append(current_date.strftime('%d/%m/%Y'))
        else:
            answers.append(ans)

    if not os.path.exists('data.csv'):
        with open('data.csv', 'w') as f:
            data = csv.writer(f)
            data.writerow(questions)
            data.writerow(answers)
    else:
        with open('data.csv', 'ab') as f:
            data = csv.writer(f)
            data.writerow(answers)

def get_data():
    if os.path.exists('data.csv'):
        with open('data.csv', 'r') as f:
            data = csv.reader(f)
            df = list(data)
            headers = df.pop(0)
            return pd.DataFrame(df, columns = range(1,len(headers)+1))

def plot(question_num):

    df = get_data()
    num_points = 10

    ax = plt.subplot(111)
    ax.spines["top"].set_visible(True)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(True)
    ax.spines["left"].set_visible(True)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    x = df[DATE_ID].tolist()
    y = df[question_num].tolist()

    plt.plot(x, y, label = questions[question_num - 1])
    plt.legend(loc='best')

    plt.show()
    plt.close()

def run():
    while(1):
        print("enter \"q\" to query, or \"p QUESTION_NUM\" to plot, or quit to finish: "),
        ans = raw_input()
        if ans is 'q': query()
        elif 'p' in ans:
            response = ans.split()
            plot(int(response[1]))
        elif ans == 'quit':
            break

run()
