import plotly.graph_objects as go
from PIL import Image
from ast import literal_eval
import datetime
from data_reader import get_data

# information = pd.read_csv('data/2021-Dec-16.csv')
information = get_data(
    'combined', datetime.datetime.now().strftime('%Y-%m-%d'))
information = information.set_index(
    keys='Team_name', drop=True).to_dict('index')

line_styles = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']


def plot_position(value):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=[-i for i in range(len(value))],
        x=[information[team]['Salaries_G'] for team in value],
        customdata=[team.capitalize() for team in value], hovertemplate='(%{customdata}, %{x:$.3s})',
        name='GOL',
        orientation='h',

        marker=dict(
            color='rgba(255, 0, 0, 0.6)',
            line=dict(color='rgba(255, 0, 0, 1.0)', width=3)
        )
    ))
    fig.add_trace(go.Bar(
        y=[-i for i in range(len(value))],
        x=[information[team]['Salaries_DEF'] for team in value],
        customdata=[team.capitalize() for team in value], hovertemplate='(%{customdata}, %{x:$.3s})',
        name='DEF',
        orientation='h',
        marker=dict(
            color='rgba(0, 0, 255, 0.6)',
            line=dict(color='rgba(0, 0, 255, 1.0)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=[-i for i in range(len(value))],
        x=[information[team]['Salaries_OFF'] for team in value],
        customdata=[team.capitalize() for team in value], hovertemplate='(%{customdata}, %{x:$.3s})',
        name='OFF',
        orientation='h',
        marker=dict(
            color='rgba(255, 153, 0, 0.6)',
            line=dict(color='rgba(255, 153, 0, 1.0)', width=3)
        )
    ))

    for row, team in enumerate(value):
        fig.add_layout_image(
            dict(
                source=Image.open('logos/'+team+'.png'),
                xref="x", yref="y",
                x=-100000, y=-row,
                xanchor='right', yanchor="middle",
                sizing='contain',

                sizex=10000000, sizey=0.8,

            )
        )
    fig.update_layout(barmode='stack')
    fig.update_yaxes(title='y', visible=False, showticklabels=False)
    fig.update_xaxes(title='Salary', ticksuffix='$',
                     range=[-10000000, 83000000])
    return fig


def plot_bracket(value):
    fig = go.Figure()
    colour_dict = dict()
    for team in value:
        colour_string = str(literal_eval(information[team]['Colour']))
        if colour_string in colour_dict:
            occurrence = colour_dict[colour_string]+1
        else:
            occurrence = 0
        colour_dict[colour_string] = occurrence
        fig.add_trace(go.Scatter(
            y=[information[team]['Comb_salaries' +
                                 str(bracket).zfill(2)] for bracket in range(11)],
            x=[i for i in range(11)],
            customdata=[team.capitalize() for bracket in range(11)],
            hovertemplate='(%{customdata}, %{y:$.3s})',
            name=team.capitalize(),
            line=dict(
                color='rgb'+colour_string, dash=line_styles[occurrence % 6],
                width=3),
            marker=dict(
                color='rgb'+colour_string,
                line=dict(color='rgb'+colour_string, width=3)
            )
        ))
    fig.update_xaxes(title='Salary',
                     ticktext=['($0.75M-$1.25M]', '($1.25M-$2.25M]', '($2.25M-$3.25M]',
                               '($3.25M-$4.25M]', '($4.25M-$5.25M]', '($5.25M-$6.25M]', '($6.25M-$7.25M]',
                               '($7.25M-$8.25M]', '($8.25M-$9.25M]', '($9.25M-$10.25M]', '($10.25M-]'],
                     tickvals=[i for i in range(11)],
                     type='category')
    return fig
