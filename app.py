# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=4a30e6ca29a242c8116fa435793f7f0a".format(movie_id)
#
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path
#
# def recommend(movie):
#      movie_index = movies[movies['title'] == movie].index[0]
#      distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
#      recommended_movies_names = []
#      recommended_movies_posters = []
#
#
#
#      for i in distances[1:6]:
#           movie_id = movies.iloc[i[0]].movie_id
#
#           recommended_movies_names.append(movies.iloc[i[0]].title)
#           recommended_movies_posters.append(fetch_poster(movie_id))
#      return recommended_movies_names,recommended_movies_posters
#
#
# movies_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl','rb'))
# st.title('movie recommender system')
#
#
# selected_movie_name = st.selectbox(
#      'tell us what is on your mind and we will recommend you',
#      movies['title'].values)
#
# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#
#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])

import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4a30e6ca29a242c8116fa435793f7f0a"

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return None
    except requests.exceptions.RequestException as e:

        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movies_names = []
    recommended_movies_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_names.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)

    return recommended_movies_names, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Cine Match Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    if recommended_movie_names and recommended_movie_posters:
        for name, poster in zip(recommended_movie_names, recommended_movie_posters):
            st.text(name)
            st.image(poster)
    else:
        st.warning('No recommendations found.')
