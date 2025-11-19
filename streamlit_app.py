import pickle
import streamlit as st
import pandas as pd
import dill
import requests

with open("dataframe.pkl", "rb") as f1:
    df = pickle.load(f1)

with open("recommend.pkl", "rb") as f2:
    recommend_system = dill.load(f2)

with open("similarity.pkl", "rb") as f3:
    similarity_score = pickle.load(f3)


import streamlit as st

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, rgba(18, 18, 18, 0.9), rgba(24, 24, 24, 0.9)), 
                    url("https://i.pinimg.com/1200x/51/3b/78/513b78c1771ef5afaf91224cb07a260a.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #f5c518; /* IMDb Yellow */
    }
    
    .stTextInput>div>div>input {
        background-color: #222; /* Darker input field */
        color: white;
    }
    
    .stButton>button {
        background-color: #f5c518; /* IMDb button color */
        color: black;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("MovieMate 🎬")
st.write("Makes your movie Search Easier.")
name = st.selectbox("Search for a movie...", df["title"]) 
search = st.button("Search")

if name and search:
    result = recommend_system(name, df, similarity_score, top_n = 5 )
    if not result.empty:
        st.write("Here are the movies recommended for you.")
        url = []
        imdb_id = result["imdb_id"].to_numpy()
        for i in range(5):
            api = f"http://www.omdbapi.com/?i={imdb_id[i]}&apikey=7419a52f"
            response = requests.get(api)
            if response.status_code == 200 :
                data = response.json()
                url.append(data["Poster"])
            else:
                url.append("https://picsum.photos/200/300")
        
        cols = st.columns(len(url))
        for col, img_url, text in zip(cols, url, result["title"]):
            with col:
                st.image(img_url, caption = text, use_container_width = True) 
    else:
        st.write("Movie not found")

    
    



