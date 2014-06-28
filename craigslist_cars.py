import argparse 
import sys 
import requests 
from bs4 import BeautifulSoup
import urlparse 
from collections import defaultdict
import dateutil.parser
from dateutil.relativedelta import relativedelta
from datetime import datetime

def parse_car_conditions(condition_groups):
    """Return dictionary with car conditions"""
    conditions_dict = defaultdict(list)
    for condition_group in condition_groups:
        # span tags have the condition e.g. odometer, title
        conditions = condition_group.find_all('span')
        for condition in conditions:
            # a condition is either separated as : separated key value
            # or just a one line text item, gettable by using beautiful
            # soup's text method
            condition_str = condition.text.strip().split(':')
            if len(condition_str) > 1:
                # if condition is a key value pair then update car 
                # condition dictionary e.g. odometer: 60000
                conditions_dict[condition_str[0].strip()].append(condition_str[1].strip())
            else:
                # otherwise add value under generic attribute
                conditions_dict["attribute"].append(condition_str[0].strip())
    return conditions_dict


def parse_time_posted(soup):
    """Zone agnostic parse of posting date for car"""
    time_posted = dateutil.parser.parse(soup.find('time').attrs['datetime']).replace(tzinfo=None)
    return time_posted


def parse_car_listing(details_url):
    """Scrape car details craigslist page for given url"""
    response = requests.get(details_url)
    soup = BeautifulSoup(response.content)

    # car conditions are grouped in p tags with class attrgroup
    condition_groups = soup.find_all('p', {'class': 'attrgroup'})
    car_attributes = parse_car_conditions(condition_groups)

    # Add to conditions the time the car listing was created
    time_posted = parse_time_posted(soup)
    car_attributes["time_posted"].append(time_posted)

    car_attributes["url"].append(details_url)
    
    # The main heading on car details page (frequently has car price listed)
    posting_title = soup.find('h2', {'class':'postingtitle'}).text.strip()
    car_attributes["posting_title"].append(posting_title)

    posting_body = soup.find('section', {'id':'postingbody'}).text.strip()
    car_attributes["posting_body"].append(posting_body)
    return car_attributes


def get_craigslist_cars(city, limit, brand=None, model=None, minimum_price=None, minimum_year=None):
    """Search list of cars and trucks on craigslist"""
    
    # Craigslist url for car listings for a city
    base_url = 'https://' + city + '.craigslist.org/'
    listings_url = urlparse.urljoin(base_url, 'search/cto')

    # Search cragislist for given car attributes
    response = requests.get(listings_url, 
        params={'query': brand + "+" + model, 'minAsk': minimum_price,
         'autoMinYear': minimum_year, 'sort': 'priceasc'})

    soup = BeautifulSoup(response.content)

    # Each returned car listing is in a html span tag with class pl
    car_listings = soup.find_all('span', {'class': 'pl'})
    cars = []

    for car in car_listings:
        # Get car details page link url
        if len(cars) >= limit: break
        details_link = car.find('a').attrs['href']
        details_url = urlparse.urljoin(base_url, details_link)
        cars.append(parse_car_listing(details_url))

    return cars


def filter_cars(cars, max_mileage, unallowed_conditions, num_weeks):
    """return cars with acceptable mileage, state, posting within time_range"""
    min_posting_date = datetime.now() - relativedelta(weeks=+2)
    filtered_cars = []

    for car in cars:
        odometer = None
        if "odometer" in car:
            odometer = car.get("odometer")[0]
        title = None
        if "title" in car:
            title = car.get("title")[0]

        time_posted = car.get("time_posted")[0]

        if odometer < max_mileage and title not in unallowed_conditions and time_posted >= min_posting_date:
            filtered_cars.append(car)

    return filtered_cars


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
    parser.add_argument("-d", "--maximum_odometer", default='100000',
        help='maximum miles travelled by car before purchase')
    parser.add_argument("-t", "--blacklist_titles", nargs='+', default=['salvage', 'rebuilt'],
        help='List unacceptable states for car, e.g. You may want to filter out cars that \
        have been totalled or salvaged')
    parser.add_argument("-w", "--week_range", default=2,
        help='number of weeks to search car listings for starting from now')
    parser.add_argument("-l", "--max_results", default=20,
        help='limit to this number of results for cars returned')
    parser.add_argument("-o", "--output",
        help='write matching cars to file')
    parser.add_argument("-v", "--verbose", action='store_true',
        help='print debug output')

    try:
        args, extra_args = parser.parse_known_args()
    except Exception, e:
        print e
        sys.exit(1)

    all_cars = get_craigslist_cars(args.city, args.max_results, args.brand, args.model, args.minimum_price,
     args.minimum_year)
    
    filtered_cars = filter_cars(all_cars, args.maximum_odometer, args.blacklist_titles, args.week_range)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
