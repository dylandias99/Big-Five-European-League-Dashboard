import re
import io
import pandas as pd
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import matplotlib.pyplot as plt
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

external_stylesheets = ['http://fonts.cdnfonts.com/css/verlag']
buffer = io.StringIO()
pd.options.plotting.backend = "plotly"


def input2(input: int):
    file = "./Teams_Stats/Big_5_" + str(input) + ".csv"
    return pd.read_csv(file, parse_dates=True)

def team_names_list(cL):
    names = list(cL['Squad'])
    return names

def league_table(pL, league):
    league_team = pL[pL['Country'] == league]
    league_team_names = league_team.sort_values(by='LgRk', ascending=True)
    return league_team_names

def all_teams_name(season):
    df = input2(season)
    all_names = df.sort_values(by=['Squad']).drop_duplicates(subset=['Squad'])
    all_teams_name = list(all_names['Squad'])
    return all_teams_name

def winning_team(pL):
    win_team = pL[pL["LgRk"] == 1].sort_values(by='Pts', ascending=False)
    return win_team

def relegated_teams(pL):
    rel_team = pL[pL["League_Status"] == "Relegated"].sort_values(by='Pts', ascending=False)
    return rel_team

def figures(pL):
    won = winning_team(pL)
    figure_1 = px.bar(won, x='Squad', y='Pts', color='Squad', text='Pts')
    figure_1.update_layout(
        font=dict(
            family="'Verlag', sans-serif",
            color="darkblue"
        )
    )
    rel = relegated_teams(pL)
    figure_2 = px.scatter(rel, x="Country", y="Pts", color='Country', size='Pts', hover_data=['Squad'])
    return figure_1, figure_2

def polar_plot(pL, team):
    stat_team = pL[pL["Squad"].isin(team)]
    stats = stat_team.sort_values(by=['Squad'])
    stats_list = stats[['MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']].values.tolist()
    Attribute = ["Matches Played", "Wins", "Draws", "Losses", "Goals For", "Goals Against", "Goal \nDifference",
                 "Points"]
    figure_3 = px.line_polar(line_close=True)
    figure_3.update_layout(title="Team Stats", font_size=14, polar=dict(bgcolor="#F0F8FF", angularaxis=dict(
        gridcolor='#40E0D0'
    ), radialaxis=dict(gridcolor="#40E0D0", linecolor="#40E0D0")), font=dict(
        family="'Verlag', sans-serif",
        color="#003399",
    ),
                           paper_bgcolor="white")
    team_name = sorted(team)
    for i in range(0, len(stats_list)):
        figure_3.add_trace(go.Scatterpolar(
            r=stats_list[i],
            theta=Attribute,
            fill='toself',
            name=team_name[i]
        ))
        i += 1
    return figure_3

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18em",
    "padding": "2rem 1rem",
    "background-color": "#002D72",
    "text-align": 'center'
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Team Stats Description

test_tab = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Button('Introduction', id="intro_button", className="test_buttons", n_clicks=0,
                                style={'border-radius': '25px 0 0 0'}),
                    html.Button('Data Description', id="data_button", className="test_buttons", n_clicks=0),
                    html.Button(['League Tabel'], id="league_button", className="test_buttons", n_clicks=0),
                    html.Button(['Winning Teams'], id="winning_button", className="test_buttons", n_clicks=0),
                    html.Button(['Relegated Teams'], id="relegated_button", className="test_buttons", n_clicks=0),
                    html.Button(['Polar Chart'], id="polar_button", className="test_buttons", n_clicks=0,
                                style={'border-radius': '0 0 0 25px'}),
                ], className="test_but"),
            ], className="cont_but_1"),
            html.Div([
                html.Div([], id="test_button_output", className="test_output"),
            ], className="cont_but_2"),
        ], className="test_button_container")
    ])
])

# Side Navigation Bar

