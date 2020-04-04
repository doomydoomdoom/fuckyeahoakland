fuckyeahoakland
===============
Single-serving website/opportunity to play w/more APIs.

This project is just shy of a logical end-point for active development. The ROI/CBA on remaining bugs/features is extremely low, as this is a somewhat hyper-local project ( unlike ITAST, which has a lot of options for feature expansion that don't need basic location data but DON'T need to account for micro-climates and cultural attitudes about microclimates.

The critical remaining "bug" is basically "Is my data slightly off, or are Oakland and SF more similar in temperature than when I started this project", and so far it looks like the latter.

This app generates 288 requests a day + manual testing; since they just got acquired by Apple that is now a rounding error.
I could technically rewrite it to function with 2 requests a day and could EASILY get it under 50, but they're not gonna lower the quota, they're just gonna shut down the API on ~1/1/21 anyway.

TBD:
- Monitoring
- AWS Migration
- Containerization

BACKLOG
- Check historical data/sanity check

DONE:
- Refactor data sanity check into from display to cron w/screaming
- test known error-cases in prod
- separate json generation and consumption
- limit errors to STDOUT to cron
- add poweredby logo
- replicate Cheat Mode ( cherry-picking micro-climates )
- mitigate edge case for partial API failure

"Q5"
- FIX edge case for a partial API failure
- Split fuckyeahoakland.py into fuckyou.py, fuckme.py, and fuckthis.json
- Refactor data sanity check into from display to cron w/screaming 
- De-pluralization ( "1 degrees warmer" ) 
- Swap the Darksky API with OpenWeatherMap if it still exists in 2021

