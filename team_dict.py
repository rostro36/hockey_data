from datetime import date

today = date.today()

DATE = today.strftime("%Y-%b-%d")

TEAMS = dict({'bruins': ['bruins', 'East', 'ATL', (252, 181, 20)],
              'canadiens': ['canadiens', 'East', 'ATL', (175, 30, 45)],
              'lightning': ['lightning', 'East', 'ATL', (0, 40, 104)],
              'mapleleafs': ['mapleleafs', 'East', 'ATL', (0, 32, 91)],
              'panthers': ['panthers', 'East', 'ATL', (4, 30, 66)],
              'redwings': ['redwings', 'East', 'ATL', (206, 17, 38)],
              'sabres': ['sabres', 'East', 'ATL', (0, 38, 84)],
              'senators': ['senators', 'East', 'ATL', (197, 32, 50)],
              'bluejackets': ['bluejackets', 'East', 'MET', (0, 38, 84)],
              'capitals': ['capitals', 'East', 'MET', (4, 30, 66)],
              'devils': ['devils', 'East', 'MET', (206, 17, 38)],
              'flyers': ['flyers', 'East', 'MET', (247, 73, 2)],
              'hurricanes': ['hurricanes', 'East', 'MET', (226, 24, 54)],
              'islanders': ['islanders', 'East', 'MET', (0, 83, 155)],
              'penguins': ['penguins', 'East', 'MET', (0, 0, 0)],
              'rangers': ['rangers', 'East', 'MET', (0, 56, 168)],
              'avalanche': ['avalanche', 'West', 'CEN', (111, 38, 61)],
              'blackhawks': ['blackhawks', 'West', 'CEN', (207, 10, 44)],
              'blues': ['blues', 'West', 'CEN', (0, 47, 135)],
              'coyotes': ['coyotes', 'West', 'CEN', (140, 38, 51)],
              'jets': ['jets', 'West', 'CEN', (4, 30, 66)],
              'predators': ['predators', 'West', 'CEN', (255, 184, 28)],
              'stars': ['stars', 'West', 'CEN', (0, 104, 71)],
              'wild': ['wild', 'West', 'CEN', (2, 73, 48)],
              'canucks': ['canucks', 'West', 'PAC', (0, 32, 91)],
              'ducks': ['ducks', 'West', 'PAC', (252, 76, 2)],
              'flames': ['flames', 'West', 'PAC', (200, 16, 46)],
              'goldenknights': ['goldenknights', 'West', 'PAC', (185, 151, 91)],
              'kings': ['kings', 'West', 'PAC', (17, 17, 17)],
              'kraken': ['kraken', 'West', 'PAC', (0, 22, 40)],
              'oilers': ['oilers', 'West', 'PAC', (4, 30, 66)],
              'sharks': ['sharks', 'West', 'PAC', (0, 109, 117)],
              })

DIVISIONS = dict({'ATL': ['ATL', 'East', 'ATL', (206, 17, 38)],
                  'MET': ['MET', 'East', 'MET', (185, 151, 91)],
                  'CEN': ['CEN', 'West', 'CEN', (0, 47, 135)],
                  'PAC': ['PAC', 'West', 'PAC', (0, 104, 71)]})

CONFERENCES = dict({'East': ['East', 'East', '-', (206, 17, 38)],
                   'West': ['West', 'West', '-', (0, 47, 135)]})
