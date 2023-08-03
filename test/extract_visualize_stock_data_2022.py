import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup

import plotly.graph_objects as go
from plotly.subplots import make_subplots

print(pd.__version__)

def plot_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price ($)", "Historical Revenue($)"), vertical_spacing=.5)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($ Millions)", row=2, col=1)
    fig.update_layout(showlegend = False, height=1000, title=stock, xaxis_rangeslider_visible=True)
    fig.show()


tesla_data= yf.Ticker('TSLA')

tsla_data = tesla_data.history(period='max')

tsla_data.reset_index(inplace=True)

tsla_data.head()

print(tsla_data)

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'

html_text = requests.get(url).text

soup = BeautifulSoup(html_text, 'html5lib')

tsla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

tables = soup.find_all('table')

table_index = 0

for index, table in enumerate(tables):
    if ('Tesla Quarterly Revenue' in str(table)):
        table_index = index

for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if(col!=[]):
        date = col[0].text
        revenue = col[1].text.replace("$","").replace(",","")
        tsla_revenue = pd.concat([tsla_revenue, pd.DataFrame([{'Date':date, 'Revenue':revenue}], columns=["Date", "Revenue"])], ignore_index=True)

tsla_revenue = tsla_revenue[tsla_revenue["Revenue"]!='']

# plot_graph(tsla_data, tsla_revenue, 'Tesla Historical Share Price & Revenue')