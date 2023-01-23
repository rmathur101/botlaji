# botlaji

This is a `python` project, `python3` was used so if you're using `python2` YMMV. 

Steps to get up and running:
1. `pip install -r requirements.txt`
2. See the `.env.example` file in the project root. Create a copy of it called `.env` and put it in in the project root. 
3. Get an API key from OpenAI. Put your API key in the `.env` file. Note that requests to the API costs money. So keep an eye on how much you're spending. (I think each request is ~$0.02 using the current model (Davinci)
4. Run the program like this: 

`python run.py [Your query (make sure it's in quotes)] [Put in "True" (without quotes) to see the entire prompt sent to Open AI API]`

Example:

`python run.py "Why do we need network states?"`

Other notes:
- Note that because of some excel parsing issues, I've been uploading to google sheets to view it. Google sheets seems to understand the `all_chunks.csv` file but excel seems to have issues. Probably some encoding issue that I'm not going to fix right now.
