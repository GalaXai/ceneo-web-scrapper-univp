from flask import Flask, redirect, send_file , url_for ,render_template , request
from script import Scrapper
import pandas as pd
app = Flask(__name__)


@app.route('/') # home here we type in url
def Home():
   return render_template('Home.html', error="")
   # enter bar  redirect(url_for("url", url="data"))


@app.route('/Error') 
def Error():
   return render_template('Error.html')

@app.route('/result',methods = ['POST', 'GET'])
def Result():
   if request.method == 'POST':
      result = request.form
      scrap = Scrapper(result['Id'])
      id = result['Id']
      if scrap.error_test() == True:
         return render_template("Home.html" , error = "Valid ID or There are not any reviews")
      result = scrap.scraping_data()

      fieldnames = [key for key in result['Opinie'][0].keys()]
      return render_template("Result.html", json = scrap.data_json() ,csv=scrap.data_csv() ,stats = f'/{id}',results=result['Opinie'],fieldnames=fieldnames , len = len )

@app.route('/<file>')
def downloadFile(file):
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = f'{file}'
    return send_file(path, as_attachment=True)

@app.route("/<int:id>/")
def plots(id):
   import json
   df = pd.read_json (f"json_data{id}.json")
   sum = []
   for i in df['Treść wiadomości']:
       sum.append(len(i))
   
   avg = df['Ocena'].sum() / len(df['Ocena'])
   avg = "{:.1f}".format(avg)
   
   count= 0
   for i in df['Przydatna opinia']:
      count += int(i) 

   count2= 0
   for i in df['Nieprzydatna opinia']:
      count2 += int(i) 

   fives = 0
   fours = 0 
   thries = 0
   twos = 0

   for i in df['Ocena']:
      i = int(i)
      if i == 5:
         fives +=1
      if i == 4:
         fours +=1
      if i == 3:
         thries +=1
      if i == 2:
         twos +=1
   firstChart = {"Helpful Opinion": count, "Unhelpful opinion":count2}
   secondChart = {"5":fives,"4":fours,"3":thries,"2":twos}
   return render_template("Graphs.html", firstChartData =json.dumps(firstChart), secondChartData= json.dumps(secondChart))

if __name__ == '__main__':
   app.run()

