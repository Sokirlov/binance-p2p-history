import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

from threading import Thread
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import P2PTrade
from p2p import p_to_p_parser

app = Flask(__name__)

# DB connect
engine = create_engine('sqlite:///p2p_trades.db')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    results = session.query(P2PTrade.created_at, P2PTrade.price).order_by(P2PTrade.created_at).all()

    # Create DataFrame from data
    df = pd.DataFrame(results, columns=['created_at', 'price'])
    df['time_slot'] = df['created_at'].dt.strftime('%Y-%m-%d %H')  # to group data by minutes '%Y-%m-%d %H:%M'
    top_3_df = df.groupby(["time_slot"]).max().reset_index(drop=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=top_3_df['created_at'], y=top_3_df['price'], mode='lines+markers', name='Price'))
    fig.update_layout(
        title="USDT/UAH",
        xaxis_title="Time",
        yaxis_title="Price",
        xaxis_rangeslider_visible=True,
        template="plotly_dark",
    )

    # convert plotly to html
    graph_html = pio.to_html(fig, full_html=False)
    return render_template('index.html', graph_html=graph_html)


if __name__ == '__main__':
    # start parser
    parser_thread = Thread(target=p_to_p_parser)
    parser_thread.start()
    # start Flask
    app.run(debug=True, use_reloader=False)
