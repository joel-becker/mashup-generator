import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.spatial.distance import jaccard
import numpy as np

def safe_eval(chord_progression):
    """
    Safely evaluate the chord progression string into a list.
    """
    try:
        return eval(chord_progression)
    except:
        return None

    
def prepare_data(df, chord_col='verse_chords_rebased', position_only=True):
    # Specify chord movements
    # Quantify similarity between chords

    # One-hot encode the chord progressions
    mlb = MultiLabelBinarizer()
    one_hot_encoded = mlb.fit_transform(df[chord_col])

    # Create DataFrame for one-hot encoded features
    if position_only:
        one_hot_df = pd.DataFrame()
    else:
        one_hot_df = pd.DataFrame(one_hot_encoded, columns=mlb.classes_)

    # Initialize the chord position columns in one_hot_df to 0
    max_length = 4
    for i in range(1, max_length + 1):
        for chord in mlb.classes_:
            one_hot_df[f'chord{i}_{chord}'] = 0

    # Iterate over the DataFrame to set chord position features
    for i, chords in enumerate(df[chord_col]):
        for pos, chord in enumerate(chords):
            if pos < max_length:
                one_hot_df.at[i, f'chord{pos+1}_{chord}'] = 1
    
    ## Add a column for the number of chords in the main chord progression
    #df['chord_count'] = df[chord_col].apply(len)
    ## One-hot encode the 'chord_count' feature
    #chord_count_mlb = MultiLabelBinarizer()
    #chord_counts_one_hot = chord_count_mlb.fit_transform(df[['chord_count']])
    #chord_counts_df = pd.DataFrame(chord_counts_one_hot, columns=[f'chord_count_{x}' for x in chord_count_mlb.classes_])
    #
    ## Combine the one-hot encoded chord progression with the chord counts
    #one_hot_df = pd.concat([one_hot_df, chord_counts_df], axis=1)

    # Reset index for smooth concatenation
    one_hot_df.reset_index(drop=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Replace NaNs with 0s in one_hot_df
    one_hot_df.fillna(0, inplace=True)

    # Concatenate original df with one_hot_df for complete dataset
    complete_df = pd.concat([df, one_hot_df], axis=1)

    return one_hot_df, complete_df, mlb.classes_

def compute_similarity(one_hot_df, df):
    """
    Computes the cosine similarity matrix for the given DataFrame.
    """
    #encoded_cols = df.columns.difference(['URL', 'Lyrics/Chords', 'Tonic Chord', 'Verse Chord Progression Rebased'])
    #similarity_matrix = cosine_similarity(df[encoded_cols])
    similarity_matrix = cosine_similarity(one_hot_df)
    return pd.DataFrame(similarity_matrix, index=df['URL'], columns=df['URL'])

def find_top_similar_songs(df, similarity_df, song_url, top_n=3, min_similarity=0.8):
    """
    Finds the top N similar songs to a given song URL, with an optional minimum similarity score cut-off.
    
    Parameters:
    - df: DataFrame containing the song data.
    - similarity_df: DataFrame containing the similarity scores between songs.
    - song_url: URL of the song to find similarities for.
    - top_n: Number of top similar songs to return.
    - min_similarity: Minimum similarity score for a song to be considered similar.
    
    Returns:
    - top_n_songs: URLs of the top N similar songs that meet the minimum similarity score.
    """
    song_index = df.index[df['URL'] == song_url].to_list()[0]
    similarities = similarity_df.iloc[song_index].sort_values(ascending=False)
    if min_similarity is not None:
        # Filter out songs that don't meet the minimum similarity score
        similarities = similarities[similarities >= min_similarity]
    top_n_indices = similarities.iloc[1:top_n+1].index  # Exclude the first one
    top_n_songs = df.loc[df['URL'].isin(top_n_indices), 'URL']
    return top_n_songs

