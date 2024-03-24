import requests
import re
import json
from bs4 import BeautifulSoup
import json
import os

amazon_prod_list = []
flipkart_prod_list = []

class WebPageInfoCollectAndParser:
    def __init__(self):
            self.amazon_data = self.get_amazon_data()
            self.flipkart_data = self.get_flipkart_data()
            self.amazon_url_list = [entry['url'] for entry in self.amazon_data if entry['site'] == 'amazon']
            self.flipkart_url_list = [entry['url'] for entry in self.flipkart_data if entry['site'] == 'flipkart']
            self.amazon_p_ID = [entry['prod_id'] for entry in self.amazon_data if entry['site'] == 'amazon']
            self.flipkart_p_ID = [entry['prod_id'] for entry in self.flipkart_data if entry['site'] == 'flipkart']

    def get_amazon_data(self):
        amazon_host = "http://localhost:3000/api/v1/ext/amazonproducts/url"
        amazon_response = requests.get(amazon_host)
        amazon_data = json.loads(amazon_response.text)
        return amazon_data

    def get_flipkart_data(self):
        flipkart_host = "http://localhost:3000/api/v1/ext/flipkartproducts/url"
        flipkart_response = requests.get(flipkart_host)
        flipkart_data = json.loads(flipkart_response.text)
        return flipkart_data

    def proxy_setter(self):
        with open(f"py_scripts\\Valid_Proxy_List.txt", "r", encoding='utf-8') as file:
            proxies_list =  file.read().split("\n")
            for p in proxies_list:
                proxy = p
                yield proxy

    # def search_amazon_product(self):
    #     fp = "https://www.pricebefore.com/search"
    #     proxy = next(self.proxy_setter())
    #     for i in range(len(self.amazon_url_list)):
    #         q = self.amazon_url_list[i]
    #         payload = {'q': q}
    #         r = requests.get(fp, params=payload, timeout=10, proxies={'http': f"http://{proxy}", 'https': f"https://{proxy}"})
    #         html = r.text
    #         product_id = self.amazon_p_ID[i]
    #         site = "amazon"
    #     return html, product_id, site
    

    def get_web_page_parser(self, html, Product_ID, site):
        soup = BeautifulSoup(html, "lxml")
        find_script = soup.findAll("script", src=None, type=None, string=re.compile("var data =(.+?);\n"))
        pattern = "var data =(.+?);\n"
        if find_script:
            json_html = re.findall(pattern, find_script[0].text)
            if json_html:
                json_data = json.loads(''.join(json_html))
                if site == "amazon":
                    if site == "amazon":
                        global amazon_prod_list
                        amazon_prod_list.append(Product_ID)
                    elif site == "flipkart":
                        global flipkart_prod_list
                        flipkart_prod_list.append(Product_ID)
                json_data["site"] = site
                json_data["prod_id"] = Product_ID
                json_file = f"public\\temp\\price_hist_data\\{Product_ID}.json"
                json_str = json.dumps(json_data, indent=4)
                open(json_file, "w").write(json_str)
            else:
                print("No data found")
        else:
            print("No script found")

    def search_flipkart_product(self):
        fp = "https://www.pricebefore.com/search"
        proxy = next(self.proxy_setter())
        for i in range(len(self.flipkart_url_list)):
            q = self.flipkart_url_list[i]
            payload = {'q': q}
            r = requests.get(fp, params=payload)
            print(r.url, r.status_code)
            html = r.text
            product_id = self.flipkart_p_ID[i]
            print(r.headers['Content-Type'])
            # Pass the HTML to the get_web_page_parser method
            self.get_web_page_parser(html, product_id, "flipkart")
            print(f"Product searched: {product_id}")

    def search_amazon_product(self):
        fp = "https://www.pricebefore.com/search"
        proxy = next(self.proxy_setter())
        for i in range(len(self.amazon_url_list)):
            q = self.amazon_url_list[i]
            payload = {'q': q}
            r = requests.get(fp, params=payload)
            print(r.url, r.status_code)
            html = r.text
            product_id = self.amazon_p_ID[i]
            print(r.headers['Content-Type'])
            # Pass the HTML to the get_web_page_parser method
            self.get_web_page_parser(html, product_id, "amazon")
            print(f"Product searched: {product_id}")


class server_price_history:

    def post_data(self,jsonfile):
        server_host = "http://localhost:3000/api/v1/historyServer/pricehistory/register"
        json_file_name = f"public\\temp\\price_hist_data\\{jsonfile}"
        with open(json_file_name, "r",encoding= "utf-8") as jsondata:
            body = json.load(jsondata)
        r = requests.post(server_host, json=body)
        # Delete the JSON file
        # os.remove(json_file_name)
        # print(f"Deleted JSON file: {json_file_name}")

    def get_all_data(self,prod_id):
        server_url = "http://localhost:3000/api/v1/historyserver/pricehistory/registetr"
        r = requests.get(server_url)
        body = r.json()
        return body

    def get_data_by_site(self, site ):
        server_url = f"http://localhost:3000/api/v1/historyServer/pricehistory/:{site}"
        r = requests.get(server_url)
        body = r.json()
        return body
    
    def get_data_by_ID(self, prod_id):
        server_url = f"http://localhost:3000/api/v1/historyServer/pricehistory/:{prod_id}"
        r = requests.get(server_url)
        body = r.json()
        return body
    

print(flipkart_prod_list)