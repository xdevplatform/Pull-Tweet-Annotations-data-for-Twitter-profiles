import sys
import os
import requests
from requests_oauthlib import OAuth1
import json
import itertools

# To set your environmental variables in your terminal run the following lines:
# export 'API_KEY'='<your_api_key>'
# export 'API_SECRET'='<your_api_secret>'
# export 'API_TOKEN'='<your_api_token>'
# export 'API_TOKEN_SECRET'='<your_api_token_secret>'

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
api_token = os.environ.get("API_TOKEN")
api_token_secret = os.environ.get("API_TOKEN_SECRET")  

auth = OAuth1(api_key, api_secret, 
            api_token, api_token_secret)

url = "https://api.twitter.com/2/tweets/search/recent"

def get_username():
    username = input("Input username (e.g. bbcnews): ")
    if username[0] == "@":
        username = username[1:]
    return username

def make_payload(username): 
    payload = {"query": f"from:{username}", "tweet.fields": "context_annotations,entities", "max_results": "100"}
    return payload

def connect_to_endpoint(url, auth, payload):
    try:
        response = requests.request("GET", url, params=payload, auth=auth)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
            print(response.text)
        if response.status_code == 200: 
            print(f"Success ({response.status_code})")
        return response.json()
    except: 
        print("Something went wrong. Make sure you've exported your environment keys and tokens before running the script. Your credentials need to be linked to an App that has access to the Twitter API v2.")
        sys.exit()

def get_annotations(username, response):

    domain = []
    entity = []
    person = []
    place = []
    product = []
    organization = []
    other = []

    tweet_count = 0

    try: 
        for element in response["data"]:
            tweet_count += 1

            if "context_annotations" in element:
                for annotation in element["context_annotations"]: 
                    domain.append(annotation["domain"]["name"])
                    entity.append(annotation["entity"]["name"])
                    
            if "entities" in element:
                if "annotations" in element["entities"]:
                    for annotation in element["entities"]["annotations"]:
                        if annotation["probability"] >= 0.5:
                            if annotation["type"] == "Person":
                                person.append(annotation["normalized_text"])
                            elif annotation["type"] == "Place":
                                place.append(annotation["normalized_text"])
                            elif annotation["type"] == "Product":
                                product.append(annotation["normalized_text"])
                            elif annotation["type"] == "Organization":
                                organization.append(annotation["normalized_text"])
                            elif annotation["type"] == "Other":
                                other.append(annotation["normalized_text"])
                            else:
                                pass

        domain_frequency = {d:domain.count(d) for d in domain} 
        entity_frequency = {e:entity.count(e) for e in entity} 

        domain_frequency_ordered = {k: v for k, v in sorted(domain_frequency.items(), key=lambda item: item[1], reverse=True)}
        entity_frequency_ordered = {k: v for k, v in sorted(entity_frequency.items(), key=lambda item: item[1], reverse=True)} 
        
        person_frequency = {i:person.count(i) for i in person}
        place_frequency = {i:place.count(i) for i in place}
        product_frequency = {i:product.count(i) for i in product} 
        organization_frequency = {i:organization.count(i) for i in organization}
        other_frequency = {i:other.count(i) for i in other}

        person_frequency_ordered = {k: v for k, v in sorted(person_frequency.items(), key=lambda item: item[1], reverse=True)}
        place_frequency_ordered = {k: v for k, v in sorted(place_frequency.items(), key=lambda item: item[1], reverse=True)}
        product_frequency_ordered = {k: v for k, v in sorted(product_frequency.items(), key=lambda item: item[1], reverse=True)}
        organization_frequency_ordered = {k: v for k, v in sorted(organization_frequency.items(), key=lambda item: item[1], reverse=True)}
        other_frequency_ordered = {k: v for k, v in sorted(other_frequency.items(), key=lambda item: item[1], reverse=True)}

    except:
        print(f"""
        No topics data to analyse for @{username} in the past week
        """)
        sys.exit()

    print(f"""
    Total number of Tweets returned for the past 7 days: {tweet_count}
    """)

    return domain_frequency_ordered, entity_frequency_ordered, person_frequency_ordered, place_frequency_ordered, product_frequency_ordered, organization_frequency_ordered, other_frequency_ordered

