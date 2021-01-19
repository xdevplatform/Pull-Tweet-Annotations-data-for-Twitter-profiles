# Pull Tweet annotations for Twitter profiles

This sample code pulls contextual information for given Twitter profiles, based on their recent Tweets (past 7 days), including: 
* Context annotations (annotation domains and annotation entities)
* Entity annotations (people, places, products, and organisations)

Specifically, this code uses: 
* [The Twitter API v2 recent search endpoint](https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent)
* [Tweet annotations](https://developer.twitter.com/en/docs/twitter-api/annotations)

Each profile's Tweets are analysed, and the top most frequent annotation topics detected in their Tweets are returned in order of frequency. 

Note that this code does not paginate through the data returned by the API. As a result, no more than 100 Tweets will be analysed at any given time.

There are two scripts: 
* `main.py` returns both context annotations and entity annotations data, through the command line interface;
* `data_to_csv.py` returns context annotations data in a CSV file. Does not return entity annotations.

## Environment variables

To run this, you will first need to export your keys and tokens for your [Twitter developer App](https://developer.twitter.com/en/docs/apps/overview). Make sure to use an App that has access to the Twitter API v2. 

In the command line, type the following lines of code. Replace each placeholder with your own credentials (without the `<>`).

```
export 'API_KEY'='<your_api_key>'
export 'API_SECRET'='<your_api_secret>'
export 'API_TOKEN'='<your_api_token>'
export 'API_TOKEN_SECRET'='<your_api_token_secret>'
```

## `main.py`

This script returns context and entities annotations, via the command line interface, for a given Twitter profile (aka @username). You will be prompted to pass in the @username when you run the script.

When present, entity annotations are analysed and returned. This means that specific people, places, products, organisations, or other topics that have been mentioned in the user's Tweets in the past week are displayed. These entities are only displayed if they have been categorised with a confidence score of 0.5 or higher.

Note that, although 100% of Tweets are reviewed, due to the contents of Tweet text, only a portion are annotated.

To run this script:

```
python3 main.py
```

## `data_to_csv.py`

This script returns context annotations data in a CSV file (generates a file entitled `annotations.csv`) for a list of given usernames. 

To pass in the usernames (aka @handles) for which you want to pull annotations data: populate the file entitled `Twitter_handles.csv` with the desired handles/usernames, without the @ (as per the example).

You may want to add `Twitter_handles.csv` to your `.gitignore` file.

Note that this script does **not** return entity annotations.

By default, this script will return a CSV file with rows, each of which contains: 
* Given username
* Number of Tweets sent in the past week (maximum 100)
* Top 5 context annotation domains (and the number of times each of these was mentioned)
* Top 5 context annotation entities (and the number of times each of these was mentioned) 

You can change the number of top results returned towards the bottom of the script: 

```
    max_count = 5   # Change number of top results displayed here
```

To run this script:

```
python3 data_to_csv.py
```
