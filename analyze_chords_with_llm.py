
import pandas as pd
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Dict

# Output schema definition using Pydantic
class SongData(BaseModel):
    song_title: str = Field(description="The title of the song.")
    artist: str = Field(description="The artist of the song.")
    popularity_score: int = Field(description="The popularity score of the song, out of 100.")
    time_signature: str = Field(description="The time signature of the song.")
    verse_chords: List[str] = Field(description="The chord progression for the verse.")
    tonic_chord: str = Field(description="The tonic chord of the song.")
    verse_chords_rebased: List[str] = Field(description="Transposed chord progression, transposed to begin in C major or A minor.")

class SongAnalyzer:
    def __init__(self, api_key: str, model_name: str):
        self.chat_model = ChatOpenAI(model=model_name, openai_api_key=api_key, max_tokens=1000)
        self.parser = PydanticOutputParser(pydantic_object=SongData)

    def generate_prompt(self, lyrics_and_chords: str) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(
                    """
                    Answer the user's query about the song.

                    ---

                    \n LYRICS AND CHORDS: 
                    \n {lyrics_and_chords}

                    ---
                    
                    \n INSTRUCTIONS: 
                    \n {format_instructions}
                    \n Just guess the song name and artist as best you can, and the popularity score as an integer out of 100. Similarly, give your best-guess time signature based on general knowledge of the song.
                    \n Please format verse chords in the most basic form possible. That is, try to only use the major or minor triad for each chord.
                    \n For rebased chords, please transpose the chord progression to C major if the tonic chord is a major chord, and A minor if the tonic chord is a minor chord. So, for example, Em G D A should be transposed to Am C G D, and so on.
                    \n So Gsus2 should be G, G/B should be G, Gadd9 should be G, Gm6 should be Gm, and so on. E7 should be E, C/B should be C, D7sus4 should be D, D flat minor should be C3m. Even an E followed by an E7 should be listed as just E, or G followed by G7 should be listed as just G, etc.
                    \n Format all chords as a python list of strings, e.g. ["C", "G", "Am", "F"]. I don't want "C G Am F" or "C | G | Am | F" and so on, but a list of strings. Try if possible to stick to 3 or 4 chords only; it's fine if the song has some deviation from this in reality. To accomplish fitting in this constraint, you might limit yourself to merely the first 1 or 2 chord sequences in the verse.
                    \n Once again, remember that I want all chords expressed as their constituent major or minor triads.
                    """
                )
            ],
            input_variables=[lyrics_and_chords],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
            },
        )
        return prompt
    
    def get_output(self, row: pd.Series):
        _input = self.generate_prompt(row['lyrics_and_chords']).format_prompt(lyrics_and_chords=row['lyrics_and_chords'])
        output = self.chat_model(_input.to_messages())
        return output
    
    def parse_output(self, output):
        return self.parser.parse(output.content)

    def analyze_song(self, row: pd.Series) -> pd.Series:
        output = self.get_output(row)
        parsed = self.parse_output(output)
        row['song_title'] = parsed.song_title
        row['artist'] = parsed.artist
        row['popularity_score'] = parsed.popularity_score
        row['verse_chords'] = parsed.verse_chords
        row['tonic_chord'] = parsed.tonic_chord
        row['verse_chords_rebased'] = parsed.verse_chords_rebased
        return row
