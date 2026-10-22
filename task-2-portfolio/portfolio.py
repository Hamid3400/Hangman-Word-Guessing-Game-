import csv
import random

# ---------- 1. Load Valid Tickers from CSV ----------
def load_valid_tickers(csv_filepath):
    valid_tickers = set()
    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row.get('Symbol')
                if symbol:
                    valid_tickers.add(symbol.upper().strip())
        print(f"✅ Loaded {len(valid_tickers)} valid S&P 500 tickers.")
        return valid_tickers
    except FileNotFoundError:
        print(f"⚠️  Warning: '{csv_filepath}' not found. Ticker validation disabled.")
        return None


# ---------- 2. Simulate "Live" Price ----------
# Deterministic pseudo-random price based on ticker so results are stable per run
def get_live_price(ticker, buy_price):
    # Seed the RNG with the ticker + a fixed "market date" so it's reproducible
    seed = sum(ord(c) for c in ticker) + 20250101
    rng = random.Random(seed)

    # Simulate a market move of -20% to +25% from the buy price
    drift = rng.uniform(-0.20, 0.25)
    simulated_price = buy_price * (1 + drift)

    return round(simulated_price, 2)


# ---------- 3. Portfolio Class ----------
class Portfolio:
    def __init__(self):
        self.holdings = {}

    def add_holding(self, ticker, shares, buy_price):
        ticker = ticker.upper()
        if ticker in self.holdings:
            current_shares = self.holdings[ticker]['shares']
            current_cost = self.holdings[ticker]['buy_price'] * current_shares
            new_cost = buy_price * shares
            total_shares = current_shares + shares
            self.holdings[ticker]['shares'] = total_shares
            self.holdings[ticker]['buy_price'] = (current_cost + new_cost) / total_shares
        else:
            self.holdings[ticker] = {'shares': shares, 'buy_price': buy_price}

    def calculate_performance(self):
        total_invested = 0.0
        total_current_value = 0.0
        report_data = []

        for ticker, data in self.holdings.items():
            shares = data['shares']
            buy_price = data['buy_price']

            current_price = get_live_price(ticker, buy_price)

            invested = shares * buy_price
            current_value = shares * current_price
            gain_loss = current_value - invested
            percent_change = (gain_loss / invested) * 100 if invested > 0 else 0

            total_invested += invested
            total_current_value += current_value

            report_data.append({
                'Ticker': ticker,
                'Shares': shares,
                'Buy Price': round(buy_price, 2),
                'Current Price': round(current_price, 2),
                'Invested': round(invested, 2),
                'Current Value': round(current_value, 2),
                'Gain/Loss': round(gain_loss, 2),
                'Return (%)': round(percent_change, 2)
            })

        return report_data, total_invested, total_current_value


# ---------- 4. Save to CSV ----------
def save_summary_to_csv(report_data, total_invested, total_current_value, filename="portfolio_summary.csv"):
    if not report_data:
        return

    fieldnames = ['Ticker', 'Shares', 'Buy Price', 'Current Price',
                  'Invested', 'Current Value', 'Gain/Loss', 'Return (%)']

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)

        total_gain = total_current_value - total_invested
        total_percent = (total_gain / total_invested) * 100 if total_invested > 0 else 0

        writer.writerow({
            'Ticker': 'TOTAL', 'Shares': '', 'Buy Price': '', 'Current Price': '',
            'Invested': round(total_invested, 2),
            'Current Value': round(total_current_value, 2),
            'Gain/Loss': round(total_gain, 2),
            'Return (%)': round(total_percent, 2)
        })
    print(f"\n✅ Summary saved to '{filename}'")


# ---------- 5. Main Program ----------
def main():
    print("=" * 70)
    print(" 📈 Stock Portfolio Performance Tracker")
    print("=" * 70)

    csv_path = "S&P 500 Ticker Dataset (.CSV).csv"
    valid_tickers = load_valid_tickers(csv_path)

    portfolio = Portfolio()

    while True:
        print("\n--- Add a Stock (type 'done' to finish) ---")
        ticker = input("Ticker symbol: ").strip().upper()

        if ticker == 'DONE':
            break

        if valid_tickers and ticker not in valid_tickers:
            print(f"❌ '{ticker}' is not in the S&P 500 list. Please try again.")
            continue

        try:
            shares = float(input(f"Shares of {ticker}: "))
            buy_price = float(input(f"Buy price per share ($): "))
            portfolio.add_holding(ticker, shares, buy_price)
            print(f"✅ Added {shares} shares of {ticker} @ ${buy_price:.2f}")
        except ValueError:
            print("⚠️  Invalid number. Please enter digits only.")

    if portfolio.holdings:
        report_data, total_invested, total_current_value = portfolio.calculate_performance()

        print("\n" + "=" * 78)
        print(f"{'Ticker':<8} | {'Shares':<8} | {'Buy $':<8} | {'Curr $':<8} | {'Gain/Loss':<10} | {'Return':<8}")
        print("-" * 78)
        for row in report_data:
            print(f"{row['Ticker']:<8} | {row['Shares']:<8.0f} | {row['Buy Price']:<8.2f} | "
                  f"{row['Current Price']:<8.2f} | {row['Gain/Loss']:<10.2f} | {row['Return (%)']:<7.2f}%")

        print("-" * 78)
        total_gain = total_current_value - total_invested
        total_percent = (total_gain / total_invested) * 100 if total_invested > 0 else 0
        print(f"TOTAL INVESTED: ${total_invested:.2f}")
        print(f"CURRENT VALUE : ${total_current_value:.2f}")
        print(f"NET GAIN/LOSS : ${total_gain:.2f} ({total_percent:.2f}%)")

        save_summary_to_csv(report_data, total_invested, total_current_value)
    else:
        print("\nNo stocks added. Exiting.")


if __name__ == "__main__":
    main()