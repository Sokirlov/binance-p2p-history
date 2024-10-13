from datetime import datetime

from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class TradeMethod(Base):
    __tablename__ = 'trade_methods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String, nullable=False)
    trade_method_name = Column(String, nullable=True)
    trade_method_short_name = Column(String, nullable=True)
    p2p_trade_id = Column(Integer, ForeignKey('p2p_trades.id'))

    def __repr__(self):
        return f"<TradeMethod(identifier={self.identifier}, name={self.trade_method_name})>"


class P2PTrade(Base):
    __tablename__ = 'p2p_trades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    adv_no = Column(String, nullable=False)
    asset = Column(String, nullable=False)
    fiat_unit = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    surplus_amount = Column(Float, nullable=False)
    tradable_quantity = Column(Float, nullable=False)
    max_single_trans_amount = Column(Float, nullable=False)
    min_single_trans_amount = Column(Float, nullable=False)
    pay_time_limit = Column(Integer, nullable=False)
    month_order_count = Column(Integer, nullable=False)
    month_finish_rate = Column(Float, nullable=False)
    positive_rate = Column(Float, nullable=False)
    user_no = Column(String, nullable=False)
    real_name = Column(String, nullable=True)
    nick_name = Column(String, nullable=True)
    trade_methods = relationship("TradeMethod", backref="p2p_trade", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<P2PTrade(asset={self.asset}, price={self.price})>"

    def add_trade_method(self, identifier, trade_method_name, trade_method_short_name):
        trade_method = TradeMethod(
            identifier=identifier,
            trade_method_name=trade_method_name,
            trade_method_short_name=trade_method_short_name
        )
        self.trade_methods.append(trade_method)
