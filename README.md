
# BTC Price with Full Moon and New Moon Events

This Streamlit app visualizes the historical price of Bitcoin (BTC) along with Full Moon and New Moon events. It allows users to explore the potential correlation between lunar events and the price movements of Bitcoin.

The app calculates the returns on BTC for Full Moon and New Moon events and compares them with the Buy and Hold returns.

## Features

- Interactive date selection to choose a specific date range for analysis
- Line chart showing the historical price of Bitcoin with Full Moon (Buy) and New Moon (Sell) markers
- Bar chart showing the returns on BTC for each Full Moon and New Moon event
- Line chart displaying cumulative returns for Full Moon/New Moon strategy and Buy and Hold strategy

## How to run the app locally

1. Clone the repository:

```
git clone https://github.com/your_username/your_repository.git
```

2. Change directory to the cloned repository:

```
cd your_repository
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Run the Streamlit app:

```
streamlit run app.py
```

The app will open in your default browser.

## Data sources

- Historical price data: [Yahoo Finance](https://finance.yahoo.com/)
- Moon phase calculation: [ephem](https://pypi.org/project/ephem/)

## Dependencies

- Python 3.7+
- pandas
- plotly
- yfinance
- ephem
- streamlit

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

![preview1](image/Screenshot%202023-04-19%20215810.png)
![preview2](image/Screenshot%202023-04-19%20215837.png)