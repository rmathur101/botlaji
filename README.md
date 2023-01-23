# botlaji

This is a `python` project, `python3` was used so if you're using `python2` YMMV. 

Steps to get up and running:
1. `pip install -r requirements.txt'
2. See the `.env.example` file. Create a copy and call it `.env`. Get an API key from OpenAI. Put your API key in the prescribed spot in the file. Note, that requests to the API cost money. So keep an eye on the spend on your account.
3. Run the program like this: 

`python run.py [Put your query for The Network State book here and make sure it's in quotations]
[Optional: you can add the word "True" (without quotations) as a 2nd argument if you want to view full context / prompt that is sent the Open AI API]`

Example:

`python run.py "Why do we need network states?"`

Other notes:
- Note that because of some excel parsing issues, I've been uploading to google sheets to view it. Google sheets seems to understand the `all_chunks.csv` file but excel seems to have issues. Probably some encoding issue that I'm not going to fix right now.
