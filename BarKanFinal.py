from datetime import datetime, timedelta
from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, render, ui, reactive


# Configuration
time_end = datetime.now()
time_start = datetime.now() - timedelta(days=30)
tickers = {"MSFT": "Microsoft" , "AAPL" : "APPLE", "TSLA" : "Tesla" , "AMZN" : "Amazon" , "GOOGL" : "Google", "QQQ" : "Invesco QQQ"}
API_KEY = "x" #Insert API key, we used the API from Tiingo


def get_stock_data(ticker1, ticker2, start_date, end_date):
    #  function get_stock_data uses the pandas_datareader library's get_data_tiingo() function to fetch the historical stock data 
    # for the specified tickers within the given date range using an API key.
    try:
        stock1_data = pdr.get_data_tiingo(ticker1, start_date, end_date, api_key=API_KEY)
        stock2_data = pdr.get_data_tiingo(ticker2, start_date, end_date, api_key=API_KEY)
    except:
        return None, None
    return stock1_data.reset_index(), stock2_data.reset_index()

def plot_stock_data(stock1_data, stock2_data, ticker1, ticker2, plot_type):
    # function plot_stock_data creates a new figure with subplots using the matplotlib.pyplot library 
    # The function then plots the historical stock data using the plot_type specified in the input parameter
    #  it returns the generated figure fig for display.
    fig, ax = plt.subplots()
    ax.set_xlim([time_start, time_end])
    plt.xticks(rotation = 45)
    if plot_type == "line":
        ax.plot(stock1_data["date"], stock1_data["adjClose"], label=ticker1)
        ax.plot(stock2_data["date"], stock2_data["adjClose"], label=ticker2)
        ax.set_title("Historical stock prices")
        ax.legend(loc="upper left")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
    elif plot_type == "stackplot":
        ax.stackplot(stock1_data["date"], stock1_data["adjClose"], stock2_data["adjClose"], labels=[ticker1, ticker2])
        ax.set_title("Historical stock prices")
        ax.legend(loc="upper left")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
    elif plot_type == "bar":
        ax.bar(stock1_data["date"], stock1_data["adjClose"], label=ticker1)
        ax.bar(stock2_data["date"], stock2_data["adjClose"], label=ticker2)
        ax.set_title("Historical stock prices")
        ax.legend(loc="upper left")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
    elif plot_type == "bollinger":
        # Bollinger Bands are a technical analysis tool defined by a set of trendlines (Up and Down)
        # plotted into two standard deviations (STD), positive and negative 
        # away from a simple moving average (SMA), Usually from 20 to 50 days.
        # of a security's price (Stock)
        
        def get_bollinger_bands(stock1_data, n= 20, m=2):
            # Stock1_data takes dataframe on input
            # n = smoothing Length
            # m = number of standard deviations away from MA

            #typical price
            TP = (stock1_data["high"] + stock1_data["low"] + stock1_data["close"]) / 3
            data = TP

            # Takes one column from dataframe and then calculate the SMA and STD, then 
            # the bollinger up and down bands can be calculated with two STD
            SMA = pd.Series((data.rolling(n, min_periods = n).mean()), name = "SMA")
            STD = data.rolling(n, min_periods = n).std()

            Bollinger_up = pd.Series((SMA + m * STD), name = "Bollinger_up")
            Bollinger_down = pd.Series((SMA - m * STD), name = "Bollinger_down")

            stock1_data = stock1_data.join(SMA)
            stock1_data = stock1_data.join(Bollinger_up)
            stock1_data = stock1_data.join(Bollinger_down)

            return stock1_data
        stock1_data = get_bollinger_bands(stock1_data, 20, 2)

        #Plot price using the SMA, Bollinger Up and Down and the Stock Price at close
        ax.set_title("Bollinger Bands chart " + str(ticker1))
        ax.plot(stock1_data["date"], stock1_data["adjClose"], label="Closing Prices")
        ax.plot(stock1_data["date"], stock1_data["Bollinger_up"], alpha = 0.3, label="Bollinger Up")
        ax.plot(stock1_data["date"], stock1_data["Bollinger_down"], alpha = 0.3, label="Bollinger Down")
        ax.plot(stock1_data["date"], stock1_data["SMA"], alpha = 0.3, label="SMA")
        ax.legend(loc="upper left")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.fill_between(stock1_data["date"], stock1_data["Bollinger_up"], stock1_data["Bollinger_down"], color = "grey", alpha = 0.1)
    return fig
    # When you plot the figure, be shure to Open the Date Frame into the Shiny App at least 2 MONTHS, 
    # Otherwise only Closing Prices line will show

