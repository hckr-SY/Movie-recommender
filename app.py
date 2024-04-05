import streamlit as st
import pandas as pd
import pickle
import requests


# def poster_id

movies_dict = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


def get_path(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1M2UzZWVhYTY0ZDQyNjllN2RiZDEyYTFhMzkzZTU0MSIsInN1YiI6IjY2MDU0ZGM1YWFmZWJkMDE4NzE3ZWQ1NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.arQTzUiKzkLg4VLgzSGN3--siX4lxtvrq2vy9AUwVQU"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return "https://image.tmdb.org/t/p/w500"+data['poster_path']
def movieRecommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    names=[]
    images=[]

    for ele in movies_list:
        names.append(movies.iloc[ele[0]].title)
        images.append(get_path(movies.iloc[ele[0]].movie_id))
        # images.append()
    return names,images







st.title("Movie Recommender System")


selected_movie_name = st.selectbox(
    'Select Movie',
    (movies['title'].values))

# st.write('You selected:', option)


if st.button("Recommend"):
    rec_movies,images=movieRecommend(selected_movie_name)
    # print(len(rec_movies))
    # print(images)

    movies_len = int(len(rec_movies))
    images_per_row = 4
    num_rows = (movies_len//images_per_row ) + 1

    i = 0
    # container=None
    # cols = None
    while i<movies_len:
        container = st.container()
        with container:
            cols = st.columns(images_per_row)

            while i<movies_len:
                cols[i%images_per_row].image(images[i],caption=rec_movies[i])

                i+=1
                if i%images_per_row==0:
                    break;









