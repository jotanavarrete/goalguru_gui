import streamlit as st
import requests
from collections import defaultdict
from utils.plots import show_probabilities_bar

'''
# Welcome to GoalGuru ⚽!

## Fun football forecasting 🔮. By fans, for fans.
'''

# vars for selecting the leagues and teams
# this is supposed to be given by the API

# API get_competitions()
# returns a list of dictionaries with the following structure
# competitions = [
#     {'competition_id': 0, 'competition_name': 'Premier League'},
#     {'competition_id': 1, 'competition_name': 'Serie A'},
#     {'competition_id': 2, 'competition_name': 'Bundesliga'},
#     {'competition_id': 3, 'competition_name': 'La Liga'},
#     {'competition_id': 4, 'competition_name': 'World Cup'}
# ]

# API get_seasons(competition_id)
# returns a list of all the available seasons for the given competition_id, with
# the following structure
# seasons = {
#     0: [
#         {'season_id': 0, 'name': '2016/2017', 'matchweeks': range(1,11), 'dataset': 'soccermatch'},
#         {'season_id': 1, 'name': '2017/2018', 'matchweeks': range(2,25), 'dataset': 'statsbomb'}
#         ],
#     1: [
#         {'season_id': 0, 'name': '2015/2016', 'matchweeks': range(3,38), 'dataset': 'soccermatch'},
#         {'season_id': 1, 'name': '2016/2017', 'matchweeks': range(4,7), 'dataset': 'statsbomb'}
#         ],
#     2: [
#         {'season_id': 0, 'name': '2015/2016', 'matchweeks': range(5,11), 'dataset': 'soccermatch'}
#         ],
#     3: [
#         {'season_id': 0, 'name': '2016/2017', 'matchweeks': range(6,15), 'dataset': 'statsbomb'},
#         {'season_id': 1, 'name': '2017/2018', 'matchweeks': range(1,11), 'dataset': 'soccermatch'}
#         ],
#     4: [
#         {'season_id': 0, 'name': '2018', 'matchweeks': range(1,8), 'dataset': 'statsbomb'}
#         ]
# }

# API get_matches(competition_id, season_id, matchweek, dataset (soccermatch or statsbomb))
# returns a list of all the matches for the given parameters, with the following
# structure. This method internally looks into the corresponding
#  dataset (soccermatch or statsbomb) and fetches the list of the matches
# matches = {
#     0: {
#         0: {
#             0: [
#                 {'match_id': 1545, 'name': 'Arsenal vs Tottenham', 'home_team': 'Arsenal', 'away_team': 'Tottenham'},
#                 {'match_id': 6545, 'name': 'ManU vs ManCity'}
#                 ]
#             },
#         1: {
#             0: [
#                 {'match_id': 484, 'name': 'Liverpool vs Everton'},
#                 {'match_id': 6546, 'name': 'Burnley vs Wolves'}
#                 ]
#             }
#         },
#     1: {
#         0: {
#             0: [
#                 {'match_id': 198, 'name': 'Inter vs Milan'},
#                 {'match_id': 1154, 'name': 'Juventus vs Torino'}
#                 ]
#             },
#         1: {
#             0: [
#                 {'match_id': 1981, 'name': 'Lazio vs Fiorentina'},
#                 {'match_id': 62, 'name': 'Napoli vs Palermo'}
#                 ]
#             }
#         },
#     2: {
#         0: {
#             0: [
#                 {'match_id': 654, 'name': 'Borussia Dortmund vs Bayern Munchen'},
#                 {'match_id': 98, 'name': 'Hannover vs Mainz'}
#                 ]
#             }
#         },
#     3: {
#         0: {
#             0: [
#                 {'match_id': 78, 'name': 'Barcelona vs Real Madrid'},
#                 {'match_id': 14, 'name': 'Real Sociedad vs Athletic Bilbao'}
#                 ]
#             },
#         1: {
#             0: [
#                 {'match_id': 1, 'name': 'Athletic Bilbao vs Real Madrid'},
#                 {'match_id': 2, 'name': 'Real Sociedad vs Barcelona'}
#                 ]
#             }
#         },
#     4: {
#         0: {
#             0:[
#                 {'match_id': 33, 'name': 'Argentina vs France'},
#                 {'match_id': 55, 'name': 'Croatia vs England'}
#                 ]
#             }
#         },
# }

