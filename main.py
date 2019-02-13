#!/usr/bin/env python3
"""Scrape website for menu of the week
"""

import argparse
import time
from lxml import html
import requests


def args_parser():
    """Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def parse_html(web_page):
    """Parse the given webpage and extract the desired content such as price, food description
    Args:
        web_page: (string) URL of the webpage
    """
    # Read the web page and extract the html content
    page = requests.get(web_page)
    tree = html.fromstring(page.content)

    # Extract html tag information
    week_name = tree.xpath('//h2[@class="header-week"]/text()')
    week_name = week_name[0].strip()

    titles = tree.xpath('//div[@class="element title col-md-4 col-print-3"]/text()')
    titles = [x.strip() for x in titles]

    descriptions = tree.xpath('//div[@class="element description col-md-4 col-print-5"]/text()')
    prices = tree.xpath('//div[@class="element price col-md-1 col-print-1"]/text()')
    return week_name, titles, descriptions, prices

def write_menu(restaurant_name, week_name, titles, descriptions, prices):
    """Write the menu from the data in the argumntns to a text file
    Args:
        restaurant_name: (string) Name of the restaurant
        week_name: (string) Name of the week
        titiles: (string) Category of the food
        descriptions: (string) Description of the food
        prices: (string) Price of each food
    """
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

    val = 4 if restaurant_name == "EricoFood" else 3

    file_name = restaurant_name + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    with open(file_name, "w") as f:
        f.write("{0}\n".format(week_name))
        for day in weekdays:
            f.write("{0}\n".format(day))
            for i in range(val):
                f.write("{0} {1} {2}\n".format(titles[i], descriptions[i], prices[i]))
            f.write("\n")

def main():
    """Main function
    """
    # Read arguments
    args = args_parser()

    web_pages = ["https://ericsson.foodbycoor.se/ericofood/en/weekmenu",
                 "https://ericsson.foodbycoor.se/the-factory/en/weekmenu"]

    for web_page in web_pages:
        # Extract content from the webpage
        week_name, titles, descriptions, prices = parse_html(web_page)

        # Check restaurant name
        restaurant_name = "EricoFood" if "ericofood" in web_page else "Factory"

        # Write in text file
        write_menu(restaurant_name, week_name, titles, descriptions, prices)


if __name__ == '__main__':
    main()
