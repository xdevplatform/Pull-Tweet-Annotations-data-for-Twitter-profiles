import sys
import os
import requests
from requests_oauthlib import OAuth1
import json
import itertools
import csv

# To set your environmental variables in your terminal run the following lines:
#   export 'API_KEY'='<your_api_key>'
#   export 'API_SECRET'='<your_api_secret>'
#   export 'API_TOKEN'='<your_api_token>'
#   export 'API_TOKEN_SECRET'='<your_api_token_secret>'

# To import @handles for which to pull annotations data: 
#   Create "Twitter_handles.csv" and populate with handles/usernames (see sample.csv as example)

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
api_token = os.environ.get("API_TOKEN")
api_token_secret = os.environ.get("API_TOKEN_SECRET")  

auth = OAuth1(api_key, api_secret, 
            api_token, api_token_secret)

url = "https://api.twitter.com/2/tweets/search/recent"

def get_usernames():

    twitter_handles = open("Twitter_handles.csv", "r") 
    usernames = []

    for username in twitter_handles: 
        usernames.append(username.strip())

    print(usernames)
    return usernames

def make_request(url, auth, usernames):

    payload_objects = []

    for username in usernames:

        query = {"query": f"from:{username} -is:retweet", "tweet.fields": "context_annotations", "expansions": "author_id", "user.fields": "username", "max_results": "100"} 

        try:
            response = requests.request("GET", url, params=query, auth=auth)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
                print(response.text)
            if response.status_code == 200: 
                print(f"Success ({response.status_code})")
            payload_objects.append(response.json())
        except: 
            print("Something went wrong. Make sure you've exported your environment keys and tokens before running the script. Your credentials need to be linked to an App that has access to the Twitter API v2.")
            sys.exit()
    
    return payload_objects

def get_annotations(usernames, payload_objects): 

    all_results = []

    for i, response in enumerate(payload_objects):
        
        print("Item")
        result = {"annotation_domains": [], "annotation_entities": []}
        tweet_count = 0

        if "data" in response:

            for tweet_object in response["data"]:
                tweet_count += 1

                if "context_annotations" in tweet_object:
                    for annotation in tweet_object["context_annotations"]: 
                        result["annotation_domains"].append(annotation["domain"]["name"])
                        result["annotation_entities"].append(annotation["entity"]["name"])

        result["username"] = usernames[i]
        
        result["tweet_count"] = tweet_count
       
        all_results.append(result) 

    return all_results

def order_annotations(all_results): 

    all_ordered_results = []

    for result in all_results: 

        annotation_domains = result["annotation_domains"]
        annotation_entities = result["annotation_entities"]

        domain_frequency = {d:annotation_domains.count(d) for d in annotation_domains}
        entity_frequency = {e:annotation_entities.count(e) for e in annotation_entities} 

        domain_frequency_ordered = {k: v for k, v in sorted(domain_frequency.items(), key=lambda item: item[1], reverse=True)}
        entity_frequency_ordered = {k: v for k, v in sorted(entity_frequency.items(), key=lambda item: item[1], reverse=True)} 

        ordered_result = {"username": result["username"], "tweet_count": result["tweet_count"] , "domain_frequency": domain_frequency_ordered, "entity_frequency": entity_frequency_ordered}
        
        all_ordered_results.append(ordered_result)

    return all_ordered_results

def export_to_csv(all_ordered_results):
    
    max_count = 5   # Change number of top results displayed here

    with open('annotations.csv', 'w') as csvfile:

        writer = csv.writer(csvfile)

        headers = ["username", "total_tweet_count"]
        
        for i in range(max_count):
            headers.append(f"annotation_domain_{i}")
            headers.append(f"count")

        for i in range(max_count):
            headers.append(f"annotation_entity_{i}")
            headers.append(f"count")    
        
        writer.writerow(headers)

        for result in all_ordered_results: 
            row = []
            row.append(result["username"])
            row.append(result["tweet_count"])
            
            annotation_domains = result["domain_frequency"]
            annotation_entities = result["entity_frequency"]

            count_domains = 0
            count_entities = 0

            for k, v in annotation_domains.items():
                if count_domains < max_count: 
                    row.append(k)
                    row.append(v)
                    count_domains += 1
            
            for i in range(count_domains, max_count):
                row.append("")
                row.append("")

            for k, v in annotation_entities.items():
                if count_entities < max_count: 
                    row.append(k)
                    row.append(v)
                    count_entities += 1
            
            for i in range(count_entities, max_count):
                row.append("")
                row.append("")
        
            writer.writerow(row)

def main():
    usernames = get_usernames()
    payload_objects = make_request(url, auth, usernames)
    all_results = get_annotations(usernames,payload_objects)
    all_ordered_results = order_annotations(all_results)
    export_to_csv(all_ordered_results)

if __name__ == "__main__":
    main()