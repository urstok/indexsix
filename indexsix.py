import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from IPython.display import HTML

# Define the ticker symbols for the indices
tickers = ["^NSEI", "^NSEBANK", "NIFTY_FIN_SERVICE.NS", "^CNXENERGY","^NSMIDCP","^NSEMDCP50"]
names = ["NIFTY 50", "BANK NIFTY", "FINNIFTY", "ENERGY SECTOR","NIFTY NEXT 50","NIFTY MIDCAP 50"]

# Set the date range for the past three years
end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
start_date = (pd.Timestamp.today() - pd.DateOffset(years=3)).strftime('%Y-%m-%d')

# Fetch data using yfinance
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# Resample data to quarterly frequency and calculate percentage change
quarterly_data = data.resample('Q').last()
quarterly_percent_change = quarterly_data.pct_change() * 100

# Create a figure with Plotly
fig = go.Figure()

# Add traces for each index with custom names
for i, ticker in enumerate(tickers):
    fig.add_trace(go.Scatter(x=quarterly_percent_change.index, y=quarterly_percent_change[ticker],
                             mode='lines+markers', name=names[i]))

# Customize layout
fig.update_layout(
    title='Quarterly Percentage Change in Index Values',
    xaxis_title='Quarter',
    yaxis_title='Percentage Change (%)',
    legend=dict(orientation='h', yanchor='top', y=-0.15, xanchor='center', x=0.5),
    xaxis=dict(tickformat='%Y-%m'),
    yaxis=dict(tickformat='.2f'),
    template='plotly_dark',  # Use Plotly dark theme
    plot_bgcolor='black',  # Set plot background color to black
    paper_bgcolor='black',  # Set paper background color to black
    font=dict(color='white')  # Set font color to white
)

# Show the interactive plot
plot_div = plot(fig, output_type='div', include_plotlyjs='cdn')
HTML(plot_div)
