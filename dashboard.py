import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from streamlit_option_menu import option_menu

# Set page config
st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('watch_movies.csv')
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.title("🎬 Movie Analytics")
    selected = option_menu(
        menu_title="Navigation",
        options=["Overview", "3D Analysis", "Genre Analysis", "Actor Analysis", "Recommendations"],
        icons=["house", "graph-up-3d", "film", "person", "star"],
        menu_icon="cast",
        default_index=0,
    )

# Main content
if selected == "Overview":
    st.title("Movie Analytics Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Movies", len(df))
    with col2:
        st.metric("Average Budget", f"${df['budget_usd'].mean():,.0f}")
    with col3:
        st.metric("Average User Score", f"{df['user_score'].mean():.1f}")
    with col4:
        st.metric("Total Genres", df['genres'].nunique())

    # Budget distribution with animation
    st.subheader("Budget Distribution Over Time")
    fig = px.histogram(
        df,
        x="budget_usd",
        animation_frame=pd.to_datetime(df['release_date']).dt.year,
        nbins=50,
        color_discrete_sequence=['#636EFA']
    )
    fig.update_layout(
        xaxis_title="Budget (USD)",
        yaxis_title="Number of Movies",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected == "3D Analysis":
    st.title("3D Movie Analysis")
    
    # 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=df['budget_usd'],
        y=df['vote_count'],
        z=df['user_score'],
        mode='markers',
        marker=dict(
            size=5,
            color=df['user_score'],
            colorscale='Viridis',
            opacity=0.8
        ),
        text=df['title']
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis_title="Budget (USD)",
            yaxis_title="Vote Count",
            zaxis_title="User Score"
        ),
        title="Budget vs Vote Count vs User Score"
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Genre Analysis":
    st.title("Genre Analysis")
    
    # Genre distribution
    genre_counts = df['genres'].value_counts().head(10)
    fig = px.bar(
        x=genre_counts.values,
        y=genre_counts.index,
        orientation='h',
        title="Top 10 Genres",
        labels={'x': 'Number of Movies', 'y': 'Genre'},
        color=genre_counts.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Genre budget analysis
    st.subheader("Average Budget by Genre")
    genre_budget = df.groupby('genres')['budget_usd'].mean().sort_values(ascending=False).head(10)
    fig = px.bar(
        x=genre_budget.values,
        y=genre_budget.index,
        orientation='h',
        title="Average Budget by Genre",
        labels={'x': 'Average Budget (USD)', 'y': 'Genre'},
        color=genre_budget.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Actor Analysis":
    st.title("Actor Analysis")
    
    # Top actors
    actor_counts = df['top_billed'].value_counts().head(10)
    fig = px.bar(
        x=actor_counts.values,
        y=actor_counts.index,
        orientation='h',
        title="Top 10 Actors by Movie Count",
        labels={'x': 'Number of Movies', 'y': 'Actor'},
        color=actor_counts.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Recommendations":
    st.title("Movie Recommendations")
    
    # Genre selection
    selected_genre = st.selectbox("Select a genre", df['genres'].unique())
    
    # Filter movies by genre
    genre_movies = df[df['genres'] == selected_genre]
    
    # Sort by user score
    top_movies = genre_movies.sort_values('user_score', ascending=False).head(5)
    
    # Display recommendations
    for _, movie in top_movies.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(movie['poster_path'], width=150)
            with col2:
                st.subheader(movie['title'])
                st.write(f"User Score: {movie['user_score']:.1f}")
                st.write(f"Release Date: {movie['release_date']}")
                st.write(f"Director: {movie['director']}")
                st.write(f"Top Billed: {movie['top_billed']}")
            st.markdown("---") 