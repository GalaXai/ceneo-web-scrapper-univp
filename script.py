


class Scrapper:
    def __init__(self,id):
        self.id = id
        self.data = {
            'Opinie':[
            ]
        }
        
        
        from bs4 import BeautifulSoup
        import requests
        url =f"https://www.ceneo.pl/{id}/opinie-1"
        result = requests.get(url)
        self.doc = BeautifulSoup(result.text, "html.parser")


    def error_test(self):
        error = self.doc.find(["div"],class_="error-page")
        if error != None :
            return True
        elif self.doc.find(["div"],class_="js_product-reviews") == None:
            return True
        else:
            return False

    def scraping_data(self):
        from bs4 import BeautifulSoup
        import requests
        id = []
        author_name = []
        stars = []
        recomend = []
        purchase = []
        opinion_date = []
        bought_date = []
        review_up =[]
        review_down = []
        message = []
        cons = []
        pros = []

        reviews = self.doc.find(["div"] ,class_="score-extend__review")
        # Ammount of opinions
        if reviews == None:
            return 0

        count = 0
        error = False
        #scraping data
        for count in range(1,51):
            url =f"https://www.ceneo.pl/{self.id}/opinie-{count}"
            result =requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            opinions = doc.find_all(["div"],class_="user-post user-post__card js_product-review")
            for x in opinions:
                #id
                id.append(x["data-entry-id"])
                if x["data-entry-id"] == id[0] and len(id)>1:
                    error = True
                    id.pop(-1)
                    break
                #Author name 
                name = x.find(["span"],class_="user-post__author-name")
                author_name.append(name.contents[0].strip()) # strip to remove newline from ex.'\nm...1'
                #Recomend
                recom = x.find(["em"],class_="recommended")
                try:
                    recomend.append(recom.contents[0])
                except AttributeError:
                    recomend.append(None)


                #Stars
                star = x.find(["span"],class_="user-post__score-count")
                stars.append(star.contents[0][0])
                #Date + Opinion
                purch = x.find(["div"], class_="review-pz")
                if purch != []:
                    purchase.append("True") 
                    date= x.find(["span"],class_="user-post__published")
                    opinion_date.append(date.time["datetime"])
                    bought_date.append(date.contents[-2]["datetime"])
                else:
                    purchase.append("False")
                    date= x.find(["span"],class_="user-post__published")
                    opinion_date.append(date.time["datetime"])
                    bought_date.append("")
                #up and down 
                up = x.find(["div"],class_="js_product-review-usefulness vote")
                review_up.append(up.find_all(["span"])[0].contents[0])
                review_down.append(up.find_all(["span"])[1].contents[0])
                #content
                mess = x.find(["div"],class_="user-post__text")
                word = ""
                for i in range (0,len(mess.contents),2):
                    word+= mess.contents[i].strip()
                message.append(word)
                #pros and cons
                pro = x.find(["div"], class_="review-feature__col")
                list= []
                try:
                    if len(pro)== 2:
                        for i in range(len(pro)):
                            for x in range (0,len(pro[i]),2):
                                list.append(pro[i].contents[x].contents[0])
                            if list[0] == 'Zalety':
                                list.pop(0)
                                pros.append(list)
                            else:
                                list.pop(0)
                                cons.append(list)   
                    else:
                        z = pro.find_all(["div"], class_="review-feature__item")
                        for x in range(len(z)):
                            list.append(z[x].contents[0])
                        pros.append(list)
                        cons.append(None)
                except TypeError:
                    pros.append(None)
                    cons.append(None)

            if error == True:
                break
            else:
                continue

        for i in range(len(id)):
            self.data['Opinie'].append({'id': id[i],'Author':author_name[i],'Ocena': stars[i],
            'Poleca' :recomend[i],'Kupił': purchase[i], 'Data wystawienia opini': opinion_date[i],
            'Data kupna': bought_date[i],'Przydatna opinia': review_up[i],
            'Nieprzydatna opinia': review_down[i],'Treść wiadomości':  message[i],
            'Wady': cons[i], 'Zalety': pros[i]})
        return self.data

    def data_json(self):
        import json
        with open(f'json_data{self.id}.json',"w", encoding="utf-8") as json_file:
            json.dump(self.data['Opinie'],json_file,indent=True,ensure_ascii=False)
            return f"json_data{self.id}.json"
    
    


    def data_csv(self):
        import csv 
        import pandas as pd

        with open(f'json_data{self.id}.json', encoding='utf-8') as inputfile:
            df = pd.read_json(inputfile)

        df.to_csv(f'json_data{self.id}.csv', encoding='utf-8', index=False)

        return f"json_data{self.id}.csv"

    def test(self):
        product_id = self.id
        url =f"https://www.ceneo.pl/{product_id}/opinie-1"
        return url
