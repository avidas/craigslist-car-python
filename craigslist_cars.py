import argparse
import sys
import requests
from bs4 import BeautifulSoup
import urlparse

def parse_car_listing(details_url):
    """Scrape car details craigslist page for given url"""
    response = requests.get(details_url)
    soup = BeautifulSoup(response.content)
    condition_groups = soup.find_all('p', {'class': 'attrgroup'})


def get_craigslist_cars(city, brand=None, model=None, minimum_price=None, minimum_year=None):
    """Search list of cars and trucks on craigslist"""
    
    # Craigslist url for car listings for a city
    base_url = 'https://' + city + '.craigslist.org/'
    listings_url = urlparse.urljoin(base_url, 'search/cto')

    # Search cragislist for given car attributes
    response = requests.get(listings_url, 
        params={'query': brand + "+" + model, 'minAsk': minimum_price, 'autoMinYear': minimum_year, 'sort': 'priceasc'})
    print response.content

    soup = BeautifulSoup(response.content)

    # Each returned car listing is in a html span tag with class pl
    car_listings = soup.find_all('span', {'class': 'pl'})
    print car_listings

    for car in car_listings:
        # Get details page link url
        details_link = car.find('a').attrs['href']
        details_url = urlparse.urljoin(base_url, details_link)
        parse_car_listing(details_url)


def main():
    parser = argparse.ArgumentParser(
        description="craigslist car finder", parents=())
    parser.add_argument("-c", "--city", default='austin',
        help='which city to search for')
    parser.add_argument("-b", "--brand", default='honda',
        help='car brand')
    parser.add_argument("-m", "--model", default='civic',
        help='car model')
    parser.add_argument("-p", "--minimum_price", default='4000')
    parser.add_argument("-y", "--minimum_year", default='2007')

    try:
        args, extra_args = parser.parse_known_args()
        print(args.model)
    except Exception, e:
        print e
        sys.exit(1)

    get_craigslist_cars(args.city, args.brand, args.model, args.minimum_price, args.minimum_year)
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
