import argparse

parser = argparse.ArgumentParser(
	description="craigslist car finder", parents=())
parser.add_argument("-b", "--brand", default='honda',
                   help='car brand')
parser.add_argument("-m", "--model", default='civic',
                   help='car model')
parser.add_argument("--minimum_price", default='4000',
                   help='car model')