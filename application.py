# import flask
import dash
import dash_html_components as html
import dash_core_components as dcc
from team_dict import TEAMS
from plotting import plot_bracket, plot_position

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

options = ['NHL', 'East', 'West', 'ATL',
           'MET', 'CEN', 'PAC']
options.extend([key for key in TEAMS])

# server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
application = app.server
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

index_page = html.Div([
    dcc.Link('Go to bracket overview', href='/bracket'),
    html.Br(),
    dcc.Link('Go to position overview', href='/position'),
])

position_page = html.Div([
    dcc.Dropdown(
        id='position-dropdown',
        options=[{'label': key, 'value': key} for key in options],
        value=['NHL'],
        multi=True
    ),
    html.Div(id='position-content'),
    dcc.Markdown('''# Position overview
This plot shows the roster cap (not in IR, LTIR, "non-roster", taxi squad and no dead cap)
of different teams and the average of divisions, conferences and the whole league as listed on
[CapFriendly](https://www.capfriendly.com/).

This view compares the expenses for the different positions across teams.

One can hover for the exact numbers.

The amount and order of the teams is based on the selection at the top of the page, which can also be searched.
## Other links
- [Go to bracket overview](./bracket)
- [Go back to home](.)''')
])


@app.callback(dash.dependencies.Output('position-content', 'children'),
              [dash.dependencies.Input('position-dropdown', 'value')])
def return_position(value):
    if value is None or len(value) == 0 or value == 'Teams':
        return 'Teams'
    return dcc.Graph(figure=plot_position(value))


bracket_page = html.Div([
    dcc.Dropdown(
        id='bracket-dropdown',
        options=[{'label': key, 'value': key} for key in options],
        value=['NHL'],
        multi=True
    ),
    dcc.Markdown('''# Salary bracket overview
This plot shows the roster cap (not in IR, LTIR, "non-roster", taxi squad and no dead cap)
of different teams and the average of divisions, conferences and the whole league as listed on
[CapFriendly](https://www.capfriendly.com/) in USD.

This view compares the amount of money spent in different salary brackets.
So if there are five million $ spent in the one million $ bracket,
this implies that there are five players making around one million $ each.

This gives interesting insights where money is spent for one team: rather the depth or the top?

Also a comparison between teams can yield interesting results.

One can hover for the exact numbers.

The amount and order of the teams is based on the selection at the top of the page, which can also be searched.
## Other links
- [Go to position overview](./position)
- [Go back to home](.)''')
])


@app.callback(dash.dependencies.Output('bracket-content', 'children'),
              [dash.dependencies.Input('bracket-dropdown', 'value')])
def return_bracket(value):
    if value is None or len(value) == 0 or value == 'Teams':
        return 'Teams'
    return dcc.Graph(figure=plot_bracket(value))


@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def select_page(pathname):
    if pathname.endswith('position'):
        return position_page
    if pathname.endswith('bracket'):
        return bracket_page
    return index_page


if __name__ == '__main__':
    application.run(debug=True, port=5000)
