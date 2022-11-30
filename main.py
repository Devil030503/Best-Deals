import requests,re,csv
from bs4 import BeautifulSoup


def searchLink(key:str)->list:
    if " " in key:
        search_list = key.split()
        search = "+".join(search_list)
    else:
        search = key
    link = []
    for i in range(1,4):
        link.extend(["https://www.amazon.in/s?k="+search+f"&page={i}","https://www.flipkart.com/search?q="+search+f"&page={i}"])
    return sorted(link)

class AmazonScrapper:
    def get_items_amazon(self,link):
        r = requests.get(link)
        soup = BeautifulSoup(r.content,"html.parser")
        itemList = soup.find_all('div',class_="a-section a-spacing-small a-spacing-top-small")
        itemList = itemList[1:len(itemList)]
        final = []        
        for item in itemList:
            link = item.find('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").get("href")
            name = item.find('span',class_="a-size-medium a-color-base a-text-normal").text.strip()
            try:
                rating_line = item.find('span',class_="a-icon-alt").text.strip()
                rating = re.search(r"[\d.]+\S",rating_line).group()
            except:
                rating = "-"
            price = item.find('span',class_="a-price").text.strip()
            sub = {}
            sub["name"] = name
            sub["rating"] = rating
            sub["price"] = price[:len(price)//2]
            sub["link"] = "https://www.amazon.in/"+str(link)
            final.append(sub)
        return final

class FlipkartScrapper:
    def get_items_flipkart(self,link):
        r = requests.get(link)
        soup = BeautifulSoup(r.content,"html.parser")
        itemList = soup.find_all('div',class_="_1AtVbE col-12-12")
        itemList = itemList[2:len(itemList)-4]
        final = []
        for item in itemList:
            link = item.find('a',class_="_1fQZEK").get("href")
            model = item.find('div',class_="_4rR01T").text.strip()
            try:
                rating = item.find('div',class_="_3LWZlK").text()
            except:
                rating = "-"
            price = item.find('div',class_="_30jeq3 _1_WHN1").text.strip()
            sub = {}
            sub["name"] = model
            sub["rating"] = rating
            sub["price"] = price
            sub["link"] = "https://www.flipkart.com/"+str(link)
            final.append(sub)
        return final

class BestOption(AmazonScrapper,FlipkartScrapper):
    def __init__(self,url_list) -> None:
        final_data = []
        for url in url_list:
            if "amazon" in url:
                self.amazon = self.get_items_amazon(url)
                final_data.extend(self.amazon)
            elif "flipkart" in url:
                self.flipkart = self.get_items_flipkart(url)
                final_data.extend(self.flipkart)
        # print(final_data,"\n",len(final_data))
        sorted_final = sorted(final_data,key=lambda k:k['name'])
        with open("Best Deals.csv","w",encoding="utf-8") as bestdeal:
            w = csv.DictWriter(bestdeal,["name","rating","price","link"])
            w.writeheader()
            for line in sorted_final:
                if search in line['name'].lower():
                    w.writerow(line)
            

if __name__ == "__main__":
    search = input("Enter the item:")
    urls = searchLink(search)
    output = BestOption(urls)