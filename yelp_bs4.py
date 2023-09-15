import json
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup

CATEGORY = "contractors"
LOCATION = "San Francisco, CA"


def scrape_yelp_businesses(category, location):
    businesses = []

    for i in range(1, 2):
        url = f"https://www.yelp.com/search?find_desc={category}&find_loc={location}&start={i * 10}"
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        for link in soup.select('span.css-1egxyvc a'):
            business_url = "https://www.yelp.com" + link['href']
            business_data = scrape_business_data(business_url)
            businesses.append(business_data)

    with open('yelp/output.json', 'w') as file:
        json.dump(businesses, file)


def scrape_business_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    business_name = soup.select_one('h1.css-1se8maq').get_text(strip=True)
    business_rating = soup.select_one('span.css-1p9ibgf').get_text(strip=True)
    num_reviews = soup.select_one('span.css-1evauet a').get_text(strip=True).split()[0].strip('(')
    business_yelp_url = soup.select_one('link[rel=canonical]')['href']
    business_website = unquote(soup.select_one('p.css-1p9ibgf a')['href'].split('=')[0].split('&')[0])

    reviews = []
    review_elements = soup.select('div#reviews ul.list__09f24__ynIEd > li')[:5]
    for review_element in review_elements:
        reviewer_name = review_element.select_one('span.fs-block.css-ux5mu6 a').get_text(strip=True)
        reviewer_location = review_element.select_one('span.css-qgunke').get_text(strip=True)
        review_date = review_element.select_one('span.css-chan6m').get_text(strip=True)

        reviews.append(
            {'reviewer_name': reviewer_name, 'reviewer_location': reviewer_location, 'review_date': review_date})

    business_data = {'business_name': business_name, 'business_rating': business_rating, 'num_reviews': num_reviews,
                     'business_yelp_url': business_yelp_url, 'business_website': business_website, 'reviews': reviews}

    return business_data


if __name__ == '__main__':
    scrape_yelp_businesses(CATEGORY, LOCATION)
