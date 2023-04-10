import streamlit as st
import pickle
import pandas as pd
import requests
import joblib

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))
similarity = joblib.load('similarity2.joblib')


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8ffad0fb9e7ad5b7ddcde49be648d794&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommend_movie_posters = []
    for movie in movies_list:
        movie_id = movies.iloc[movie[0]].movie_id
        recommended_movies .append(movies.iloc[movie[0]].title)
        # fetch poster from api
        recommend_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommend_movie_posters


st.title('Movie recommendation system')
selected_movie_name = st.selectbox('Which movie did you like ? ', movies['title'].values)

if st.button('Recommend'):
    movies, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movies[0])
        st.image(posters[0])
    with col2:
        st.text(movies[1])
        st.image(posters[1])
    with col3:
        st.text(movies[2])
        st.image(posters[2])
    with col4:
        st.text(movies[3])
        st.image(posters[3])
    with col5:
        st.text(movies[4])
        st.image(posters[4])



#.\venv\Scripts\activate.ps1