def annotations_analysis(username, domains, entities): 

    domains_count = 0
    entities_count = 0

    for i in domains: 
        domains_count += 1
    
    for i in entities: 
        entities_count += 1

    print(f"""
    =========
    The following context annotations topics are ranked in order of frequency for the past week:
    """)    

    if not domains and not entities: 
        print(f"""
        --- No annotations topics to return for @{username} in the past week
        """)
    
    elif domains_count >= 5 and entities_count >= 5:
        top_five_domains = dict(itertools.islice(domains.items(), 5))
        top_five_entities = dict(itertools.islice(entities.items(), 5))
        print(f"""
        Top five domain topics for @{username} in the past week: {top_five_domains}
        ~~~~~
        Top five entities topics for @{username} in the past week: {top_five_entities} 
        """)
    
    elif domains_count >= 3 and entities_count >= 3: 
        top_three_domains = dict(itertools.islice(domains.items(), 3))
        top_three_entities = dict(itertools.islice(entities.items(), 3))
        print(f"""
        Top three domain topics for @{username} in the past week: {top_three_domains}
        ~~~~~
        Top three entities topics for @{username} in the past week: {top_three_entities}"
        """) 

    elif domains_count >= 1 and entities_count >= 1:
        print(domains.items(), entities.items())
        domains_list = dict(itertools.islice(domains.items()))
        entities_list = dict(itertools.islice(entities.items()))
        print(f"""
        Limited domain topics available for @{username} in the past week. This includes: {domains_list}
        ~~~~~
        Limited entities topics available for @{username} in the past week. This includes: {entities_list}
        """)  
    
    else: 
        print(f"""
        --- No annotations topics to return for @{username} in the past week
        """)

def entities_analysis(username, person, place, product, organization, other): 

    person_count = 0
    place_count = 0
    product_count = 0
    organization_count = 0
    other_count = 0

    for i in person: 
        person_count += 1
    
    for i in place: 
        place_count += 1
    
    for i in product: 
        product_count += 1

    for i in organization: 
        organization_count += 1

    for i in other: 
        other_count += 1

    print(f"""
    =========
    Entities are only returned for the past week if confidence in their categorization is of 0.5 or higher:
    """)

    if not person and not place and not product and not organization and not other: 
        print(f"""
        --- No entities to return for @{username} in the past week
        """)

    if person_count >= 1: 
        top_person = dict(itertools.islice(person.items(), 5))
        print(f"""
        --- The top people @{username} Tweets about include: {top_person}
        """)
    
    if place_count >= 1: 
        top_place = dict(itertools.islice(place.items(), 5))
        print(f"""
        --- The top places @{username} Tweets about include: {top_place}
        """)    

    if product_count >= 1: 
        top_product = dict(itertools.islice(product.items(), 5))
        print(f"""
        --- The top products @{username} Tweets about include: {top_product}
        """)

    if organization_count >= 1: 
        top_organization = dict(itertools.islice(organization.items(), 5))
        print(f"""
        --- The top organizations @{username} Tweets about include: {top_organization}
        """)

    if other_count >= 1: 
        top_other = dict(itertools.islice(other.items(), 5))
        print(f"""
        --- The top other topics @{username} Tweets about include: {top_other}
        """)

def main():
    username = get_username() 
    payload = make_payload(username)
    json_response = connect_to_endpoint(url, auth, payload)
    domains, entities, person, place, product, organization, other = get_annotations(username, json_response)
    annotations_analysis(username, domains, entities)
    entities_analysis(username, person, place, product, organization, other)

if __name__ == "__main__":
    main()