import requests
from bs4 import BeautifulSoup
import csv
import time


class ZooplaScrapper:
    results = []
    def fetch(self, url):
        print("HTTP GET REQUEST : %s" % url)
        res = requests.get(url)
        print("Getting Request ... \nStatus Code : %s" %res.status_code)
        return res
    
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        cards = content.findAll("div", {"class": "listing-results-wrapper"})
        for card in cards:
            self.results.append({
                "title" : card.find("a", {"style": "text-decoration:underline;"}).text,
                "address" : card.find("a", {"class": "listing-results-address"}).text,
                "description" : card.find("p").text.strip(),
                "price": card.find("a", {"class": "listing-results-price"}).text.strip().split(' ')[0].strip(),
                "phone": card.find("span", {"class": "agent_phone"}).find("span").text,
                "image": card.find("a", {"class": "photo-hover"}).find('img')['data-src']
            })     

    def to_csv(self):

        with open('zoopla.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print("Stored CSV file to 'zoopla.csv' ")

    
    def run(self):
        base_url = "https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&q=london&search_source=home&radius=0&pn="
        for page in range(1, 5):
            url = base_url + str(page)
            res = self.fetch(url)   
            self.parse(res.text)
            time.sleep(2)
                
        self.to_csv()
            
if __name__ == "__main__":
    scrapper = ZooplaScrapper()
    scrapper.run()
    
    
    
        