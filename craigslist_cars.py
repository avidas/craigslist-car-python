import argparse
import sys
import requests
from bs4 import BeautifulSoup
import urlparse
from collections import defaultdict

def parse_car_conditions(condition_groups):
    """Return dictionary with car conditions"""
    conditions_dict = defaultdict(list)
    for condition_group in condition_groups:
        # span tags have the condition e.g. odometer, title
        conditions = condition_group.find_all('span')
        for condition in conditions:
            # a condition is either separated as : separated key value
            # or just a one line text item
            condition_str = condition.text.strip().split(':')
            if len(condition_str) > 1:
                # if condition is a key value pair then update car 
                # condition dictionary e.g. odometer: 60000
                conditions_dict[condition_str[0].strip()].append(condition_str[1].strip())
            else:
                # otherwise add value under generic attribute
                conditions_dict["attribute"].append(condition_str[0].strip())
    return conditions_dict


def parse_car_listing(details_url):
    """Scrape car details craigslist page for given url"""
    response = requests.get(details_url)
    soup = BeautifulSoup(response.content)
    # car conditions are grouped in p tags with class attrgroup
    condition_groups = soup.find_all('p', {'class': 'attrgroup'})
    condition_list = parse_car_conditions(condition_groups)


def get_craigslist_cars(city, brand=None, model=None, minimum_price=None, minimum_year=None):
    """Search list of cars and trucks on craigslist"""
    
    # Craigslist url for car listings for a city
    base_url = 'https://' + city + '.craigslist.org/'
    listings_url = urlparse.urljoin(base_url, 'search/cto')

    # Search cragislist for given car attributes
    response = requests.get(listings_url, 
        params={'query': brand + "+" + model, 'minAsk': minimum_price,
         'autoMinYear': minimum_year, 'sort': 'priceasc'})
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

    get_craigslist_cars(args.city, args.brand, args.model, args.minimum_price,
     args.minimum_year)
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
