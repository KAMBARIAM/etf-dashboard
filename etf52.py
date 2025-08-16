# fetch_etfs.py
import yfinance as yf
import json

# List of Indian ETFs on NSE
# Format: [Ticker, Full Name]
etfs_data = [
    # Nifty Indices
    ["NIFTYBEES.NS", "Nippon India ETF Nifty 50"],
    ["JUNIORBEES.NS", "Nippon India ETF Nifty Next 50"],
    ["BANKBEES.NS", "Nippon India ETF Bank BeES"],
    ["ITBEES.NS", "Nippon India ETF Nifty IT"],
    ["PSUBANKBEES.NS", "Nippon India ETF PSU Bank BeES"],
    ["CPSEETF.NS", "CPSE ETF"],
    ["MON100.NS", "Motilal Oswal NASDAQ 100 ETF"],
    
    # Gold and Silver ETFs
    ["GOLDBEES.NS", "Nippon India ETF Gold BeES"],
    ["SILVERBEES.NS", "Nippon India ETF Silver"],
    ["HDFCMFGETF.NS", "HDFC Gold ETF"],
    ["GOLDSHARE.NS", "Reliance ETF Gold"],
    
    # Sectoral and Thematic ETFs
    ["ICICICONSUMP.NS", "ICICI Prudential Consumption ETF"],
    ["ICICIAUTOV.NS", "ICICI Prudential Auto ETF"],
    ["ICICIBANKNIFTY.NS", "ICICI Prudential Bank ETF"],
    ["ICICIFIN.NS", "ICICI Prudential FMCG ETF"],
    ["ICICILOVOL.NS", "ICICI Prudential Low Vol 30 ETF"],
    ["ICICIMCAP250.NS", "ICICI Prudential Midcap 250 ETF"],
    ["ICICINIFTY.NS", "ICICI Prudential Nifty 50 ETF"],
    ["ICICINV20.NS", "ICICI Prudential NV20 ETF"],
    ["ICICINXT50.NS", "ICICI Prudential Nifty 100 ETF"],
    ["ICICINXT50.NS", "ICICI Prudential Nifty Next 50 ETF"],
    ["ICICIPHARMA.NS", "ICICI Prudential Pharma ETF"],
    ["ICICISENSX.NS", "ICICI Prudential Sensex ETF"],
    ["ICICITECH.NS", "ICICI Prudential IT ETF"],
    
    # Other Major ETFs
    ["KOTAKNIFTY.NS", "Kotak Nifty 50 ETF"],
    ["HDFCNIFTY.NS", "HDFC NIFTY50 ETF"],
    ["SBINIFTY.NS", "SBI Nifty 50 ETF"],
    ["UTINIFTETF.NS", "UTI Nifty 50 ETF"],
    ["MOM100.NS", "Mirae Asset NYSE FANG+ ETF"],
    ["MIRAEEMG.NS", "Mirae Asset NYSE FANG+ ETF"],
    ["SETFNIF50.NS", "SBI Nifty 50 ETF"],
]

# Extract just the ticker symbols for yfinance
etfs = [etf[0] for etf in etfs_data]

output = []

for symbol in etfs:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1y")
        
        if hist.empty:
            print(f"No data available for {symbol}, skipping...")
            continue
            
        # Use iloc to avoid deprecation warning
        current_price = hist["Close"].iloc[-1]
        low_52w = hist["Low"].min()
        high_52w = hist["High"].max()

        change_from_low = ((current_price - low_52w) / low_52w) * 100
        change_from_high = ((current_price - high_52w) / high_52w) * 100
        
    except Exception as e:
        print(f"Error processing {symbol}: {str(e)}")
        continue

    output.append({
        "symbol": symbol,
        "name": ticker.info.get("shortName", ""),
        "current_price": round(current_price, 2),
        "low_52w": round(low_52w, 2),
        "high_52w": round(high_52w, 2),
        "change_from_low_pct": round(change_from_low, 2),
        "change_from_high_pct": round(change_from_high, 2),
    })

# Save to JSON file
with open("data.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ data.json updated")
