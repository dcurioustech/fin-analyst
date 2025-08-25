import yfinance as yf
import pandas as pd
import sys # Used for flushing output to ensure prints appear immediately

# --- Configuration ---
# Set pandas options to display data cleanly without truncation
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# --- Helper Functions ---
def format_large_number(num):
    """Formats a large number into a more readable string (e.g., 1.25 T, 350.50 B, 15.75 M)."""
    if num is None or not isinstance(num, (int, float)):
        return "N/A"
    if abs(num) > 1e12:
        return f"{num / 1e12:.2f} T"
    elif abs(num) > 1e9:
        return f"{num / 1e9:.2f} B"
    elif abs(num) > 1e6:
        return f"{num / 1e6:.2f} M"
    else:
        return f"{num:,.2f}"

def plot_text_bar(label, value, max_value):
    """Creates a simple text-based horizontal bar chart."""
    if value is None or max_value is None or max_value == 0:
        bar_str = "N/A"
        print(f"{label:<15} | {bar_str}")
        return
        
    bar_length = 40  # Max length of the bar in characters
    
    # Handle negative values by plotting on a scale from min to max
    scaled_value = float(value)
    
    # Calculate the length of the bar
    try:
        bar_fill_length = int((scaled_value / max_value) * bar_length)
    except (ValueError, TypeError):
        bar_fill_length = 0

    # Create the bar string
    bar = '█' * bar_fill_length
    
    # Format the value for display
    if isinstance(value, float):
        value_str = f"{value:.2f}"
    else:
        value_str = str(value)

    print(f"{label:<15} | {bar} {value_str}")

# --- Core Analysis Functions ---
def get_company_profile(ticker_info):
    """Displays the core company profile."""
    # (This function is the same as before)
    print("\n--- Company Profile ---")
    print(f"Name: {ticker_info.get('longName', 'N/A')}")
    print(f"Sector: {ticker_info.get('sector', 'N/A')}")
    print(f"Industry: {ticker_info.get('industry', 'N/A')}")
    print(f"Country: {ticker_info.get('country', 'N/A')}")
    print(f"Website: {ticker_info.get('website', 'N/A')}")
    print("\nBusiness Summary:")
    print(ticker_info.get('longBusinessSummary', 'No summary available.'))
    print("-" * 25)

def get_key_metrics(ticker_info):
    """Displays key financial ratios and metrics."""
    # (This function is the same as before)
    print("\n--- Key Financial Metrics ---")
    print("Valuation:")
    print(f"  Market Cap: {format_large_number(ticker_info.get('marketCap'))}")
    print(f"  Enterprise Value: {format_large_number(ticker_info.get('enterpriseValue'))}")
    print(f"  Trailing P/E: {ticker_info.get('trailingPE', 'N/A'):.2f}" if ticker_info.get('trailingPE') else "  Trailing P/E: N/A")
    print(f"  Forward P/E: {ticker_info.get('forwardPE', 'N/A'):.2f}" if ticker_info.get('forwardPE') else "  Forward P/E: N/A")
    print(f"  Price to Sales (TTM): {ticker_info.get('priceToSalesTrailing12Months', 'N/A'):.2f}" if ticker_info.get('priceToSalesTrailing12Months') else "  Price to Sales (TTM): N/A")
    print(f"  Price to Book: {ticker_info.get('priceToBook', 'N/A'):.2f}" if ticker_info.get('priceToBook') else "  Price to Book: N/A")
    print("\nProfitability & Management:")
    print(f"  Profit Margins: {ticker_info.get('profitMargins', 0) * 100:.2f}%")
    print(f"  Return on Equity (ROE): {ticker_info.get('returnOnEquity', 0) * 100:.2f}%")
    print(f"  Return on Assets (ROA): {ticker_info.get('returnOnAssets', 0) * 100:.2f}%")
    print("\nStock Price Info:")
    print(f"  Current Price: {ticker_info.get('currentPrice', 'N/A')}")
    print(f"  52-Week Range: {ticker_info.get('fiftyTwoWeekLow', 'N/A')} - {ticker_info.get('fiftyTwoWeekHigh', 'N/A')}")
    print(f"  Beta: {ticker_info.get('beta', 'N/A')}")
    print("\nDividends:")
    print(f"  Dividend Yield: {ticker_info.get('dividendYield', 0) * 100:.2f}%")
    print(f"  Payout Ratio: {ticker_info.get('payoutRatio', 0) * 100:.2f}%")
    print("-" * 25)

def display_financial_statement(statement_func, name):
    """Generic function to fetch and display a financial statement."""
    # (This function is the same as before)
    try:
        statement = statement_func()
        if not statement.empty:
            print(f"\n--- {name} (Annual) ---")
            # Format all numeric columns to be more readable
            formatted_statement = statement.applymap(lambda x: format_large_number(x) if isinstance(x, (int, float)) else x)
            print(formatted_statement)
            print("-" * (len(name) + 12))
        else:
            print(f"No {name} data available.")
    except Exception as e:
        print(f"Could not retrieve {name}: {e}")

