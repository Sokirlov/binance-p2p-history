# Binance p2p history saver

This program ask from binance api p2p trade data every 5 min about 
- trade_type "BUY", 
- pare "USDT/UAH", 
- payment_method "PrivatBank"

Collect it to Database with SqlAlchemy<br>
To show it in web I use the Flask and show data in chart from Plotly. 

## To start project 
_(it`s non production config)_

1. Create venv
2. Install requirements
3. Run main.py

Now data start collecting
____

## Project specifics

Data group by hour, so as first start you will see only one dot on chart.
If you want see more dot you need correct grouping. 
So open `main.py` and find this line 
`df['time_slot'] = df['created_at'].dt.strftime('%Y-%m-%d %H')`
<br>you need add rewrite `%Y-%m-%d %H` to `%Y-%m-%d %H:%M`
Now restart projects then you will see every minute charts

