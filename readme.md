Initital plan:

There will be two spiders - one before the change of webpage design, and one after.
Might need more if there are different designs. The key that will connect scores and surfers are:

Surfers: unique name and DOB
Heats: unique time and location

There will be a table for every:

Wave score - columns = surferid, heatid, waveid, wave score
Surfer - columns = surferid, age, height, country, dob etc..
Heat - columns = heatid, conditions, date, event, location etc.

surferid = surfername+dob
heatid = heatdate+event+somethingelse
waveid = heatid+surferid+index





V1 Works!!! I haven't checked it out or anything, but it is running, so just need to make sure the data is as expected and everything now!



Let's make a neural network!
1) specify Architecture
    - Specify how many inputs (features) it will have and how many hidden layers. Keep it simple
    - Could predict world champ or not, or nationality or something. idk, just use a simple neural net to do something fun. could use the count of excellent heats for each surfer?
2) Compile
3) Fit
4) Predictions