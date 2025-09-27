from bs4 import BeautifulSoup as soup
import requests
import random


async def scrape():
    page = requests.get('https://www.thefactsite.com/1000-interesting-facts/')
    response = soup(page.text, 'html.parser')

    
    facts = [p.get_text(strip=True) for p in response.select("p.list") if p.get_text(strip=True)]
    print("test")
    return facts

async def get_random_fact():
    facts = await scrape()

    return random.choice(facts) or "Couldn't get a fact."
