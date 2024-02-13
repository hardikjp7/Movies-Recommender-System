import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ace05b317404492bc2d3cb7abe311664&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/original" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

# Set page configuration
st.set_page_config(page_title="Movie Recommender", layout="centered")

# Display introduction
st.title("Discover Your Next Favorite Movie")
st.write("Explore a world of cinema with personalized recommendations.")

# Load movie data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Create a search bar for movie selection
selected_movie = st.selectbox("Select a movie from the dropdown", movies['title'].values)

# Show recommendations when movie is selected
if st.button("Get Recommendations"):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)

    st.text("Recommended Movies:")
    cols = st.columns(5)  # Adjust number of columns as needed
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
