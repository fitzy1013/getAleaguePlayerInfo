import discord
from bs4 import BeautifulSoup
import requests
import csv
import random
from table2ascii import table2ascii as t2a, PresetStyle


class Player:
    def __init__(self, id, name, position, club):
        self.name = name
        self.position = position
        self.club = club
        self.id = id

    def get_playerID(self):
        return self.id

    def print_info(self):
        return self.name + " " + self.position


try:
    source = requests.get('https://www.ultimatealeague.com/players/')
    source.raise_for_status()
except Exception as e:
    print(e)


def league_table_to_csv():
    with open('fbreference.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                try:
                    source2 = requests.get(row[1])
                    source2.raise_for_status()
                    id = row[2]
                except Exception as e:
                    print(e)
                soup = BeautifulSoup(source2.text, 'html.parser')
                table = soup.find('table', {'id': row[2]}).find('tbody').find_all('tr')

                table_list = []
                index = 1

                for team in table:
                    team_name = team.find('td', {'data-stat': 'team'}).a.text
                    gp = team.find('td', {'data-stat': 'games'}).text
                    gd = team.find('td', {'data-stat': 'goal_diff'}).text
                    pts = team.find('td', {'data-stat': 'points'}).text
                    table_entry = [index, team_name, gp, gd, pts]
                    table_list.append(table_entry)
                    index += 1

                header = ['pos', 'team', 'gp', 'gd', 'pts']
                with open('{}_table.csv'.format(row[0]), 'w', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(table_list)
            line_count += 1


def playerInfoToCSV():
    playerList = []
    soup = BeautifulSoup(source.text, 'html.parser')
    players = soup.find('table', {'id': 'players-data-table'}).find('tbody').find_all('tr')

    for player in players:
        name = player.find('div', {'class': 'player-link'}).a.text
        pos = player.find('td', {'class': 'data-table-desktop-hide data-table-cell'}).text
        club = player.find('div', {'class': 'club-link club-link-left'}).a.text
        playerEntry = [name, pos, club]
        playerList.append(playerEntry)

    header = ['name', 'pos', 'club']
    with open('a-league_players.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(playerList)


def checkIfPlayerInSquad(squad: [Player], playerID):
    for i in squad:
        if i.get_playerID() == playerID:
            return True

    return False


def getTable(league):
    team_list = []
    team = []
    with open('{}_table.csv'.format(league)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                team = [row[0], row[1], row[2], row[3], row[4]]
                team_list.append(team)
            line_count += 1

    return team_list


def getRandomXI():
    squad_string = ""
    gk_list = []
    def_list = []
    mid_list = []
    fwd_list = []
    with open('a-league_players.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                p = Player(line_count, row[0], row[1], row[2])
                if row[1] == "GK":
                    gk_list.append(p)
                elif row[1] == "DEF":
                    def_list.append(p)
                elif row[1] == "MID":
                    mid_list.append(p)
                elif row[1] == "FWD":
                    fwd_list.append(p)
            line_count += 1

    squad = []
    index = random.randint(0, len(gk_list) - 1)
    squad.append(gk_list[index])
    squad_string = squad_string + gk_list[index].print_info() + "\n"
    for i in range(0, 4):
        index = random.randint(0, len(def_list) - 1)
        if not checkIfPlayerInSquad(squad, def_list[index].get_playerID()):
            squad.append(def_list[index])
            squad_string = squad_string + def_list[index].print_info() + "\n"

    for i in range(0, 4):
        index = random.randint(0, len(mid_list) - 1)
        if not checkIfPlayerInSquad(squad, mid_list[index].get_playerID()):
            squad.append(mid_list[index])
            squad_string = squad_string + mid_list[index].print_info() + "\n"

    for i in range(0, 2):
        index = random.randint(0, len(fwd_list) - 1)
        if not checkIfPlayerInSquad(squad, fwd_list[index].get_playerID()):
            squad.append(fwd_list[index])
            squad_string = squad_string + fwd_list[index].print_info() + "\n"

    return squad_string


TOKEN = ""

with open('token.txt') as f:
    TOKEN = TOKEN + f.readline()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=discord.Intents.all())


def print_table(league):
    team_list = getTable(league)
    output = t2a(
        header=["Pos", "Team", "GP", "GD", "Pts"],
        body=team_list,
        style=PresetStyle.thin_compact
    )
    return output


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    message_low = message.content.lower()

    if message.author == client.user:
        return

    if message_low == '!ligue1-table':
        output = print_table("ligue1")
        await message.channel.send(f"```\n{output}\n```")

    if message_low == '!bundesliga-table':
        output = print_table("bundesliga")
        await message.channel.send(f"```\n{output}\n```")

    if message_low == '!la-liga-table':
        output = print_table("la-liga")
        await message.channel.send(f"```\n{output}\n```")

    if message_low == '!serie-a-table':
        output = print_table("serie-a")
        await message.channel.send(f"```\n{output}\n```")

    if message_low == '!epl-table':
        output = print_table("epl")
        await message.channel.send(f"```\n{output}\n```")

    if message_low == '!a-league-table':
        output = print_table("a-league")
        await message.channel.send(f"```\n{output}\n```")

    if message_low == '!randomxi':
        squad = getRandomXI()
        print("{} has requested randomxi".format(message.author))
        await message.channel.send("{} this is your Random 11\n\n{}".format(message.author, squad))

    if message_low == '!hello':
        await message.channel.send("Hello, {}!".format(message.author))

playerInfoToCSV()
league_table_to_csv()
client.run(TOKEN)
