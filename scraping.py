import urllib3
import re
from team_dict import TEAMS, DIVISIONS, CONFERENCES, DATE
import pandas as pd

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


COLUMNS = ['ID', 'Conference', 'Division', 'Colour']
easier_player_columns = [['OFF players' + f'{i:02}' for i in range(11)], ['Players OFF'],
                         ['DEF players' +
                             f'{i:02}' for i in range(11)],  ['Players DEF'],
                         ['G players' +
                             f'{i:02}' for i in range(11)], ['Players G'],
                         ['Comb players'+f'{i:02}' for i in range(11)], ['Total players']]
easier_salary_columns = [['OFF salaries'+f'{i:02}' for i in range(11)], ['Salaries OFF'],
                         ['DEF salaries' +
                             f'{i:02}' for i in range(11)], ['Salaries DEF'],
                         ['G salaries' +
                             f'{i:02}' for i in range(11)], ['Salaries G'],
                         ['Comb salaries'+f'{i:02}' for i in range(11)], ['Total salaries']]
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


def get_team(identifier):
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
    data = [flatten([TEAMS[identifier], flat_team_players, combined_players, [
                    total_players], flat_team_salaries, combined_salaries, [total_salaries]])]
    return pd.DataFrame(data=data, columns=COLUMNS)


def aggregate_df(df):
    division_df = df.drop(['ID', 'Conference', 'Colour'], axis='columns')
    division_df = division_df.groupby('Division').mean().convert_dtypes()
    division_df = DIVISIONS.merge(division_df, on='Division', how='inner')

    conference_df = df.drop(['ID', 'Division', 'Colour'], axis='columns')
    conference_df = conference_df.groupby('Conference').mean().convert_dtypes()
    conference_df = CONFERENCES.merge(
        conference_df, on='Conference', how='inner')

    league_df = df.drop(
        ['ID', 'Division', 'Conference', 'Colour'], axis='columns')
    league_df = league_df.mean().to_frame().transpose().convert_dtypes()
    LEAGUES = pd.DataFrame(data=[['nhl', '-', '-', (0, 0, 0)]],
                           columns=['ID', 'Conference', 'Division', 'Colour'])
    league_df = pd.concat([LEAGUES, league_df], axis=1)
    return pd.concat([division_df, conference_df, league_df])


if __name__ == "__main__":
    team_stats = pd.DataFrame(columns=COLUMNS)
    print('Started working on getting teams.')
    for team in TEAMS:
        print('Working on '+str(team))
        team_frame = get_team(team)
        team_stats = team_stats.append(team_frame, ignore_index=True)
    team_stats = team_stats.convert_dtypes()
    aggregated_df = aggregate_df(team_stats)
    team_stats = team_stats.append(aggregated_df, ignore_index=True)
    team_stats.to_csv('data/'+DATE+'.csv')
