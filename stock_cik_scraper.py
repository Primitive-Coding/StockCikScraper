import os
import json
import requests
import pandas as pd


# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class StockCik:
    def __init__(self) -> None:
        self.browser = None
        self.chrome_driver_path = self._get_chrome_driver_path()
        self.cik_file = self._get_data_export_path()
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-gpu")
        dir_path = os.path.dirname(self.cik_file)
        os.makedirs(dir_path, exist_ok=True)

    """-----------------------------------"""

    def _get_data_export_path(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        return data["data_export_path"]

    """-----------------------------------"""

    def _get_chrome_driver_path(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        return data["chrome_driver_path"]

    """-----------------------------------"""

    def get_cik(self, ticker: str):
        try:
            df = pd.read_csv(self.cik_file, sep="|")
            df.set_index("Ticker", inplace=True)
            df = self._formate_cik_df(df)

            try:
                cik = df.loc[ticker, "CIK"]
                return cik
            except KeyError:
                df = self._fill_df(ticker, df)
                df.to_csv(self.cik_file, sep="|")
                cik = df.loc[ticker, "CIK"]
                return cik
        except FileNotFoundError:

            cols = [
                "Ticker",
                "CIK",
                "Name",
                "Exchange",
                "SIC",
                "Business",
                "Incorporated",
                "IRS",
            ]
            df = pd.DataFrame(columns=cols)
            df.set_index("Ticker", inplace=True)
            df = self._fill_df(ticker, df)
            cik = df.loc[ticker, "CIK"]
            cik = str(cik).zfill(
                10
            )  # Add leading zero prefix. The total string length should *ONLY EVER* be 10 characters long.
            df.loc[ticker, "CIK"] = cik
            df.to_csv(self.cik_file, sep="|")
            return cik

    """-----------------------------------"""

    def _formate_cik_df(self, df):
        col = "CIK"
        df["CIK"] = df[col].astype(str)
        df[col] = df[col].apply(lambda x: x.zfill(10))
        return df

    """-----------------------------------"""

    def _fill_df(self, ticker: str, df: pd.DataFrame) -> pd.DataFrame:
        data = self._scrape_sec_website(ticker)
        df.loc[ticker.upper(), "CIK"] = data["CIK"]
        df.loc[ticker.upper(), "Name"] = data["Name"]
        df.loc[ticker.upper(), "Exchange"] = "N\\A"
        df.loc[ticker.upper(), "SIC"] = data["SIC"]
        df.loc[ticker.upper(), "Business"] = data["State_Location"]
        df.loc[ticker.upper(), "Incorporated"] = data["State_Incorporated"]
        df.loc[ticker.upper(), "IRS"] = "N\\A"

        df["CIK"] = df["CIK"].astype("str")
        df["SIC"] = df["SIC"].astype("str")
        return df

    """-----------------------------------"""

    def get_filing_history(self, ticker: str):
        cik = self.get_cik(ticker)
        print(f"CIK: {cik}")
        query = f"https://data.sec.gov/submissions/CIK{cik}.json"
        print(f"Query: {query}")
        response = requests.get(query)
        print(f"Response: {response.status_code}")
        data = response.content

    """-----------------------------------"""

    def _scrape_sec_website(self, ticker: str):
        annual_filings = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker.lower()}&type=10-k&dateb=&owner=include&count=40&search_text="

        self._create_browser(annual_filings)

        company_name_xpath = "/html/body/div[4]/div[1]/div[3]/span"
        cik_xpath = "/html/body/div[4]/div[1]/div[3]/span/a"
        sic_xpath = "/html/body/div[4]/div[1]/div[3]/p/a[1]"
        state_location_xpath = "/html/body/div[4]/div[1]/div[3]/p/a[2]"
        state_inc_xpath = "/html/body/div[4]/div[1]/div[3]/p/strong"

        company_name = self._read_data(company_name_xpath)
        # Logic to clean 'company_name'
        company_name = company_name.split(":")[0]
        company_name = company_name[:-4]

        cik = self._read_data(cik_xpath)
        # Logic to clean 'cik'
        cik = cik.split(" ")[0]
        sic = str(self._read_data(sic_xpath))
        state_location = self._read_data(state_location_xpath)
        state_inc = self._read_data(state_inc_xpath)

        self._clean_close()
        return {
            "Name": company_name,
            "CIK": cik,
            "SIC": sic,
            "State_Location": state_location,
            "State_Incorporated": state_inc,
        }

    """-----------------------------------"""

    def _create_browser(self, url=None):
        """
        :param url: The website to visit.
        :return: None
        """
        service = Service(executable_path=self.chrome_driver_path)
        self.browser = webdriver.Chrome(service=service, options=self.chrome_options)
        # Default browser route
        if url == None:
            self.browser.get(url=self.sec_annual_url)
        # External browser route
        else:
            self.browser.get(url=url)

    def _clean_close(self) -> None:
        self.browser.close()
        self.browser.quit()

    def _read_data(
        self, xpath: str, wait: bool = False, _wait_time: int = 5, tag: str = ""
    ) -> str:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: (str) Text of the element.
        """

        if wait:
            try:
                data = (
                    WebDriverWait(self.browser, _wait_time)
                    .until(EC.presence_of_element_located((By.XPATH, xpath)))
                    .text
                )
            except TimeoutException:
                print(f"[Failed Xpath] {xpath}")
                if tag != "":
                    print(f"[Tag]: {tag}")
                raise NoSuchElementException("Element not found")
            except NoSuchElementException:
                print(f"[Failed Xpath] {xpath}")
                return "N\A"
        else:
            try:
                data = self.browser.find_element("xpath", xpath).text
            except NoSuchElementException:
                data = "N\A"
        # Return the text of the element found.
        return data

    def _view_data(self):
        df = pd.read_csv(self.cik_file, sep="|")
        df = self._formate_cik_df(df)
        df.set_index("Ticker", inplace=True)
        df["SIC"] = df["SIC"].astype(str)
        print(f"{df}")
        return df


if __name__ == "__main__":
    ticker = "AMZN"
    s = StockCik()
    cik = s.get_cik(ticker)
