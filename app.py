import streamlit as st
import requests
from utils.plots import show_probabilities_bar

st.set_page_config(
    page_title="GoalGuru",
    page_icon="⚽",
    menu_items={
        'Report a bug': "https://github.com/jotanavarrete/goalguru_gui/issues",
        'About': '''**Developers:**
* [jotanavarrete](https://github.com/jotanavarrete)
* [juancruzgui](https://github.com/juancruzgui)
* [sahb7](https://github.com/sahb7)'''
    }
)

''''''
st.title("Welcome to GoalGuru ⚽!")

st.header("Fun football forecasting 🔮. By fans, for fans.", divider='violet')
''''''

base_url = st.secrets['api_url']


@st.cache_data
def get_competitions():
    url = base_url + 'competitions'
    competitions = requests.get(url).json()
    # print('\nget_competitions called', competitions, '\n')
    # st.session_state.competitions = competitions
    return competitions

# @st.cache_data
def get_seasons():
    url = base_url + 'seasons'
    competition_id = st.session_state.competition_selected['competition_id']
    params = {'competition_id': competition_id}
    seasons = requests.get(url, params=params).json()
    # print('\nget_seasons called', seasons, '\n')
    st.session_state.seasons = seasons
    st.session_state.season_selected = st.session_state.seasons[0]
    mid_index = len(st.session_state.season_selected['matchweeks'])//2
    st.session_state.matchweek_selected = st.session_state.season_selected['matchweeks'][mid_index]
    get_matches(from_seasons=True)
    # return seasons

def get_matches(from_seasons=True):
    url = base_url + 'matches'
    if from_seasons:
        mid_index = len(st.session_state.season_selected['matchweeks'])//2
        st.session_state.matchweek_selected = st.session_state.season_selected['matchweeks'][mid_index]
    params = {'competition_id': st.session_state.competition_selected['competition_id'],
              'season_id': st.session_state.season_selected['season_id'],
              'matchweek': st.session_state.matchweek_selected,
              'dataset': st.session_state.season_selected['dataset']}
    matches = requests.get(url, params=params).json()
    # print('\nget_matches called', matches, '\n')
    st.session_state.matches = matches
    st.session_state.match_selected = st.session_state.matches[0]
    predict()

def predict():
    url = base_url + 'predict'
    params = {'match_id': st.session_state.match_selected['match_id'],
              'dataset': st.session_state.season_selected['dataset']}
    prediction = requests.get(url, params=params).json()
    # print('\npredict called', matches, '\n')
    st.session_state.prediction = prediction
    outcome_mapper = {
    1: f'{st.session_state.match_selected["home_team"]} wins',
    0: 'teams draw',
    -1: f'{st.session_state.match_selected["away_team"]} wins'
    }
    st.session_state.fig = show_probabilities_bar(st.session_state.prediction, outcome_mapper.values())


if 'competitions' not in st.session_state:
    st.session_state.competitions = get_competitions()
# st.write(st.session_state.competitions)

if 'competition_selected' not in st.session_state:
    st.session_state.competition_selected = st.session_state.competitions[0]
# st.write(st.session_state.competition_selected)

if 'seasons' not in st.session_state:
    get_seasons()
# st.write(st.session_state.seasons)

if 'season_selected' not in st.session_state:
    st.session_state.season_selected = st.session_state.seasons[0]
# st.write(st.session_state.season_selected)

if 'matchweek_selected' not in st.session_state:
    st.session_state.matchweek_selected = min(st.session_state.season_selected['matchweeks'])
# st.write(st.session_state.matchweek_selected)

if 'matches' not in st.session_state:
    get_matches()
# st.write(st.session_state.matches)

if 'match_selected' not in st.session_state:
    st.session_state.match_selected = st.session_state.matches[0]
# st.write(st.session_state.match_selected)

if 'prediction' not in st.session_state:
    predict()
# st.write(st.session_state.prediction)

if 'fig' not in st.session_state:
    outcome_mapper = {
    1: f'{st.session_state.match_selected["home_team"]} wins',
    0: 'teams draw',
    -1: f'{st.session_state.match_selected["away_team"]} wins'
    }
    st.session_state.fig = show_probabilities_bar(st.session_state.prediction, outcome_mapper.values())



# to select
# print('\n page_reloaded\n')

competition_selected = st.selectbox('Select a competition',
                                    st.session_state.competitions,
                                    format_func=lambda x: x.get('name'),
                                    on_change=get_seasons,
                                    key='competition_selected')

# st.write(f'you selected {st.session_state.competition_selected}')

season_selected = st.selectbox('Select a season',
                               st.session_state.seasons,
                               format_func=lambda x: x.get('name'),
                               on_change=get_matches,
                               kwargs=dict(from_seasons=True),
                               key='season_selected')

# st.write(f'you selected {st.session_state.season_selected}')

matchweek_selected = st.selectbox('Select a matchweek (round)',
                               season_selected.get('matchweeks'),
                               format_func=lambda x: f'Round {x}' if x != 0 else 'Knockout Phase',
                               on_change=get_matches,
                               kwargs=dict(from_seasons=False),
                               key='matchweek_selected')

# st.write(f'you selected {st.session_state.matchweek_selected}')

match_selected = st.selectbox('Select a match',
                               st.session_state.matches,
                               format_func=lambda x: x.get('name'),
                               on_change=predict,
                               key='match_selected')

# st.write(f'you selected {st.session_state.match_selected}')


# show_prediction()
outcome_mapper = {
    1: f'{st.session_state.match_selected["home_team"]} wins',
    0: 'teams draw',
    -1: f'{st.session_state.match_selected["away_team"]} wins'
    }

st.markdown(f'''### The model predicts that __{outcome_mapper[st.session_state.prediction["outcome"]]}__ with the following probabilities:''')

st.pyplot(st.session_state.fig)

if st.session_state.matchweek_selected == 1:
    st.info("The predictions for the first matchweek gives always the same probabilities, because the model doesn't know past information.", icon="ℹ️")

result_button = st.button('Show actual results')

if result_button:

    st.markdown('''#### The actual result of the match was:''')

    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.match_selected['result']}</h2>", unsafe_allow_html=True)
