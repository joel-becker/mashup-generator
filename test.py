import scrape_lyrics_and_chords as slc 
import analyze_chords_with_llm as acl
import calculate_similarity as cs
import os
from dotenv import load_dotenv


# Environment Configuration
load_dotenv(".env")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4"

urls = [
    'https://tabs.ultimate-guitar.com/tab/elvis-presley/cant-help-falling-in-love-chords-1086983',
    'https://tabs.ultimate-guitar.com/tab/jason-mraz/im-yours-chords-373896',
    'https://tabs.ultimate-guitar.com/tab/vance-joy/riptide-chords-1237247',
    'https://tabs.ultimate-guitar.com/tab/justin-bieber/love-yourself-chords-1780199',
    'https://tabs.ultimate-guitar.com/tab/oasis/dont-look-back-in-anger-chords-6097',
    'https://tabs.ultimate-guitar.com/tab/oasis/wonderwall-chords-39144',
    'https://tabs.ultimate-guitar.com/tab/green-day/boulevard-of-broken-dreams-chords-146744',
    'https://tabs.ultimate-guitar.com/tab/john-denver/take-me-home-country-roads-chords-1101747',
    'https://tabs.ultimate-guitar.com/tab/the-beatles/hey-jude-chords-17275',
    'https://tabs.ultimate-guitar.com/tab/lewis-capaldi/someone-you-loved-chords-2512737',
    'https://tabs.ultimate-guitar.com/tab/elton-john/your-song-chords-29113',
    'https://tabs.ultimate-guitar.com/tab/nirvana/smells-like-teen-spirit-chords-807883',
    'https://tabs.ultimate-guitar.com/tab/the-killers/mr-brightside-chords-202646',
    'https://tabs.ultimate-guitar.com/tab/2135261',
    'https://tabs.ultimate-guitar.com/tab/britney-spears/baby-one-more-time-chords-279810',
    'https://tabs.ultimate-guitar.com/tab/misc-musicals/hamilton-alexander-hamilton-chords-1781125',
    'https://tabs.ultimate-guitar.com/tab/wheatus/teenage-dirtbag-chords-927822',
    'https://tabs.ultimate-guitar.com/tab/misc-cartoons/aladdin-a-whole-new-world-chords-171361',
    'https://tabs.ultimate-guitar.com/tab/taylor-swift/love-story-chords-730809',
    'https://tabs.ultimate-guitar.com/tab/train/hey-soul-sister-chords-884388',
    'https://tabs.ultimate-guitar.com/tab/the-beatles/let-it-be-chords-17427',
    'https://tabs.ultimate-guitar.com/tab/fugees/killing-me-softly-chords-50470',
    'https://tabs.ultimate-guitar.com/tab/hozier/take-me-to-church-chords-1424967',
    'https://tabs.ultimate-guitar.com/tab/train/drops-of-jupiter-chords-1433',
    'https://tabs.ultimate-guitar.com/tab/ben-e-king/stand-by-me-chords-1724608',
    'https://tabs.ultimate-guitar.com/tab/sean-kingston/beautiful-girls-chords-604139',
    'https://tabs.ultimate-guitar.com/tab/men-without-hats/the-safety-dance-chords-785904',
    'https://tabs.ultimate-guitar.com/tab/scissor-sisters/take-your-mama-chords-147493',
    'https://tabs.ultimate-guitar.com/tab/guns-n-roses/sweet-child-o-mine-chords-176076',
    'https://tabs.ultimate-guitar.com/tab/green-day/good-riddance-time-of-your-life-chords-12835',
    'https://tabs.ultimate-guitar.com/tab/adele/make-you-feel-my-love-chords-752102',
    'https://tabs.ultimate-guitar.com/tab/the-fray/how-to-save-a-life-chords-258804',
    'https://tabs.ultimate-guitar.com/tab/759809',
    'https://tabs.ultimate-guitar.com/tab/the-animals/house-of-the-rising-sun-chords-18688',
    'https://tabs.ultimate-guitar.com/tab/death-cab-for-cutie/i-will-follow-you-into-the-dark-chords-335735',
    'https://tabs.ultimate-guitar.com/tab/eagle-eye-cherry/save-tonight-chords-14172',
    'https://tabs.ultimate-guitar.com/tab/goo-goo-dolls/iris-chords-54512',
    'https://tabs.ultimate-guitar.com/tab/a-ha/take-on-me-chords-1842621',
    'https://tabs.ultimate-guitar.com/tab/misc-soundtrack/grease-hopelessly-devoted-to-you-chords-78008',
    'https://tabs.ultimate-guitar.com/tab/the-foundations/build-me-up-buttercup-chords-815490',
    'https://tabs.ultimate-guitar.com/tab/abba/mamma-mia-chords-709013',
    'https://tabs.ultimate-guitar.com/tab/the-bangles/eternal-flame-chords-1196444',
    'https://tabs.ultimate-guitar.com/tab/kings-of-leon/sex-on-fire-chords-723359',
    'https://tabs.ultimate-guitar.com/tab/gloria-gaynor/i-will-survive-chords-154172',
    'https://tabs.ultimate-guitar.com/tab/fall-out-boy/sugar-were-going-down-chords-267936',
    'https://tabs.ultimate-guitar.com/tab/misc-cartoons/the-lion-king-i-just-cant-wait-to-be-king-chords-810607',
    'https://tabs.ultimate-guitar.com/tab/plain-white-ts/hey-there-delilah-chords-337676',
    'https://tabs.ultimate-guitar.com/tab/gary-jules/mad-world-chords-97039',
    'https://tabs.ultimate-guitar.com/tab/amy-winehouse/back-to-black-chords-467281',
    'https://tabs.ultimate-guitar.com/tab/mariah-carey/all-i-want-for-christmas-is-you-chords-903566',
    'https://tabs.ultimate-guitar.com/tab/radiohead/creep-chords-4169',
    'https://tabs.ultimate-guitar.com/tab/backstreet-boys/i-want-it-that-way-chords-827123',
    'https://tabs.ultimate-guitar.com/tab/the-cure/friday-im-in-love-chords-101457',
    'https://tabs.ultimate-guitar.com/tab/misc-cartoons/toy-story-youve-got-a-friend-in-me-chords-107274',
    'https://tabs.ultimate-guitar.com/tab/bobby-helms/jingle-bell-rock-chords-1443245',
    'https://tabs.ultimate-guitar.com/tab/audrey-hepburn/moon-river-chords-1788365',
    #'https://tabs.ultimate-guitar.com/tab/misc-cartoons/the-little-mermaid-part-of-your-world-chords-978268',
    'https://tabs.ultimate-guitar.com/tab/survivor/eye-of-the-tiger-chords-1483686',
    #'https://tabs.ultimate-guitar.com/tab/misc-cartoons/the-lion-king-hakuna-matata-chords-153275',
    'https://tabs.ultimate-guitar.com/tab/misc-cartoons/the-lion-king-circle-of-life-chords-211642',
    'https://tabs.ultimate-guitar.com/tab/misc-soundtrack/high-school-musical-breaking-free-chords-334142',
    'https://tabs.ultimate-guitar.com/tab/misc-cartoons/pokemon-theme-chords-938502',
    'https://tabs.ultimate-guitar.com/tab/misc-soundtrack/grease-youre-the-one-that-i-want-chords-78010'
]

results_df = slc.process_urls(urls)
print(results_df)
results_df = results_df.loc[results_df['lyrics_and_chords'].ne('')]
results_df.to_csv('results_df_processed.csv', index=False)

analyzer=acl.SongAnalyzer(API_KEY, MODEL_NAME)
results_df = results_df.apply(analyzer.analyze_song, axis=1)
print(results_df)

results_df.to_csv('results_df.csv', index=False)
df = results_df
one_hot_df, prepared_df, classes = cs.prepare_data(df)
similarity_df = cs.compute_similarity(one_hot_df, prepared_df)

prepared_df.to_csv('prepared_df.csv', index=False)
similarity_df.to_csv('similarity_df.csv')