sidebar = html.Div([
    dbc.Nav([
        html.Div([
            dbc.NavLink("Home", href="/", active="exact", className="links",
                        style={'text-decoration': 'none', 'color': '#002D72'}),
            dbc.NavLink("Team Stats", href="/team-page", className='links', active="exact",
                        style={'text-decoration': 'none', 'color': '#002D72'}),
            # dbc.NavLink("Player Stats", href="/player-page", className='links', active="exact",
            #             style={'text-decoration': 'none', 'color': '#002D72'}),
            html.H4('Select Season', className='nav_link_season_title'),
            html.Div([
                dcc.RadioItems(
                    id='season-radio',
                    options=[
                        {'label': ' 2015/16', 'value': 0},
                        {'label': ' 2016/17', 'value': 1},
                        {'label': ' 2017/18', 'value': 2},
                        {'label': ' 2018/19', 'value': 3},
                        {'label': ' 2019/20', 'value': 4},
                        {'label': ' 2020/21', 'value': 5}
                    ],
                    value=0,
                    style={
                        'margin': '1em 0 0 0',
                        'display': 'grid',
                        'grid-template-columns': 'auto auto',
                        'grid-row-gap': '1em',
                        'color': '#002D72',
                        'font-size': '1.1em',
                        'align-content': 'center'
                    }
                ),
            ], className='season_values')
        ], className='nav_links')
    ], vertical=True, pills=True, className='nav-bar'),
], style=SIDEBAR_STYLE, )

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
application = app.server
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
])


@app.callback(Output('test_button_output', 'children'),
              dash.dependencies.Input('intro_button', 'n_clicks'),
              dash.dependencies.Input('data_button', 'n_clicks'),
              Input('league_button', 'n_clicks'),
              Input('winning_button', 'n_clicks'),
              Input('relegated_button', 'n_clicks'),
              Input('polar_button', 'n_clicks'))
def displayClick(btn1, btn2, btn3, btn4, btn5, btn6):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'intro_button' in changed_id:
        return "The teams stats page consists of visualizations and tables about the data. Below is a description of the data-set and types of visualization you will come across."
    elif 'data_button' in changed_id:
        return html.Div([
            html.Ul([
                html.Div([
                    html.Div([
                        html.Li(['Rk: Indicates the rank of the team in the Big 5 European League.']),
                        html.Li(['Squad: Name of the team.']),
                        html.Li(['Country: Name of the country the team represents.']),
                        html.Li(['LgRk: Position the team finished within the league.']),
                        html.Li(['MP: Total number of matches played.']),
                        html.Li(['W: Total wins.']),
                        html.Li(['D: Total draws.']),
                        html.Li(['L: Total loses.']),
                    ], className='attribute_2'),
                    html.Div([
                        html.Li(['GF: Goals for.']),
                        html.Li(['GA: Goals against.']),
                        html.Li(['GD: Goal difference.']),
                        html.Li(['Pts: Total points earned.']),
                        html.Li(['Pts/G: Points per game.']),
                        html.Li(['Attendance: Attendance per game during this season (only for home games).']),
                        html.Li([
                                    'Top Team Scorer: Name of the teams top scorer along with the number of goals scored (only for league games.']),
                        html.Li(['Goalkeeper: Name of the goalkeeper.']),
                    ], className='attribute_2')
                ], style={'margin': '0 0em 0 -3.3em', 'display': 'grid', 'grid-column-gap': '1em',
                          'padding': '0 0 0 0em', 'grid-template-columns': '14em 16em', 'text-align': 'justify',
                          'text-justify': 'inter-word', 'list-style-type': 'none'}, className="attribute_list")
            ], style={'transform': 'scale(0.82)'})
        ])
    elif 'league_button' in changed_id:
        return "The league table shows the ranking of teams based on points at the end of the season. If you see the league table for other leagues, just click on the desired leagues button."
    elif 'winning_button' in changed_id:
        return "This section shows the teams ranked first in their league and sorted by their points."
    elif 'relegated_button' in changed_id:
        return "This section shows the teams that will be demoted to the league below and sorted by their points."
    elif 'polar_button' in changed_id:
        return "This section shows a polar plot for stats for select teams. You can simply search for the team in the drop down and it will keep adding the stats for the selected teams in the same plot. If the team wasn’t present that season it will show a message 'One of the selected team was relegated'."
    else:
        return "Team Stats information"


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"),
     dash.dependencies.Input('season-radio', 'value')]
)
def render_page_content(pathname, season):
    if pathname == "/":
        return [
            html.H1(['Big 5 European Leagues'], className='page-title'),
            html.Div([
                html.Div([
                    html.Div('About the Application', className="test_item_1 test_title test_title_1"),
                    html.Div(
                        "This application is built using data-sets from the FBREF website. These data-sets consist of season wise stats for all teams and players in the Big 5 European League. The Big 5 European League consists of the Premier League, Bundesliga, La Liga, Serie A, and Ligue 1. Using this data we are able to create various interactive visualization, and tables based on certain queries for teams in the Big 5 League.",
                        className="test_item_2"),
                    html.Div('Team Stats Section', className="test_item_3 test_title test_title_2"),
                    html.Div(test_tab, className="test_item_4"),
                ], className="test_grid")
            ], className="test_container")
        ]
    elif pathname == "/team-page":
        return [
            html.H1(['Big 5 European Leagues'], style={'font-style': 'normal'}, className='page-title'),
            html.Div(id='slider-output-container', className="slider-container"),
        ]






