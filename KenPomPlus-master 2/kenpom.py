# Created by Lee Robinson

from bs4 import BeautifulSoup
from flask import Flask, render_template
import requests
import csv

app = Flask(__name__)
TEAMS = []


class Team:
    def __init__(self, arr):
        self.rank = arr[0]
        self.name = arr[1]
        self.conference = arr[2]
        self.win_loss = arr[3]
        self.pyth = float(arr[4])
        self.adj_o = float(arr[5])
        self.adj_o_rank = arr[6]
        self.adj_d = float(arr[7])
        self.adj_d_rank = arr[8]
        self.adj_t = float(arr[9])
        self.adj_t_rank = arr[10]
        self.luck = arr[11]
        self.luck_rank = arr[12]
        self.sos_pyth = float(arr[13])
        self.sos_pyth_rank = arr[14]
        self.sos_opp_o = float(arr[15])
        self.sos_opp_o_rank = arr[16]
        self.sos_opp_d = float(arr[17])
        self.sos_opp_d_rank = arr[18]
        self.ncsos_pyth = float(arr[19])
        self.ncsos_pyth_rank = arr[20]


def read_teams():

    teams = list()
    with open('teams.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stats = []
            [stats.append(row[f]) for f in reader.fieldnames]
            teams.append(Team(stats)) 

    return teams


def write_teams(teams):

    with open('teams.csv', 'w') as csvfile:

        categories = ['Name', 'Rank', 'Conference', 'Win/Loss', 'Pyth', 'AdjO',
                      'AdjO Rank', 'AdjD', 'AdjD Rank', 'AdjT', 'AdjT Rank', 'Luck',
                      'Luck Rank', 'SoS Pyth', 'SoS Pyth Rank', 'SoS OppO', 'SoS OppO Rank', 
                      'SoS OppD', 'SoS OppD Rank', 'NCSoS Pyth', 'NCSoS Pyth Rank']
        writer = csv.DictWriter(csvfile, fieldnames=categories)

        writer.writeheader()
        for team in teams:
            writer.writerow({'Name': team.name,
                             'Rank': team.rank,
                             'Conference': team.conference,
                             'Win/Loss': team.win_loss,
                             'Pyth': team.pyth,
                             'AdjO': team.adj_o,
                             'AdjO Rank': team.adj_o_rank,
                             'AdjD': team.adj_d,
                             'AdjD Rank': team.adj_d_rank,
                             'AdjT': team.adj_t,
                             'AdjT Rank': team.adj_t_rank,
                             'Luck': team.luck,
                             'Luck Rank': team.luck_rank,
                             'SoS Pyth': team.sos_pyth,
                             'SoS Pyth Rank': team.sos_pyth_rank,
                             'SoS OppO': team.sos_opp_o,
                             'SoS OppO Rank': team.sos_opp_o_rank,
                             'SoS OppD': team.sos_opp_d,
                             'SoS OppD Rank': team.sos_opp_d_rank,
                             'NCSoS Pyth': team.ncsos_pyth,
                             'NCSoS Pyth Rank': team.ncsos_pyth_rank})


def retrieve_teams(soup):

    teams = list()
    table = soup.find(id="ratings-table")

    for team in table.findAll("tbody")[0].findAll("tr"):

        stats_arr = []
        for td in team.findAll('td'):
            stats_arr.append(td.text)

        if len(stats_arr) > 0:
            teams.append(Team(stats_arr))  

    return teams


@app.route("/")
def hello():
    # Scrape site for newest stats
    html = requests.get('http://kenpom.com/')
    soup = BeautifulSoup(html.text, "lxml")
    teams = retrieve_teams(soup)

    # Or read from file
    # teams = read_teams()
    return render_template('index.html', teams=teams)

@app.route("/<year>")
def change_year(year):
    html = requests.get('http://kenpom.com/index.php?y=' + year)
    soup = BeautifulSoup(html.text, "lxml")
    teams = retrieve_teams(soup)
    return render_template('index.html', teams=teams)


if __name__ == '__main__':
    app.run()