# --- NEW: Peer Comparison Function ---
def perform_peer_comparison(main_ticker_symbol):
    """Gathers data for peer comparison and visualizes it."""
    main_ticker = yf.Ticker(main_ticker_symbol)
    
    # Try to find peers automatically from recommendations
    suggested_peers = []
    try:
        recommendations = main_ticker.recommendations_summary
        if 'recommended_tickers' in recommendations:
           suggested_peers = [item['symbol'] for item in recommendations['recommended_tickers']][:4] # Get up to 4
    except:
        pass # Ignore if it fails
    
    print("\n--- Peer Comparison ---")
    if suggested_peers:
        print(f"Suggested peers from Yahoo Finance: {', '.join(suggested_peers)}")
    
    peer_input = input("Enter peer tickers separated by spaces (or press Enter to use suggestions): ").upper()
    
    if peer_input.strip():
        peers = peer_input.strip().split()
    elif suggested_peers:
        peers = suggested_peers
    else:
        print("No peers provided. Returning to main menu.")
        return

    all_tickers = [main_ticker_symbol] + peers
    peer_data = []

    print("Fetching data for comparison...")
    
    # Define the metrics we want to compare
    metrics_to_compare = {
        'marketCap': 'Market Cap',
        'trailingPE': 'P/E Ratio',
        'priceToSalesTrailing12Months': 'P/S Ratio',
        'priceToBook': 'P/B Ratio',
        'profitMargins': 'Profit Margin (%)',
        'returnOnEquity': 'ROE (%)'
    }

    for ticker_symbol in all_tickers:
        try:
            print(f"  Fetching {ticker_symbol}...")
            sys.stdout.flush() # Ensure print appears before data fetch
            ticker_info = yf.Ticker(ticker_symbol).info
            
            data_point = {'Ticker': ticker_symbol}
            for key, name in metrics_to_compare.items():
                value = ticker_info.get(key)
                # Convert percentage metrics
                if '%' in name and value is not None:
                    value *= 100
                data_point[name] = value if value is not None else 'N/A'
            
            peer_data.append(data_point)
        except Exception:
            print(f"  Could not fetch data for {ticker_symbol}. Skipping.")

    if not peer_data:
        print("Could not gather any data for comparison.")
        return

    # --- Display Data Table ---
    df = pd.DataFrame(peer_data)
    df.set_index('Ticker', inplace=True)
    
    print("\n--- Comparison Table ---")
    print(df.round(2)) # Display data rounded to 2 decimal places

    # --- Display Visuals ---
    print("\n--- Visual Comparison ---")
    df_numeric = df.apply(pd.to_numeric, errors='coerce').fillna(0) # Convert to numbers for plotting

    for column in df_numeric.columns:
        print(f"\n-- {column} --")
        # Use the max of the absolute values for scaling to handle negative values properly
        max_val = df_numeric[column].abs().max()
        if pd.isna(max_val): max_val = 0

        for ticker, value in df_numeric[column].items():
            plot_text_bar(ticker, value, max_val)
        print("-" * 25)

# --- Main Chat Bot Loop ---
def chat_bot():
    """Main function to run the analysis chat bot."""
    while True:
        ticker_symbol = input("Enter a stock ticker (e.g., AAPL, GOOGL) or type 'exit' to quit: ").upper()
        if ticker_symbol == 'EXIT':
            break

        try:
            stock = yf.Ticker(ticker_symbol)
            if not stock.info or stock.info.get('regularMarketPrice') is None:
                print(f"Error: Could not find data for ticker '{ticker_symbol}'. Please check the symbol and try again.")
                continue

            print(f"\nSuccessfully fetched data for {stock.info['longName']} ({ticker_symbol}).")
            
            while True:
                print("\nWhat analysis would you like to see?")
                print("1: Company Profile & Summary")
                print("2: Key Financial Metrics & Ratios")
                print("3: Income Statement (Annual)")
                print("4: Balance Sheet (Annual)")
                print("5: Cash Flow Statement (Annual)")
                print("6: Analyst Recommendations")
                print("7: Peer Comparison with Visuals") # New Option
                print("8: Search for a new ticker")
                print("9: Exit")

                choice = input("Please enter your choice (1-9): ")

                if choice == '1':
                    get_company_profile(stock.info)
                elif choice == '2':
                    get_key_metrics(stock.info)
                elif choice == '3':
                    display_financial_statement(stock.financials, "Income Statement")
                elif choice == '4':
                    display_financial_statement(stock.balance_sheet, "Balance Sheet")
                elif choice == '5':
                    display_financial_statement(stock.cashflow, "Cash Flow Statement")
                elif choice == '6':
                    recommendations = stock.recommendations
                    if recommendations is not None and not recommendations.empty:
                         print("\n--- Analyst Recommendations (Last 30) ---")
                         print(recommendations.tail(30))
                    else:
                        print("No analyst recommendations available.")
                elif choice == '7':
                    perform_peer_comparison(ticker_symbol) # Call the new function
                elif choice == '8':
                    break
                elif choice == '9':
                    print("Exiting analysis bot. Goodbye!")
                    return
                else:
                    print("Invalid choice. Please enter a number between 1 and 9.")
        except Exception as e:
            print(f"An error occurred: {e}. Please check the ticker symbol and your internet connection.")

if __name__ == "__main__":
    chat_bot()
    