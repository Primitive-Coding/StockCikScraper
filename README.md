# StockCik Scraper

- Get the CIK for a company.

---

### Setup

1. Clone git repository: `https://github.com/PrimalFinance/StockCikScraper.git`
1. Configure the "config.json" file.

```
    {
        "chrome_driver_path": "D:\\PATH TO CHROME DRIVER\\chromedriver.exe",
        "data_export_path": "D:\\TEST\\CikData\\cik_data.csv"
    }

```

3. Install the projects requirements with `pip install -r requirements.txt`

---

### Instructions

- Create a class instance.

```
    s = StockCik()
```

###### CIK Data

```
    cik = s.get_cik("AAPL")

    # Output
    0000320193
```

###### **NOTE**

- If the CIK does not exist in the local files, it will be scraped and stored in `cik_data.csv` upon execution of `s.get_cik(ticker)`.

```
    ~cik_data.csv

           CIK       Name Exchange     SIC Business Incorporated  IRS
Ticker
RKLB    0001819994  Rocket Lab USA, Inc.       N\A  3760.0       CA           DE  N\A
AAPL    0000320193            Apple Inc.       N\A  3571.0       CA           CA  N\A

```

```
    cik = s.get_cik("AMZN")
```

```
    ~cik_data.csv

          CIK       Name Exchange     SIC Business Incorporated  IRS
Ticker
RKLB    0001819994  Rocket Lab USA, Inc.       N\A  3760.0       CA           DE  N\A
AAPL    0000320193            Apple Inc.       N\A  3571.0       CA           CA  N\A
AMZN    0001018724        AMAZON COM INC       N\A  5961.0       WA           DE  N\A <--------------------
```

### Local Data Overview

- Ticker: Ticker symbol of the company
- CIK: Central Index Key associated with the company.
- Name: Name of the company.
- Exchange: Exchange the stock is traded on. (Note: This feature is prone to failure)
- SIC: Standard Industrial Classification associated with the company.
- Business: Location the business is headquartered.
- Incorporated: Location the business was incorporated.
- IRS: Internal Revenue Service code associated with the stock.

```
 ~cik_data.csv

          CIK                                      Name Exchange     SIC Business Incorporated          IRS
Ticker
A       0001090872                  Agilent Technologies Inc     NYSE  3825       CA           DE  770518772
AA      0000004281                                 Alcoa Inc     NYSE  3350       PA           PA  250317820
AAACU   0001332552          Asia Automotive Acquisition Corp      NaN  6770       DE           DE  203022522
AABB    0001287145                        Asia Broadband Inc      OTC  8200       GA           NV  721569126
AABC    0001024015                Access Anytime Bancorp Inc      NaN  6035       NM           DE  850444597
...            ...                                       ...      ...     ...      ...          ...          ...
ZVXI    0000827056                   Zevex International Inc      NaN  3845       UT           NV  870462807
ZYNX    0000846475                                 Zynex Inc      NaN  3845       CO           NV  870403828
ZYTC    0001406796                                 Zyto Corp      NaN  3841       UT          NaN  205534033
ZZ      0000748015                                Sealy Corp     NYSE  2510       WA           DE  363284147
ZZGQI   0000827830  Wilder Richman Historic Properties II LP      NaN  6513       CT           DE  133481443
```
