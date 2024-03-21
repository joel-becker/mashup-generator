import streamlit as st
# Assuming your existing scripts can be imported like any other Python module
from scrape_lyrics_and_chords import process_urls
#from analyze_chords_with_llm import analyze_song
from calculate_similarity import prepare_data, compute_similarity, find_top_similar_songs

# Load your data - this would ideally be preprocessed and loaded from a file or a database for efficiency
# For the purpose of this example, let's assume 'results_df' is already loaded and processed as you described
import pandas as pd
prepared_df = pd.read_csv('prepared_df.csv')
similarity_df = pd.read_csv('similarity_df.csv', index_col=0)


# Initialize your Streamlit app
st.title('Sing-A-Long Mash-Up Generator')

# Assuming 'results_df' has a column 'song_name' and 'URL' after processing
if 'song_title' not in prepared_df.columns:
    st.write("Dataframe does not contain 'song_title' column.")
else:
    # Create a dropdown menu for song selection
    song_options = prepared_df['song_title'].tolist()
    selected_song = st.selectbox('Choose a song:', options=song_options)

    # Find the URL of the selected song
    selected_song_url = prepared_df[prepared_df['song_title'] == selected_song]['URL'].iloc[0]

    # Assuming 'find_top_similar_songs' function returns a DataFrame or Series with the top 3 similar songs' URLs
    if st.button('Find Similar Songs'):
        #one_hot_df, prepared_df, classes = prepare_data(results_df)
        #similarity_df = compute_similarity(one_hot_df, prepared_df)
        top_3_songs = find_top_similar_songs(prepared_df, similarity_df, selected_song_url)
        
        # Display the top 3 similar songs
        st.write("Top Similar Songs:")
        if len(top_3_songs) > 0:
            for idx in top_3_songs:
                song_title = prepared_df.loc[prepared_df['URL']==idx]['song_title'].item()
                artist = prepared_df.loc[prepared_df['URL']==idx]['artist'].item()
                st.write(f"- {song_title}, {artist} ({idx})")
        else:
            st.write("No similar songs found.")
