#!/usr/bin/env python3
"""Scrape website for menu of the week
"""

import argparse
from lxml import html
import requests

def args_parser():
    """Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--web_page',
                        default='https://ericsson.foodbycoor.se/ericofood/en/weekmenu',
                        help="Webpage to be scraped")
    return parser.parse_args()

def main():
    """Main function
    """
    # Read the web page and extract the html content
    args = args_parser()
    page = requests.get(args.web_page)
    tree = html.fromstring(page.content)

    # Extract html tag information
    titles = tree.xpath('//div[@class="element title col-md-4 col-print-3"]/text()')
    titles = [x.strip() for x in titles]
    descriptions = tree.xpath('//div[@class="element description col-md-4 col-print-5"]/text()')
    prices = tree.xpath('//div[@class="element price col-md-1 col-print-1"]/text()')
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

    # Check restaurant name
    restaurant = "EricoFood" if "ericofood" in args.web_page else "Factory"
    val = 4 if restaurant == "EricoFood" else 3

    # Write in text file
    with open("menu.txt", "w") as f:
        for day in weekdays:
            f.write("{0}\n".format(day))
            for i in range(val):
                f.write("{0} {1} {2}\n".format(titles[i], descriptions[i], prices[i]))
            f.write("\n")


if __name__ == '__main__':
    main()
