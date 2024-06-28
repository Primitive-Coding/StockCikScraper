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
