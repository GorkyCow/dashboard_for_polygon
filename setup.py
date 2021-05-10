from models import models as md


if __name__ == "__main__":
    md.StocksNames.save_stock_name("AAPL", "Apple")
    md.StocksNames.save_stock_name("GOOGL", "Google")
    md.StocksNames.save_stock_name("WMT", "Walmart")
    md.StocksNames.save_stock_name("EBAY", "eBay Inc")
    md.StocksNames.save_stock_name("COST", "Costco")
    md.StocksNames.save_stock_name("MSFT", "Microsoft")
