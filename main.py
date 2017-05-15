import os.path
import csv
from operator import itemgetter

import numpy as np
import matplotlib.pyplot as plt
import requests


def download_files_if_not_exists(url_list=[], file_list=[]):
    for url, file in zip(url_list, file_list):
        if not os.path.isfile(file):
            html = requests.get(url).content.decode()
            with open(file, 'w') as csvfile:
                csvfile.writelines(html)


def fetch_from_file(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # ignore first row which is heading
        if filename=='gender.csv':
            for row in reader:
                row[1] = int(row[1])
                row[2] = int(row[2])
                row[3] = int(row[3])
                row[4] = int(row[4])
                data.append(row)
        if filename=='political_parties.csv':
            for row in reader:
                row[1] = int(row[1])
                data.append(row)

    return data[:-1]

def plot_local_bodies():
    """Plot a pie chart showing the distribution of local bodies"""
    # Categories of local bodies
    labels = ['Gaupalika', 'Nagarpalika', 'Upa-Mahanagarpalika', 'Mahanagarpalika']

    # Respective number of each category
    values =[463,240,12,4]

    # Percentage of each local body
    percent = [v/sum(values)*100 for v in values]

    # Adds the percentage to respective label
    # For e.g. Gaupalika turns to Gaupalika (64.39%)
    for i in range(4):
        labels[i] += ' (' + str(round(percent[i],2)) + '%)'

    # Plotting pie chart
    plt.figure(figsize=(10,5))
    patches,_ = plt.pie(x=values,
            shadow=True,
            colors=['r','g','b','black'],
            counterclock=False,
            )

    plt.legend(patches, labels, loc='lower left')
    plt.axis('equal')
    plt.title("Distribution of Local Bodies")
    plt.show()


def plot_female_percent():
    """Plots a bar graph showing highest percentage of female voters from each district"""
    filename = 'gender.csv'
    data = fetch_from_file(filename)

    # Adds a new column for percentage of female voters
    [x.append(x[2] / x[4]) for x in data]

    # Sorts the nested list based on percentage of female voters
    new_data = sorted(data, reverse=True,
                      key=itemgetter(5))

    # Selecting first 5
    district = [x[0] for x in new_data[:5]]
    percent = [x[5] * 100 for x in new_data[:5]]

    y_pos = np.arange(len(district))
    color = ['black', 'blue', 'green', '#2F4F4F', 'red']
    plt.figure(figsize=(9, 5))
    plt.barh(y_pos, percent[::-1], align='center', alpha=1, color=color)
    for i, v in enumerate(percent[::-1]):
        plt.text(v + 0.6, i - 0.1, str(round(v,2)) + '%')

    plt.yticks(y_pos, district[::-1])
    plt.xticks(range(0, 80, 10))
    plt.xlabel('Percentage of Female Voters')
    plt.title('Districts with Highest Percentage of Female Voters')
    plt.show()


def plot_female_number():
    """Plots a bar graph showing highest number of female voters from each district"""
    filename = 'gender.csv'
    data = fetch_from_file(filename)


    # Sorts the nested list based on number of female voters
    data = sorted(fetch_from_file(filename), reverse=True,
                      key=itemgetter(2))

    # Selecting first 5
    district = [x[0] for x in data[:5]]
    female = [x[2] for x in data[:5]]

    y_pos = np.arange(len(district))
    color = ['black', 'blue', 'green', '#2F4F4F', 'red']
    plt.figure(figsize=(9, 5))
    plt.barh(y_pos, female[::-1], align='center', alpha=1, color=color)
    for i, v in enumerate(female[::-1]):
        plt.text(v + 0.6, i - 0.1, str(v))

    plt.yticks(y_pos, district[::-1])
    plt.xticks(range(0, 400000, 50000))
    plt.xlabel('Number of Female Voters')
    plt.title('Districts with Highest Number of Female Voters')
    plt.show()


if __name__=='__main__':

    # list of urls to get the data from
    url_list = [
        'https://raw.githubusercontent.com/okfnepal/election-nepal-data/master/Demographics/Total%20Male%20and%20female%20voters%20per%20districts.csv',
        'https://raw.githubusercontent.com/okfnepal/election-nepal-data/master/Demographics/Total%20number%20of%20Local%20Bodies%20per%20districts.csv',
        'https://raw.githubusercontent.com/okfnepal/election-nepal-data/master/Demographics/Total%20number%20of%20registered%20political%20parties%20per%20districts.csv',
        ]

    # list of file names to store data
    file_list = ['gender.csv', 'local_bodies.csv', 'political_parties.csv']

    download_files_if_not_exists(url_list, file_list)


    # Call the function as you need to see the graphs

    plot_local_bodies()
    # plot_female_percent()
    # plot_female_number()