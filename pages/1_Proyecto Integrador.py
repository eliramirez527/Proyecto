import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.sidebar.title("Nuevas Tecnologias")

logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Explorador de Base de Datos de Canciones")

df = pd.read_csv('static/datasets/songs_data (1).csv')

artists = sorted(df['Nombre del artista'].unique())
genres = sorted(df['Género/s musical/es'].unique())
years = sorted(df['Fecha de lanzamiento'].apply(lambda x: x.split('-')[0]).unique())

def filter_by_genre(df, genres):
    return df[df['Género/s musical/es'].isin(genres)]

def filter_by_artist(df, artist):
    return df[df['Nombre del artista'] == artist]

def filter_by_album(df, album):
    return df[df['Álbum'] == album]

def filter_by_song(df, song):
    return df[df['Título de la canción'] == song]

def filter_by_album(df, album_title):
    return df[df['Título del álbum'] == album_title]

def filter_by_release_year(df, start_year, end_year):
    df['Fecha de lanzamiento'] = pd.to_datetime(df['Fecha de lanzamiento'])
    return df[(df['Fecha de lanzamiento'].dt.year >= start_year) & (df['Fecha de lanzamiento'].dt.year <= end_year)]

def filter_by_reproductions(df, min_reproductions, max_reproductions):
    return df[(df['Número de reproducciones'] >= min_reproductions) & (df['Número de reproducciones'] <= max_reproductions)]

def filter_by_top5(df):
    return df[df['Top 5'] == True]

# Configurar la paleta de colores de Seaborn
sns.set_palette("Set2")

# Filtro por género musical
def filtro1():
    selected_genres = st.multiselect("Género Musical", genres)
    if selected_genres:
        filtered_df = filter_by_genre(df, selected_genres)
        st.dataframe(filtered_df)
        st.subheader("Gráfico de Canciones por Género")
        
        plt.figure(figsize=(10, 5))
        sns.countplot(data=filtered_df, y='Género/s musical/es', order=filtered_df['Género/s musical/es'].value_counts().index)
        plt.xlabel('Número de Canciones')
        plt.ylabel('Género Musical')
        st.pyplot(plt.gcf())

# Filtro por artista
def filtro2():
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_artist = st.selectbox("Artista", sorted(df['Nombre del artista'].unique()))
    if selected_artist:
        filtered_df_artist = filter_by_artist(df, selected_artist)
        albums = sorted(filtered_df_artist['Título del álbum'].unique())
        with col2:
            selected_album = st.selectbox("Álbum", albums)
        if selected_album:
            filtered_df_album = filter_by_album(filtered_df_artist, selected_album)
            songs = sorted(filtered_df_album['Título de la canción'].unique())
            with col3:
                selected_song = st.selectbox("Canción", songs)
            if selected_song:
                filtered_df_song = filter_by_song(filtered_df_album, selected_song)
                st.dataframe(filtered_df_song)
                st.subheader(f"Gráfico de Reproducciones del Artista: {selected_artist} - Álbum: {selected_album} - Canción: {selected_song}")
                
                plt.figure(figsize=(10, 5))
                sns.barplot(data=filtered_df_song, x='Título de la canción', y='Número de reproducciones', palette="Set2")
                plt.xlabel('Canción')
                plt.ylabel('Número de Reproducciones')
                st.pyplot(plt.gcf())

                st.subheader("Promedio de Reproducciones")
                promedio_reproducciones = filtered_df_song['Número de reproducciones'].mean()
                st.subheader(round(promedio_reproducciones, 1))

# Filtro por año de lanzamiento
def filtro3():
    start_year, end_year = st.slider("Año de Lanzamiento", min_value=int(years[0]), max_value=int(years[-1]), value=(int(years[0]), int(years[-1])))
    filtered_df = filter_by_release_year(df, start_year, end_year)
    st.dataframe(filtered_df)
    st.subheader("Gráfico de Canciones por Año de Lanzamiento")
    
    plt.figure(figsize=(10, 5))
    sns.countplot(data=filtered_df, x=filtered_df['Fecha de lanzamiento'].dt.year, order=sorted(filtered_df['Fecha de lanzamiento'].dt.year.unique()), palette="Set2")
    plt.xlabel('Año de Lanzamiento')
    plt.ylabel('Número de Canciones')
    st.pyplot(plt.gcf())

# Filtro por número de reproducciones
def filtro4():
    min_reproductions, max_reproductions = st.slider("Número de Reproducciones", min_value=int(df['Número de reproducciones'].min()), max_value=int(df['Número de reproducciones'].max()), value=(int(df['Número de reproducciones'].min()), int(df['Número de reproducciones'].max())))
    filtered_df = filter_by_reproductions(df, min_reproductions, max_reproductions)
    st.dataframe(filtered_df)
    st.subheader("Gráfico de Reproducciones")
    
    plt.figure(figsize=(10, 5))
    sns.barplot(data=filtered_df, x='Título de la canción', y='Número de reproducciones', palette="Set2")
    plt.xlabel('Canción')
    plt.ylabel('Número de Reproducciones')
    st.pyplot(plt.gcf())

# Filtro por Top 5
def filtro5():
    filtered_df = filter_by_top5(df)
    st.dataframe(filtered_df)
    st.subheader("Gráfico de Top 5 Canciones")
    
    plt.figure(figsize=(10, 5))
    sns.barplot(data=filtered_df, x='Título de la canción', y='Número de reproducciones', palette="Set2")
    plt.xlabel('Canción')
    plt.ylabel('Número de Reproducciones')
    st.pyplot(plt.gcf())

# Menú de selección de filtro
filtros = [
    "Filtrar por Género Musical",
    "Filtrar por Artista",
    "Filtrar por Año de Lanzamiento",
    "Filtrar por Número de Reproducciones",
    "Filtrar por Top 5"
]

filtro = st.selectbox("Selecciona un Filtro", filtros)

if filtro:
    if filtro == filtros[0]:
        filtro1()
    elif filtro == filtros[1]:
        filtro2()
    elif filtro == filtros[2]:
        filtro3()
    elif filtro == filtros[3]:
        filtro4()
    elif filtro == filtros[4]:
        filtro5()
