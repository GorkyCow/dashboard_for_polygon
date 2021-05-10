from sqlalchemy import (BigInteger, Column, DateTime, Float, Integer, String,
                        asc, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint

from Config import config
from utils import ts_to_datetime

engine = create_engine(
    "postgresql://{0}:{1}@{2}/{3}".format(
        config.DB_USERNAME,
        config.DB_PASSWORD,
        config.DB_HOST,
        config.DB_NAME,
    ),
    encoding="utf-8",
)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class StocksAggregates(Base):
    __tablename__ = "stocks_aggregates"
    __table_args__ = (PrimaryKeyConstraint("ticker", "timestamp"),)

    ticker = Column(String(64, convert_unicode=True))
    timestamp = Column(DateTime)
    volume = Column(BigInteger)
    volume_weight = Column(Float)
    open = Column(Float)
    close = Column(Float)
    highest = Column(Float)
    lowest = Column(Float)
    number = Column(Integer)

    def __repr__(self):
        return (
            f"<StocksAggregates(ticker='{self.ticker}', timestamp='{self.timestamp}', volume={self.volume}, "
            + f"volume_weight={self.volume_weight}, open={self.open}, close={self.close}, highest={self.highest}, lowest={self.lowest}, number={self.number})>"
        )

    @staticmethod
    def get_stock_aggregates(ticker, from_, to):
        session = Session()
        result = []

        for aggregate in (
            session.query(StocksAggregates)
            .filter_by(ticker=ticker)
            .filter(StocksAggregates.timestamp.between(from_, to))
            .order_by(asc(StocksAggregates.timestamp))
        ):
            result.append(aggregate)
        session.close()
        return result

    @staticmethod
    def save_stock_aggregates(ticker, resp_aggregates):
        session = Session()
        stock_aggregates = [
            StocksAggregates(
                ticker=ticker,
                timestamp=ts_to_datetime(aggregate["t"]),
                volume=aggregate["v"],
                volume_weight=aggregate["vw"],
                open=aggregate["o"],
                close=aggregate["c"],
                highest=aggregate["h"],
                lowest=aggregate["l"],
                number=aggregate["n"],
            )
            for aggregate in resp_aggregates
        ]
        new_uniqe_aggregates = []

        for stock_aggregate in stock_aggregates:
            try:
                session.add(stock_aggregate)
                session.flush()
                session.rollback()
                new_uniqe_aggregates.append(stock_aggregate)
            except Exception as msg:
                session.rollback()
        session.add_all(new_uniqe_aggregates)
        try:
            session.commit()
        except:
            session.rollback()
            raise
        session.close()
        return len(new_uniqe_aggregates)

    @staticmethod
    def get_days(ticker):
        session = Session()
        result = []

        for aggregate in (
            session.query(StocksAggregates)
            .filter_by(ticker=ticker)
            .order_by(asc(StocksAggregates.timestamp))
        ):
            result.append(aggregate.timestamp.strftime("%Y-%m-%d"))
        session.close()
        result = list(set(result))
        result.sort()
        return result

    @staticmethod
    def get_first_day(ticker):
        session = Session()

        result = (
            session.query(StocksAggregates)
            .filter_by(ticker=ticker)
            .order_by(asc(StocksAggregates.timestamp))
            .first()
        )
        session.close()
        return result.timestamp.strftime("%Y-%m-%d")


class StocksNames(Base):
    __tablename__ = "stocks_names"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(64, convert_unicode=True), unique=True)
    name = Column(String(64, convert_unicode=True))

    def __repr__(self):
        return (
            f"<StocksNames(id='{self.id}', ticker='{self.ticker}', name={self.name})>"
        )

    @staticmethod
    def save_stock_name(ticker, name):
        session = Session()
        stock_name = StocksNames(ticker=ticker, name=name)

        session.add(stock_name)
        try:
            session.commit()
        except Exception as msg:
            session.rollback()
            print(msg)
            session.close()
            return False
        session.close()
        return True

    @staticmethod
    def get_stock_names():
        session = Session()
        result = []

        for aggregate in session.query(StocksNames).order_by(asc(StocksNames.ticker)):
            result.append(aggregate)
        session.close()
        return result

    @staticmethod
    def get_first_ticker():
        session = Session()

        result = session.query(StocksNames).order_by(asc(StocksNames.ticker)).first()
        session.close()
        return result.ticker


Base.metadata.create_all(engine)