@app.callback(Output('container-button-timestamp', 'children'),
              dash.dependencies.Input('season-radio', 'value'),
              Input('prem-btn', 'value'),
              Input('ligue-btn', 'value'),
              Input('laliga-btn', 'value'),
              Input('bundesliga-btn', 'value'),
              Input('serie-a-btn', 'value'),
              Input('prem-btn', 'n_clicks'),
              Input('ligue-btn', 'n_clicks'),
              Input('laliga-btn', 'n_clicks'),
              Input('bundesliga-btn', 'n_clicks'),
              Input('serie-a-btn', 'n_clicks'))
def displayClick(season, eng, fre, esp, ger, ita, btn1, btn2, btn3, btn4, btn5):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'prem-btn' in changed_id:
        league = eng
    elif 'ligue-btn' in changed_id:
        league = fre
    elif 'laliga-btn' in changed_id:
        league = esp
    elif 'bundesliga-btn' in changed_id:
        league = ger
    elif 'serie-a-btn' in changed_id:
        league = ita
    else:
        league = eng
    pL = input2(season)
    league_teams = league_table(pL, league)
    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in
                     league_teams[['LgRk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']].columns],
            data=league_teams[['LgRk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']].to_dict('records'),
            fixed_rows={'headers': True},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#1877F2',
                    'color': 'white'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': '#1877F2',
                    'color': 'white'
                }
            ],
            style_cell={'padding': '5px'},
            style_cell_conditional=[
                {'if': {'column_id': 'LgRk'},
                 'width': '5em'},
            ],
            style_data={
                'font-family': '"Verlag", sans-serif',
                'text-align': 'center',
                'font-size': '12px',
                'padding': '10px',
            },
            style_table={
                'overflowX': 'auto',
                'overflowY': 'auto',
                'width': '35em',
                'height': '40em',
            },
            style_header={
                'padding': '10px',
                'font-family': '"Verlag", sans-serif',
                'backgroundColor': '#002D72',
                'color': 'white',
                'text-align': 'center',
                'font-size': '15px'
            }),
    ], className='sub_layer_table', style={'margin': '3em 0 0 0', "position": "static"})


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value'),
    dash.dependencies.Input('season-radio', 'value'))
