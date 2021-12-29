import urllib3
import re
from sql_connection import get_data, append_data
from team_dict import TEAMS
import pandas as pd
import datetime

now = datetime.datetime.utcnow()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http = urllib3.PoolManager()

URL_BASE = 'https://www.capfriendly.com/teams/'

# regex anchors
UNITS = 'style="width:195px">TOTAL'
BEFORE = 'cap rel mtv">$'
AFTER = '<'
PLAYER = '/transactions/players/'


def flatten(listlist):
    return [[item for List in listlist for item in List]][0]


COLUMNS = ['Team_name', 'Conference', 'Division', 'Scraping_date']
easier_player_columns = [['OFF_players' + f'{i:02}' for i in range(11)], ['Players_OFF'],
                         ['DEF_players' +
                             f'{i:02}' for i in range(11)],  ['Players_DEF'],
                         ['G_players' +
                             f'{i:02}' for i in range(11)], ['Players_G'],
                         ['Comb_players'+f'{i:02}' for i in range(11)], ['Total_players']]
easier_salary_columns = [['OFF_salaries'+f'{i:02}' for i in range(11)], ['Salaries_OFF'],
                         ['DEF_salaries' +
                             f'{i:02}' for i in range(11)], ['Salaries_DEF'],
                         ['G_salaries' +
                             f'{i:02}' for i in range(11)], ['Salaries_G'],
                         ['Comb_salaries'+f'{i:02}' for i in range(11)], ['Total_salaries']]
COLUMNS.extend(flatten(easier_player_columns))
COLUMNS.extend(flatten(easier_salary_columns))


def download(URL):
    try:
        r = http.request('GET', URL)  # get the actual site
    except Exception as ex:
        print(ex)
        print('Internet not working.')
        quit()
    page = r.data.decode('UTF-8')
    return page


def calculate_combined(List):
    combined_meta = [sum([unit[i] for unit in List])
                     for i in range(len(List[0][:-1]))]
    total_meta = sum(combined_meta)
    return combined_meta, total_meta


def clip_salary(player):
    before_cut = re.split(re.escape(BEFORE), player)[1]
    after_cut = re.split(AFTER, before_cut)[0]
    salary = int(after_cut.replace(',', ''))
    return salary


def calc_bracket(salary):
    unclipped_bracket = int((salary - 1250000)/1000000)
    bracket = max(min(unclipped_bracket, 10), 0)
    return bracket


def parse_group(group):
    players = re.split(PLAYER, group)[1:]
    player_bracket = [0]*11
    salary_bracket = [0]*11
    player_group = 0
    salary_group = 0
    for player in players:
        if BEFORE in player:
            salary = clip_salary(player)
            bracket = calc_bracket(salary)
            player_bracket[bracket] += 1
            player_group += 1
            salary_bracket[bracket] += salary
            salary_group += salary
    player_bracket.append(player_group)
    salary_bracket.append(salary_group)
    return salary_bracket, player_bracket


def get_team(identifier, team_background):
    output = re.split(UNITS, download(URL_BASE+identifier), 3)
    [forwards, defence, goalies, _] = output

    groups = [forwards, defence, goalies]
    team_salaries = []
    team_players = []
    for group in groups:
        salaries, players = parse_group(group)
        team_salaries.append(salaries)
        team_players.append(players)

    combined_salaries, total_salaries = calculate_combined(team_salaries)
    combined_players, total_players = calculate_combined(team_players)
    flat_team_salaries = flatten(team_salaries)
    flat_team_players = flatten(team_players)

    data = [flatten([list(team_background[team_background['Team_name'] == identifier].iloc[0]),
                     [now.strftime('%Y-%m-%d')],
                     flat_team_players, combined_players, [total_players],
                     flat_team_salaries, combined_salaries, [total_salaries]])]
    return pd.DataFrame(data=data, columns=COLUMNS)


def aggregate_df(df):
    division_df = df.drop(['Team_name', 'Conference'
                           ], axis='columns')
    division_df = division_df.groupby('Division').mean().convert_dtypes()
    division_df['Team_name'] = division_df.index
    division_df['Scraping_date'] = [
        now.strftime('%Y-%m-%d')]*len(division_df.index)
    division_df['index'] = range(len(division_df.index))
    division_df = division_df.set_index('index')

    conference_df = df.drop(
        ['Team_name', 'Division'  # , 'Scraping_date'
         ], axis='columns')
    conference_df = conference_df.groupby('Conference').mean().convert_dtypes()
    conference_df['Team_name'] = conference_df.index
    conference_df['Scraping_date'] = [
        now.strftime('%Y-%m-%d')]*len(conference_df.index)
    conference_df['index'] = range(len(conference_df.index))
    conference_df = conference_df.set_index('index')

    league_df = df.drop(
        ['Team_name', 'Division', 'Conference'
         ], axis='columns')
    league_df = league_df.mean().to_frame().transpose().convert_dtypes()
    LEAGUES = pd.DataFrame(data=[['NHL', now.strftime(
        '%Y-%m-%d')]], columns=['Team_name', 'Scraping_date'])
    league_df = pd.concat([LEAGUES, league_df], axis=1)
    return pd.concat([division_df, conference_df, league_df])


if __name__ == "__main__":
    team_stats = pd.DataFrame(columns=COLUMNS)
    start_year = now.year
    if now.month < 9:
        start_year = start_year-1
    team_background = get_data(
        'team_data', datetime.datetime.now().strftime('%Y'))
    team_background = team_background.drop(
        ['Start_year', 'Colour'], axis='columns')
    print('Started working on getting teams.')
    for team in TEAMS:
        print('Working on '+str(team))
        team_frame = get_team(team, team_background)
        team_stats = team_stats.append(team_frame, ignore_index=True)
    team_stats = team_stats.convert_dtypes()
    aggregated_df = aggregate_df(team_stats)
    team_stats = team_stats.drop(['Division', 'Conference'], axis='columns')
    team_stats = team_stats.append(aggregated_df, ignore_index=True)
    append_data(team_stats, 'salary_data')
    # team_stats.to_csv('data/'+str(now.strftime('%Y-%m-%d'))+'.csv')
