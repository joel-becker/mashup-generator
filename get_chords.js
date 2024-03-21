const ugs = require('ultimate-guitar-scraper');

// Example: Get chords for a popular song
const SONG_NAME = "Wish You Were Here";
const ARTIST_NAME = "Pink Floyd";

ugs.search({
    bandName: ARTIST_NAME,
    songName: SONG_NAME,
    type: ['chords'] // Focus on getting chords
}, function(error, tabs) {
    if (error) {
        console.log(error);
    } else {
        // Assuming chords are in the first result:  
        const firstTabUrl = tabs[0].url; 

        ugs.get(firstTabUrl, function(error, tab) {
            if (error) {
                console.log(error);
            } else {
                console.log("Song Title: ", tab.name);
                console.log("Chord Progression:\n", tab.contentText); 
            }
        });
    }
});
