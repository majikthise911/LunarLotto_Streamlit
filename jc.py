import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import ephem
from datetime import datetime, timedelta


# page_title = "Financial Portfolio Optimizer"
# page_icon = ":zap:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# layout = "centered"

# st.set_page_config(page_title = page_title, layout = layout, page_icon = page_icon)
# st.title(page_title + " " + page_icon)
page_title = "Lunar Lotto"
page_icon = "🌖"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config( page_icon = page_icon)
st.title(page_title + " " + page_icon)


# Hide Streamlit Menu and Footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# # Function to fetch historical price data
# def get_historical_data(ticker, start_date, end_date):
#     data = yf.download(ticker, start=start_date, end=end_date)
#     return data

# Function to fetch historical price data
def get_historical_data(ticker, start_date, end_date):
    start_date = pd.to_datetime(start_date).tz_localize('UTC')
    end_date = pd.to_datetime(end_date).tz_localize('UTC')
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to calculate full moon and new moon dates
from datetime import datetime

def moon_dates(start_date, end_date):
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.min.time())
    observer = ephem.Observer()
    observer.date = start_datetime
    new_moons = []
    full_moons = []
    while observer.date.datetime() <= end_datetime:
        new_moon = ephem.next_new_moon(observer.date)
        full_moon = ephem.next_full_moon(observer.date)
        new_moons.append(new_moon.datetime())
        full_moons.append(full_moon.datetime())
        observer.date = full_moon
    return new_moons, full_moons

# Default date range
default_end_date = datetime.today().date()
default_start_date = (datetime.today() - timedelta(days=365)).date()

# Input date range
start_date = st.date_input("Start Date", value=default_start_date)
end_date = st.date_input("End Date", value=default_end_date)


# Fetch historical data
btc_data = get_historical_data("BTC-USD", start_date, end_date)

# Calculate moon dates
new_moons, full_moons = moon_dates(start_date, end_date)

# Prepare moon events dataframe
import pytz

# Prepare moon events DataFrame
moon_events = pd.DataFrame({"date": new_moons + full_moons, "event": ["new_moon"] * len(new_moons) + ["full_moon"] * len(full_moons)})
moon_events["date"] = pd.to_datetime(moon_events["date"]).dt.tz_localize('UTC')

# Find nearest date in btc_data for each moon event
def nearest_date(dates, date):
    date = pd.to_datetime(date).tz_localize('UTC').tz_convert(dates[0].tz)
    nearest = min(dates, key=lambda x: abs(pd.to_datetime(x) - date))
    return nearest

full_moons = [nearest_date(btc_data.index, fm) for fm in full_moons]
new_moons = [nearest_date(btc_data.index, nm) for nm in new_moons]

# Merge moon events with btc_data
full_moon_df = btc_data.reset_index().merge(pd.DataFrame({"date": full_moons}), left_on="Date", right_on="date", how="inner")
new_moon_df = btc_data.reset_index().merge(pd.DataFrame({"date": new_moons}), left_on="Date", right_on="date", how="inner")

# Plot BTC price with moon events
fig = px.line(btc_data.reset_index(), x="Date", y="Close", title="BTC Price with Full Moon and New Moon Events")
fig.add_scatter(x=full_moon_df["Date"], y=full_moon_df["Close"], mode="markers", marker=dict(symbol="star", color="green", size=10), name="Full Moon - Buy")
fig.add_scatter(x=new_moon_df["Date"], y=new_moon_df["Close"], mode="markers", marker=dict(symbol="circle", color="red", size=10), name="New Moon - Sell")

# Display plot
st.plotly_chart(fig)

# Calculate the returns on BTC for full moon and new moon events
returns = []
for i in range(len(new_moons)):
    if i < len(full_moons):
        buy_price = new_moon_df.loc[new_moon_df["Date"] == new_moons[i], "Close"].values[0]
        sell_price = full_moon_df.loc[full_moon_df["Date"] == full_moons[i], "Close"].values[0]
        returns.append((sell_price - buy_price) / buy_price * 100)

# Create a DataFrame for the returns
returns_df = pd.DataFrame({"Date": full_moons[:len(returns)], "Return": returns})

# Calculate the cumulative returns
returns_df["CumulativeReturn"] = returns_df["Return"].cumsum()

# Calculate the Buy and Hold returns
buy_and_hold_return = (btc_data["Close"].iloc[-1] - btc_data["Close"].iloc[0]) / btc_data["Close"].iloc[0] * 100
returns_df["BuyAndHoldReturn"] = buy_and_hold_return

# add a new column to the btc_data DataFrame
btc_data["BuyAndHoldPercent"] = (btc_data["Close"] - btc_data["Close"].iloc[0]) / btc_data["Close"].iloc[0] * 100

# Create a single figure for both returns and cumulative returns
fig = px.bar(returns_df, x="Date", y="Return", title="BTC Returns and Cumulative Returns for Full Moon/New Moon Strategy")
fig.add_scatter(x=returns_df["Date"], y=returns_df["CumulativeReturn"], mode="lines", name="Cumulative Returns", line=dict(color="red"))
fig.add_scatter(x=btc_data.index, y=btc_data["BuyAndHoldPercent"], mode="lines", name="Buy and Hold Returns", line=dict(color="blue"))
fig.update_traces(name="Returns", selector=dict(type="bar"))

# Display the combined chart
st.plotly_chart(fig)
# Display the returns DataFrame
st.markdown("### Returns DataFrame")
st.dataframe(returns_df)



# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

st.markdown( ''' Made with 👾 by Jordan Clayton

[LinkedIn](https://www.linkedin.com/in/jordan-clayton/)
[Twitter](https://twitter.com/JordanJClayton2)
[Telegram](https://t.me/jordan_clayton)
''', unsafe_allow_html=True)

st.markdown( ''' Also, check out my other projects and give them a follow and a star if they deserve it: [GitHub](https://github.com/majikthise911)''', unsafe_allow_html=True)