# API predict(match_id, dataset)
# returns a prediction with the following structure
prediction = {
    'outcome': 1,
    'probabilities': [0.56, 0.24, 0.20]
}

# this is not for the API
outcome_mapper = {
    1: 'local wins',
    0: 'teams draw',
    -1: 'away wins'
}

# API get_result(match_id, dataset)
# returns the result of a given match with the following structure
# (to change for the real team names)

result = {
    'result': 'local team 2 - 1 away team'
}

# session_state
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

def unclick_button():
    st.session_state.clicked = False


if 'competitions' not in st.session_state:
    st.session_state.competitions = [defaultdict()]

if 'seasons' not in st.session_state:
    st.session_state.seasons = [defaultdict()]

if 'matches' not in st.session_state:
    st.session_state.matches = [defaultdict()]

base_url = 'http://127.0.0.1:8000/'

@st.cache_data
def get_competitions():
    url = base_url + 'competitions'
    competitions = requests.get(url).json()
    print('get_competitions called', competitions, '\n')
    st.session_state.competitions = competitions
    # return competitions

# @st.cache_data
def get_seasons():
    unclick_button()
    url = base_url + 'seasons'
    params = {'competition_id': competition_selected['competition_id']}
    seasons = requests.get(url, params=params).json()
    print('get_seasons called', seasons, '\n')
    st.session_state.seasons = seasons
    # return seasons

def get_matches():
    unclick_button()
    url = base_url + 'matches'
    params = {'competition_id': competition_selected['competition_id'],
              'season_id': season_selected['season_id'],
              'matchweek': matchweek_selected,
              'dataset': season_selected['dataset']}
    matches = requests.get(url, params=params).json()
    print('get_matches called', matches, '\n')
    st.session_state.matches = matches

# to select

# competitions_url = 'http://127.0.0.1:8000/competitions'

# competitions = get_competitions()
get_competitions()

competition_selected = st.selectbox('Select a competition',
                                    # competitions,
                                    st.session_state.competitions,
                                    # format_func=lambda x: x['name'],
                                    format_func=lambda x: x.get('name'),
                                    on_change=get_seasons)

st.write(f'you selected {competition_selected}')

# seasons = defaultdict(defaultdict)
# seasons = get_seasons()

season_selected = st.selectbox('Select a season',
                            #    seasons,
                               st.session_state.seasons,
                            #    format_func=lambda x: x['season_name'],
                               format_func=lambda x: x.get('name'),
                               on_change=unclick_button)

st.write(f'you selected {season_selected}')

matchweek_selected = st.selectbox('Select a matchweek (round)',
                               season_selected['matchweeks'],
                               format_func=lambda x: f'Round {x}',
                               on_change=get_matches)

st.write(f'you selected {matchweek_selected}')

# matches = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [defaultdict()])))

match_selected = st.selectbox('Select a match',
                            #    matches[competition_selected['competition_id']][season_selected['season_id']][0],
                               st.session_state.matches,
                            #    format_func=lambda x: x['name'],
                               format_func=lambda x: x.get('name'),
                               on_change=unclick_button)

st.write(f'you selected {match_selected}')

# to predict

pred_button = st.button('Make a prediction', on_click=click_button)

if st.session_state.clicked:
    st.markdown(f'''### The model predicts that __{outcome_mapper[prediction["outcome"]]}__ with the following probabilities:''')

    fig = show_probabilities_bar(prediction)

    st.pyplot(fig)

    result_button = st.button('Show results')

    if result_button:

        st.markdown('''#### The actual result of the match was:''')

        st.markdown(f'''#### {result["result"]}''')
