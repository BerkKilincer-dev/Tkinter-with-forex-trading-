````markdown
# 📈 Real-Time Trading Simulation Dashboard

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=flat)
![Matplotlib](https://img.shields.io/badge/Data-Matplotlib-orange?style=flat&logo=matplotlib)

A desktop application built with **Python** that simulates real-time trading data visualization. This tool allows traders and developers to monitor currency pairs, analyze price trends with Moving Averages, and view fundamental news feeds in a dynamic GUI environment.

![Dashboard Screenshot](screenshot.png)
*(Please add a screenshot of the application here named 'screenshot.png')*

## 🌟 Features

* **Real-Time Simulation:** mimics live market data updates using dynamic plotting.
* **Dual Charting:**
    * **Line Chart:** For clear trend visualization.
    * **Scatter Plot:** For spotting individual data points and volatility.
* **Technical Indicators:**
    * **MA50 (Moving Average 50):** Short-term trend analysis.
    * **MA200 (Moving Average 200):** Long-term trend analysis.
* **Fundamental Analysis:** Integrated text-based news reader for currency pairs.
* **Auto-Data Generation:** If CSV data files are missing, the system automatically generates synthetic market data for testing purposes.
* **Interactive UI:** Treeview selection, tabbed charts, and real-time buy/sell price updates.

## 🛠️ Built With

* **[Python](https://www.python.org/)** - Core programming language.
* **[Tkinter](https://docs.python.org/3/library/tkinter.html)** - Standard GUI toolkit for Python.
* **[Matplotlib](https://matplotlib.org/)** - Comprehensive library for creating static, animated, and interactive visualizations.
* **[Pandas](https://pandas.pydata.org/)** & **[NumPy](https://numpy.org/)** - Powerful data analysis and manipulation tools.

## 📂 Project Structure

```text
Trading-Dashboard/
│
├── main.py              # The main application entry point
├── eurusd.csv           # Historical data for EUR/USD (Optional)
├── eurgbr.csv           # Historical data for EUR/GBR (Optional)
├── news_EURUSD.txt      # News feed text for EUR/USD
├── news_EURGBR.txt      # News feed text for EUR/GBR
├── README.md            # Project documentation
└── requirements.txt     # List of python dependencies
````

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Ensure you have Python installed on your system.

```bash
python --version
```

### Installation

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/yourusername/trading-dashboard.git](https://github.com/yourusername/trading-dashboard.git)
    cd trading-dashboard
    ```

2.  **Install required packages**
    It's recommended to create a virtual environment first.

    ```bash
    pip install pandas numpy matplotlib
    ```

3.  **Run the Application**

    ```bash
    python main.py
    ```

## 🎮 Usage

1.  **Select a Pair:** Double-click or select a currency pair (e.g., **EUR/USD**) from the list on the left.
2.  **Load Data:** Click the **"Open Trading"** button to load historical data and news.
3.  **Choose Strategy:** Select a Moving Average period (**m1** for 50 periods, **m2** for 200 periods) via the radio buttons.
4.  **Start Simulation:** Click **"Start Trading"** to begin the real-time price simulation.
5.  **Analyze:** Switch between "Line" and "Scatter" tabs to view different chart types.

## 📊 Data Format (Optional)

You can use your own dataset by placing CSV files in the root directory. The file name should match the pair (e.g., `eurusd.csv`) and must contain a `close1` column.

```csv
date,close1
2023-01-01,1.0650
2023-01-02,1.0680
...
```

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

-----

*Developed by [Berk Kılınçer]*

```
```