def create_stock_table(stock1_data, stock2_data):
    # This function create_stock_table concatenates the two pandas dataframes along the columns(axis=1)
    #  using the pd.concat() method from the pandas library
    data = pd.concat([stock1_data, stock2_data], axis=1)
    return data    

# App UI
# The app_ui variable defines the user interface of the Shiny web application using the shiny library.
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.tags.style("#container {display: flex, flex-direction: column; align-items: center;}"),
            ui.tags.div(
                ui.row(
                    ui.column(12, ui.panel_title("Welcome to BarKan App"))
                ),
                ui.panel_sidebar(
                    ui.row(
                        ui.column(10, ui.input_select(id="ticker1", label="Ticker 1:", choices= tickers)),
                        ui.column(10, ui.input_select(id="ticker2", label="Ticker 2:", choices=tickers)),
                        ui.column(10, ui.input_date(id="start_date", label="Start Date:", value=time_start)),
                        ui.column(10, ui.input_date(id="end_date", label= "End Date", value = time_end)),
                        ui.column(10, ui.input_select(id="plot_type", label= "Plot Type:", choices={"line": "Line", "stackplot": "Stackplot", "bar": "Bar","bollinger": "Bollinger"}))
                    )
                )
            )
        ),
        ui.panel_main(
            ui.navset_tab(
                ui.nav("Plots",
                    ui.row(
                        ui.column(12, ui.output_plot("Display"))
                    )
                ),
                ui.nav("Stock Table",
                    ui.row(
                        ui.column(12, ui.output_table("table_data"))
                    )
                )
            )
        )
    )
)


# Server logic
def server(input, output, session):
    # The server() function is where the logic for handling the inputs and outputs for the UI of the Shiny web application is defined.
    # reactive.Calc is a decorator from the shiny library that allows you to define a reactive computation.
    # the data() function is defined as a reactive computation using the @reactive.Calc decorator.
    # This allows the data to be recalculated each time one of the inputs changes and also pass data between different functions.
    @reactive.Calc
    def data():
        return get_stock_data(input.ticker1(), input.ticker2(), input.start_date(), input.end_date())

    # then two output render functions, Display() and table_data(), which are using the @output decorator.
    # render is a module in the shiny library that contains decorators for creating output elements in a Shiny application.
    # The Display() function uses the render.plot decorator to output the result of the plot_stock_data function.
    # Chart    
    @output
    @render.plot
    def Display():
        stock1_data, stock2_data = data()
        if stock1_data is None or stock2_data is None:
            return ui.tags.div("Error: Could not retrieve data from API. Please check that the tickers are valid and that you have a valid API key.")
        return plot_stock_data(stock1_data, stock2_data, input.ticker1(), input.ticker2(), input.plot_type())
    # Table 
    # The table_data() function uses the render.table decorator to output the result of the create_stock_table function .
    @output
    @render.table
    def table_data():
        stock1_data, stock2_data = data()
        if stock1_data is None or stock2_data is None:
            return ui.tags.div("Error: Could not retrieve data from API. Please check that the tickers are valid and that you have a valid API key.")
        return create_stock_table(stock1_data, stock2_data)
    Display = Display
    table_data = table_data

#Connect everything
#if __name__ == '__main__':
app = App(ui=app_ui, server=server)
    #app.run()
