import datetime
import logging
import time
import pytz
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, P2PTrade

logging.basicConfig(
    # filename=logfile_path,
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("[P2P BINANCE PARSER]")

# Create DB
engine = create_engine('sqlite:///p2p_trades.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_p2p_trade(session, trade_data, date):
    existing_trade = session.query(P2PTrade).filter_by(
        adv_no=trade_data['adv']['advNo'],
        surplus_amount=trade_data['adv']['surplusAmount'],
        price=trade_data['adv']['price'],
    ).first()

    if existing_trade is None:
        p2p_trade = P2PTrade(
            adv_no=trade_data['adv']['advNo'],
            asset=trade_data['adv']['asset'],
            fiat_unit=trade_data['adv']['fiatUnit'],
            price=trade_data['adv']['price'],
            surplus_amount=trade_data['adv']['surplusAmount'],
            tradable_quantity=trade_data['adv']['tradableQuantity'],
            max_single_trans_amount=trade_data['adv']['maxSingleTransAmount'],
            min_single_trans_amount=trade_data['adv']['minSingleTransAmount'],
            pay_time_limit=trade_data['adv']['payTimeLimit'],
            user_no=trade_data['advertiser']['userNo'],
            real_name=trade_data['advertiser'].get('realName'),
            nick_name=trade_data['advertiser'].get('nickName'),
            month_order_count=trade_data['advertiser']['monthOrderCount'],
            month_finish_rate=trade_data['advertiser']['monthFinishRate'],
            positive_rate=trade_data['advertiser']['positiveRate'],
            created_at=date
        )

        for method in trade_data['adv']['tradeMethods']:
            p2p_trade.add_trade_method(
                identifier=method['identifier'],
                trade_method_name=method['tradeMethodName'],
                trade_method_short_name=method['tradeMethodShortName']
            )
        session.add(p2p_trade)
        session.commit()
        return True
    else:
        return False


def get_binance_p2p_data(asset, page=1, trade_type="BUY", fiat="USD", payment_method="PrivatBank"):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    data = {
        "page": page,
        "rows": 10,   # max value 10
        "payTypes": [payment_method],
        "asset": asset,
        "tradeType": trade_type,
        "fiat": fiat,
        "publisherType": "merchant"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.debug(f"Error: {response.status_code}")
        return None


def data_parse():
    date = datetime.datetime.now(tz=pytz.timezone('Europe/Kiev'))
    p2p_data = get_binance_p2p_data(page=1, asset="USDT", trade_type="SELL", fiat="UAH")
    if p2p_data:
        for ad in p2p_data['data']:
            md = create_p2p_trade(session, ad, date)
            if md:
                banks = [i['identifier'] for i in ad['adv']['tradeMethods']]
                logger.info(f"Price: {ad['adv']['price']},\t"
                      f"TYPE: {ad['adv']['tradeType']}"
                      f"Available: {ad['adv']['surplusAmount']},\t\t"
                      f"Nickname: {ad['advertiser']['nickName']}\t\t"
                      f"Bank: {banks}"
                      )
def timeout(r):
    i = 0
    while i < r:
        i += 10
        time.sleep(10)
        logger.debug(f'Last: {r - i} second')


def p_to_p_parser():
    while True:
        data_parse()
        # logger.info('Wait 300 sec')
        timeout(1*60*60)


if __name__ == '__main__':
    p_to_p_parser()
