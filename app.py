import streamlit as st

'''
# Welcome to GoalGuru ⚽!

## Fun football forecasting 🔮. By fans, for fans.
'''

# vars for selecting the leagues and teams
# this is supposed to be given by the API

# API get_competitions
competitions = [
    {'competition_id': 0, 'name': 'Premier League'},
    {'competition_id': 1, 'name': 'Serie A'},
    {'competition_id': 2, 'name': 'Bundesliga'},
    {'competition_id': 3, 'name': 'La Liga'},
    {'competition_id': 4, 'name': 'World Cup'}
]

# API get_seasons with competition_id
seasons = {
    0: [{'season_id': 0, 'name': '2016/2017', 'matchweeks': range(1,11)},
        {'season_id': 1, 'name': '2017/2018', 'matchweeks': range(2,25)}],
    1: [{'season_id': 0, 'name': '2015/2016', 'matchweeks': range(3,38)},
        {'season_id': 1, 'name': '2016/2017', 'matchweeks': range(4,7)}],
    2: [{'season_id': 0, 'name': '2015/2016', 'matchweeks': range(5,11)}],
    3: [{'season_id': 0, 'name': '2016/2017', 'matchweeks': range(6,15)},
        {'season_id': 1, 'name': '2017/2018', 'matchweeks': range(1,11)}],
    4: [{'season_id': 0, 'name': '2018', 'matchweeks': range(1,8)}]
}

# API get_matches with competition_id, season_id, matchweek, maybe model (soccermatch or statsbomb)
# this dictionary should be indexed on the third level by the matchweek, as an
# example, this shows just one matchweek
matches = {
    0: {0: {0: [{'match_id': 1545,'name': 'Arsenal vs Tottenham'},
                {'match_id': 6545,'name': 'ManU vs ManCity'}]},
        1: {0: [{'match_id': 484,'name': 'Liverpool vs Everton'},
                {'match_id': 6546,'name': 'Burnley vs Wolves'}]}},
    1: {0: {},
        1: {}},
    2: {0: {}},
    3: {0: {},
        1: {}},
    4: {0: {}},
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
