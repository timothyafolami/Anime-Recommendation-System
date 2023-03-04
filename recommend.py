import streamlit as st
# import joblib
import pandas as pd
# pip install tensorflow
# from tensorflow import keras
from anime_rec import New_User

# load your saved model
# model = keras.models.load_model('New_model1')

# create a function to make recommendations
def recommend_anime(genres, anime_type):

    # make recommendations using your model
    recommendations_df = New_User(genres, anime_type)
    output_df = recommendations_df[['name', 'genre', 'type', 'episodes', 'anime_rating', 'members']].reset_index(drop=True)
    return output_df[:25]



# create a function to preprocess the selected genres
def preprocess_genres(genres):
    # perform any preprocessing needed, such as converting the list to a string
    return ','.join(genres)

# create your Streamlit app
def main():
    # set page title and favicon
    st.set_page_config(page_title='Anime Recommendation System', page_icon='📺')


    # add a header and subtitle
    st.markdown(
        """
        <style>
            @keyframes sparkles {
                0% {background-position:0 0}
                100% {background-position:-1000px 1000px}
            }
            h1 {
                background: linear-gradient(45deg, #EE82EE, #87CEEB, #00BFFF, #FFD700, #EE82EE);
                background-size: 400% 400%;
                -webkit-animation: sparkles 5s ease infinite;
                -moz-animation: sparkles 5s ease infinite;
                animation: sparkles 5s ease infinite;
                color: transparent;
                -webkit-background-clip: text;
                background-clip: text;
            }
            h3 {
                color: #555555;
            }
        </style>
        """
        , unsafe_allow_html=True
    )

    st.title('Anime Recommendation System')
    st.subheader('Discover your next favorite anime!')

    # add a multiselect for genre selection
    genres = st.multiselect(
        'Select your favorite genres',
        ['Drama', 'Romance', 'School', 'Supernatural', 'Action', 'Adventure', 'Fantasy', 'Magic', 'Military', 'Shounen', 'Comedy', 'Historical', 'Parody', 'Samurai', 'Sci-Fi', 'Thriller', 'Sports', 'SuperPower', 'Space', 'SliceofLife', 'Mecha', 'Music', 'Mystery', 'Seinen', 'MartialArts', 'Vampire', 'Shoujo', 'Horror', 'Police', 'Psychological', 'Demons', 'Ecchi', 'Josei', 'ShounenAi', 'Game', 'Dementia', 'Harem', 'Cars', 'Kids', 'ShoujoAi', 'Hentai', 'Yaoi', 'Yuri']
    )

    anime_type = st.selectbox(
        'Select the type of anime you want to watch',
        ['TV', 'Movie', 'OVA', 'ONA', 'Special']
    )

    # add a button to trigger recommendations
    if st.button('Recommend'):
        # show a loading spinner while the model is generating recommendations
        with st.spinner('Generating recommendations...'):
            recommendations_df = recommend_anime(genres, anime_type)
        # display the recommendations as a table
        st.subheader('Recommended anime')
        st.dataframe(recommendations_df)

if __name__ == '__main__':
    main()