def update_output(team, season):
    pL = input2(season)
    team_name = team_names_list(pL)
    polar = polar_plot(pL, team)
    if set(team).issubset(set(team_name)):
        return html.Div([dcc.Graph(id="graph", figure=polar)], style={'margin': '0em 0 0 0', 'width': '40em'}),
    else:
        return "One of the selected team was relegated"

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('season-radio', 'value')])
def update_output(value):
    pL = input2(value)
    won = winning_team(pL)
    relegated = relegated_teams(pL)
    all_teams = all_teams_name(value)
    fig3, fig4 = figures(pL)
    return html.Div([
        html.Div(['League Table'], style={'text-align': 'center'}, className='sub_layer_1 sub_layer_title_1'),
        html.Div([
            html.Div([html.Span(['Select League'], className="icon_title"),
                      html.Button(html.Img(src='assets/premier.png',
                                           style={'width': '8em', 'padding': '8px', 'height': '8em',
                                                  'text-decoration': 'none'}), id='prem-btn',
                                  style={'background-color': 'white', 'border-radius': '20px',
                                         'border': '2px solid #132257', 'cursor': 'pointer'}, n_clicks=0,
                                  value="ENG", className="btn1"),
                      html.Button(html.Img(src='assets/bundesliga.png',
                                           style={'width': '8em', 'padding': '8px', 'height': '8em',
                                                  'text-decoration': 'none'}), id='bundesliga-btn',
                                  style={'background-color': 'white', 'border-radius': '20px',
                                         'border': '2px solid red', 'cursor': 'pointer'}, n_clicks=0, value="GER",
                                  className="btn2"),
                      html.Button(html.Img(src='assets/ligue_1.png',
                                           style={'width': '6em', 'border-radius': '30px', 'padding': '8px',
                                                  'height': '8em', 'text-decoration': 'none'}), id='ligue-btn',
                                  style={'background-color': 'white', 'border-radius': '20px',
                                         'border': '2px solid #132257', 'cursor': 'pointer'}, n_clicks=0,
                                  value="FRA", className="btn3"),
                      html.Button(html.Img(src='assets/laliga.png',
                                           style={'width': '6em', 'padding': '8px', 'height': '8em',
                                                  'text-decoration': 'none'}), id='laliga-btn',
                                  style={'background-color': 'white', 'border-radius': '20px',
                                         'border': '2px solid black', 'cursor': 'pointer'}, n_clicks=0, value="ESP",
                                  className="btn4"),
                      html.Button(html.Img(src='assets/serie-a.png',
                                           style={'width': '5em', 'padding': '8px', 'height': '8em',
                                                  'text-decoration': 'none'}, className="serie_img"), id='serie-a-btn',
                                  style={'background-color': 'white', 'border-radius': '20px',
                                         'border': '2px solid #024494', 'cursor': 'pointer'}, n_clicks=0,
                                  value="ITA", className="btn5")
                      ], className='flex-buttons')
        ], style={'margin': "5em 0 0 0em"}, className='sub_layer_2'),
        html.Div(id='container-button-timestamp', className='sub_layer_3', style={'margin': '0 0em 0 -8em'}),
        html.Div(['Winning teams from each league'], style={'text-align': 'center'},
                 className='sub_layer_4 sub_layer_title_2'),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in
                         won[["Squad", "Pts", "Country", "Top Team Scorer", "Goalkeeper"]].columns],
                data=won[["Squad", "Pts", "Country", "Top Team Scorer", "Goalkeeper"]].to_dict('records'),
                fixed_rows={'headers': True},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#1877F2',
                        'color': 'white'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#1877F2',
                        'color': 'white'
                    }
                ],
                style_cell={'padding': '5px'},
                style_cell_conditional=[
                    {'if': {'column_id': 'Country'},
                     'width': '6em'},
                    {'if': {'column_id': 'Pts'},
                     'width': '4em'},
                ],
                style_data={
                    'font-family': '"Verlag", sans-serif',
                    'text-align': 'center',
                    'font-size': '12px',
                    'padding': '10px',
                },
                style_table={
                    'overflowX': 'auto',
                    'overflowY': 'auto',
                    'width': '30em'
                },
                style_header={
                    'padding': '10px',
                    'font-family': '"Verlag", sans-serif',
                    'backgroundColor': '#002D72',
                    'color': 'white',
                    'text-align': 'center',
                    'font-size': '15px'
                }),
        ], className='sub_layer_5 sub_layer_table', style={'margin': '6em 0 0 0'}),
        html.Div([dcc.Graph(id="graph", figure=fig3)], style={'margin': '0 0 0 0', 'width': '30em', 'height': '10em'},
                 className='sub_layer_6 sub_layer_graph'),
        html.Div(['Relegated teams from each league'], style={'text-align': 'center'},
                 className='sub_layer_7 sub_layer_title_3'),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in
                         relegated[["Squad", "Pts", "Country", "Top Team Scorer", "Goalkeeper"]].columns],
                data=relegated[["Squad", "Pts", "Country", "Top Team Scorer", "Goalkeeper"]].to_dict('records'),
                fixed_rows={'headers': True},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#1877F2',
                        'color': 'white'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#1877F2',
                        'color': 'white'
                    }
                ],
                style_cell={'padding': '5px'},
                style_data={
                    'font-family': '"Verlag", sans-serif',
                    'text-align': 'center',
                    'font-size': '12px',
                    'padding': '10px',
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'Pts'},
                     'width': '4em'},
                    {'if': {'column_id': 'Country'},
                     'width': '6em'},
                ]
                ,
                style_table={
                    'overflowX': 'auto',
                    'overflowY': 'auto',
                    'width': '30em',
                    'height': '30em',
                },
                style_header={
                    'padding': '10px',
                    'font-family': '"Verlag", sans-serif',
                    'backgroundColor': '#002D72',
                    'color': 'white',
                    'text-align': 'center',
                    'font-size': '15px'
                }),
        ], className='sub_layer_8 sub_layer_table', style={'margin': '3em 0 0 0'}),
        html.Div([dcc.Graph(id="graph", figure=fig4)], style={'margin': '4em 0 0 0', 'width': '30em'},
                 className='sub_layer_9 sub_layer_graph'),
        html.Div(['Polar plot to display season wise stats for teams in the Big 5 League'],
                 style={'text-align': 'center'}, className='sub_layer_10 sub_layer_title_4'),
        html.Div([
            dcc.Dropdown(
                id='demo-dropdown',
                options=[
                    {'label': i, 'value': i} for i in all_teams
                ],
                value=[],
                multi=True
                , style={
                    'width': '40em',
                    'color': '#003399',
                }), html.Div(id='dd-output-container', style={'position': 'relative'})
        ], className='sub_layer_11 sub_layer_polar'),
    ], className='container'),


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    Input('season-radio', 'value'),
    dash.dependencies.Input('submit-val', 'value'),
    dash.dependencies.Input('submit-val-2', 'value'),
    dash.dependencies.Input('submit-val', 'n_clicks'),
    dash.dependencies.Input('submit-val-2', 'n_clicks'))
