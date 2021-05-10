from datetime import date
import time

from polygon import RESTClient

import models.models as md
from utils import get_next_day_str, get_last_n_days
from Config import config


def main(ticker, from_, to=None):
    key = config.POLYGON_KEY

    if not to:
        to = get_next_day_str(from_)

    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        try:
            resp = client.stocks_equities_aggregates(ticker.ticker, 1, "minute", from_, to, unadjusted=True)
        except Exception as msg:
            print(msg)
            resp = None

        print(f"Minute aggregates for {ticker.ticker} between {from_} and {to}.")

        if hasattr(resp, "results"):
            new_added = md.StocksAggregates.save_stock_aggregates(resp.ticker, resp.results)
            print(f"Got from polygon: {len(resp.results)}")
            print(f"Added to DB: {new_added}")
        else:
            print("Polygon didn't return any results")


if __name__ == '__main__':
    stock_names = md.StocksNames.get_stock_names()
    days_to_collect = get_last_n_days(date.today().strftime("%Y-%m-%d"), n=config.DAYS_TO_LOAD)
    for day in days_to_collect:
        for stock_name in stock_names:
            main(stock_name, day)
            time.sleep(60/5)
