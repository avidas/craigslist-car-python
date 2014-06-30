craigslist-python-car
=====================

Python library to get cars from craigslist. Filter by date posting, mileage, odometer, year, price.

Usage
-----

Clone the repo and check out the options available! Not all the filters are available yet.

~~~ sh
$ git clone https://github.com/avidas/craigslist-car-python.git
$ python craigslist_cars.py --help
usage: craigslist_cars.py [-h] [-c CITY] [-b BRAND] [-m MODEL]
                          [-p MINIMUM_PRICE] [-y MINIMUM_YEAR]
                          [-d MAXIMUM_ODOMETER]
                          [-t BLACKLIST_TITLES [BLACKLIST_TITLES ...]]
                          [-w WEEK_RANGE] [-l MAX_RESULTS] [-o OUTPUT] [-v]

craigslist car finder

optional arguments:
  -h, --help            show this help message and exit
  -c CITY, --city CITY  which city to search for
  -b BRAND, --brand BRAND
                        car brand
  -m MODEL, --model MODEL
                        car model
  -p MINIMUM_PRICE, --minimum_price MINIMUM_PRICE
  -y MINIMUM_YEAR, --minimum_year MINIMUM_YEAR
  -d MAXIMUM_ODOMETER, --maximum_odometer MAXIMUM_ODOMETER
                        maximum miles travelled by car before purchase
  -t BLACKLIST_TITLES [BLACKLIST_TITLES ...], --blacklist_titles BLACKLIST_TITLES [BLACKLIST_TITLES ...]
                        List unacceptable states for car, e.g. You may want to
                        filter out cars that have been totalled or salvaged
  -w WEEK_RANGE, --week_range WEEK_RANGE
                        number of weeks to search car listings for starting
                        from now
  -l MAX_RESULTS, --max_results MAX_RESULTS
                        limit to this number of results for cars returned
  -o OUTPUT, --output OUTPUT
                        write matching cars to file
  -v, --verbose         print debug output
~~~