def update_output(season, league_1, league_2, league_btn_1, league_btn_2):
    pL = input2(season)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit-val' in changed_id:
        league_teams = league_table(pL, league_1)
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in
                         league_teams[['LgRk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']].columns],
                data=league_teams[['LgRk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']].to_dict('records'),
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#1877F2',
                        'color': 'white'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#1877F2',
                        'color': 'white'
                    }
                ],
                style_cell={'padding': '5px'},
                style_data={
                    'font-family': '"Verlag", sans-serif',
                    'text-align': 'center',
                    'font-size': '12px',
                    'padding': '10px',
                },
                style_table={
                    'overflowX': 'auto',
                    'width': '30em'

                },
                style_header={
                    'padding': '10px',
                    'font-family': '"Verlag", sans-serif',
                    'backgroundColor': '#002D72',
                    'color': 'white',
                    'text-align': 'center',
                    'font-size': '15px'
                }),
        ], className='sub_layer_5 sub_layer_table', style={'margin': '3em 0 0 0'})
    elif 'submit-val-2' in changed_id:
        league_teams = league_table(pL, league_2)
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in
                         league_teams[['LgRk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']].columns],
                data=league_teams[['LgRk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']].to_dict('records'),
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#1877F2',
                        'color': 'white'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#1877F2',
                        'color': 'white'
                    }
                ],
                style_cell={'padding': '5px'},
                style_data={
                    'font-family': '"Verlag", sans-serif',
                    'text-align': 'center',
                    'font-size': '12px',
                    'padding': '10px',
                },
                style_table={
                    'overflowX': 'auto',
                    'width': '30em'

                },
                style_header={
                    'padding': '10px',
                    'font-family': '"Verlag", sans-serif',
                    'backgroundColor': '#002D72',
                    'color': 'white',
                    'text-align': 'center',
                    'font-size': '15px'
                }),
        ], className='sub_layer_5 sub_layer_table', style={'margin': '3em 0 0 0'})



if __name__ == '__main__':
    application.run(debug=True, port=8080)
