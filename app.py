import streamlit as st

'''
# Welcome to GoalGuru ⚽!

## Fun football forecasting 🔮. By fans, for fans.
'''

# vars for selecting the leagues and teams
# this is supposed to be given by the API

# API get_competitions()
# returns a list of dictionaries with the following structure
competitions = [
    {'competition_id': 0, 'name': 'Premier League'},
    {'competition_id': 1, 'name': 'Serie A'},
    {'competition_id': 2, 'name': 'Bundesliga'},
    {'competition_id': 3, 'name': 'La Liga'},
    {'competition_id': 4, 'name': 'World Cup'}
]

# API get_seasons(competition_id)
# returns a list of all the available seasons for the given competition_id, with
# the following structure
seasons = {
    0: [
        {'season_id': 0, 'name': '2016/2017', 'matchweeks': range(1,11), 'dataset': 'soccermatch'},
        {'season_id': 1, 'name': '2017/2018', 'matchweeks': range(2,25), 'dataset': 'statsbomb'}
        ],
    1: [
        {'season_id': 0, 'name': '2015/2016', 'matchweeks': range(3,38), 'dataset': 'soccermatch'},
        {'season_id': 1, 'name': '2016/2017', 'matchweeks': range(4,7), 'dataset': 'statsbomb'}
        ],
    2: [
        {'season_id': 0, 'name': '2015/2016', 'matchweeks': range(5,11), 'dataset': 'soccermatch'}
        ],
    3: [
        {'season_id': 0, 'name': '2016/2017', 'matchweeks': range(6,15), 'dataset': 'statsbomb'},
        {'season_id': 1, 'name': '2017/2018', 'matchweeks': range(1,11), 'dataset': 'soccermatch'}
        ],
    4: [
        {'season_id': 0, 'name': '2018', 'matchweeks': range(1,8), 'dataset': 'statsbomb'}
        ]
}

# API get_matches(competition_id, season_id, matchweek, dataset (soccermatch or statsbomb))
# returns a list of all the matches for the given parameters, with the following
# structure. This method internally looks into the corresponding
#  dataset (soccermatch or statsbomb) and fetches the list of the matches
matches = {
    0: {
        0: {
            0: [
                {'match_id': 1545, 'name': 'Arsenal vs Tottenham'},
                {'match_id': 6545, 'name': 'ManU vs ManCity'}
                ]
            },
        1: {
            0: [
                {'match_id': 484, 'name': 'Liverpool vs Everton'},
                {'match_id': 6546, 'name': 'Burnley vs Wolves'}
                ]
            }
        },
    1: {
        0: {
            0: [
                {'match_id': 198, 'name': 'Inter vs Milan'},
                {'match_id': 1154, 'name': 'Juventus vs Torino'}
                ]
            },
        1: {
            0: [
                {'match_id': 1981, 'name': 'Lazio vs Fiorentina'},
                {'match_id': 62, 'name': 'Napoli vs Palermo'}
                ]
            }
        },
    2: {
        0: {
            0: [
                {'match_id': 654, 'name': 'Borussia Dortmund vs Bayern Munchen'},
                {'match_id': 98, 'name': 'Hannover vs Mainz'}
                ]
            }
        },
    3: {
        0: {
            0: [
                {'match_id': 78, 'name': 'Barcelona vs Real Madrid'},
                {'match_id': 14, 'name': 'Real Sociedad vs Athletic Bilbao'}
                ]
            },
        1: {
            0: [
                {'match_id': 1, 'name': 'Athletic Bilbao vs Real Madrid'},
                {'match_id': 2, 'name': 'Real Sociedad vs Barcelona'}
                ]
            }
        },
    4: {
        0: {
            0:[
                {'match_id': 33, 'name': 'Argentina vs France'},
                {'match_id': 55, 'name': 'Croatia vs England'}
                ]
            }
        },
}

# to show

competition_selected = st.selectbox('Select a competition',
                                    competitions,
                                    format_func=lambda x: x['name'])

st.write(f'you selected {competition_selected}')

season_selected = st.selectbox('Select a season',
                               seasons[competition_selected['competition_id']],
                               format_func=lambda x: x['name'])

st.write(f'you selected {season_selected}')

matchweek_selected = st.selectbox('Select a matchweek (round)',
                               season_selected['matchweeks'],
                               format_func=lambda x: f'Round {x}')

st.write(f'you selected {matchweek_selected}')

match_selected = st.selectbox('Select a match',
                               matches[competition_selected['competition_id']][season_selected['season_id']][0],
                               format_func=lambda x: x['name'])

st.write(f'you selected {match_selected}')
