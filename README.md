# EASY FUTURES BUYER BINANCE

<p align="center">
  <img src="https://github.com/SNABUR/EASY-BUYER-BINANCE/assets/136861183/22e82c51-6b2e-48c9-ac57-e70bf8d1a781" alt="Descripción de la imagen">
</p>


This is a project that implements a interface using the Binance API and the Tkinter graphical user interface in Python. It offers functionalities to execute both limit and market orders on the Binance exchange, allowing users to automate buying (LONG) and selling (SHORT) cryptocurrency operations.

## Key Features:

- **Limit and Market Orders**: The  allows both limit and market orders, providing flexibility in executing trades.
  
- **Risk Management**: It incorporates functions to calculate and manage the risk associated with each trade, helping users set loss limits and control their exposure.

- **Graphical User Interface (GUI)**: Utilizing Tkinter, it offers an intuitive and user-friendly interface facilitating user interaction. It displays relevant information about trades and enables easy configurations.

## Requirements:

- Python 3.x
- Packages: `tkinter`, `binance`, `datetime`

## Structure of the `keys.txt` file:

The `keys.txt` file should have the following structure:


BINANCE_API_KEY=Xo5jng5glkdfnglknrglksndgohsinhglknlkzdfnmLd1
BINANCE_API_SECRET_KEY=FbrtbfynjtyklnmlkmxcflnjmUHqzNaT
MAX_AMOUNT=260
MIN_AMOUNT=5
APUESTA=50


Where:

- `BINANCE_API_KEY`: Your Binance API key.
- `BINANCE_API_SECRET_KEY`: Your Binance API secret key.
- `MAX_AMOUNT`: The maximum notional amount.
- `MIN_AMOUNT`: The minimum notional amount.
- `APUESTA`: The amount of money you are willing to lose per trade.

## Usage:

1. Run the code on jupyter or spyder
2. Set up your Binance credentials in the `keys.txt` file.
3. Run the main script `buyer_futures.py`.
4. Use the graphical interface to input your trade parameters and execute them.

Start your operations with this tool!

Donations: 0x563AFB0307CFA1Cb69534c6D5C09Dd57A170EF8b
