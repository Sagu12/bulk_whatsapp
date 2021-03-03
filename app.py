from flask import Flask, request, render_template
import pandas as pd
import time
import pyautogui as pg
import webbrowser as web
#from textblob import TextBlob
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#import nltk
#from newspaper import Article
#nltk.download("punkt")



app = Flask(__name__)



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'), encoding='cp1252')
        return render_template('index.html', tables=[df.to_html(classes='data', header="true")])

    return render_template("index.html")



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'))
        df_dict= df.to_dict('list')
        leads = df_dict['LeadNumber']
        messages = df_dict['Message']

        combo = zip(leads,messages)
        first = True
        for lead,message in combo:

            time.sleep(6)
            web.open("https://web.whatsapp.com/send?phone="+lead+"&text="+message)
            if first:
                time.sleep(8)
                first=False
            width,height = pg.size()
            pg.click(width/2,height/2)
            time.sleep(15)

            pg.press('enter')
            time.sleep(15)
            pg.hotkey('ctrl', 'w')
    return render_template('upload.html')



#----------------------------------------------------------------------------------------------------------------------

#@app.route('/sentiment') # default route
#def new():
    #result = ""
    #return render_template('sentiment.html', result = result) # renders template: index.html with argument result = ""

#@app.route('/result', methods = ['POST', 'GET']) # /result route, allowed request methods; POST, and GET
#def predict():
    #sid_obj = SentimentIntensityAnalyzer()

    #if request.method == 'POST': 
        #result = request.form['Name'] # fetches text from <input name = "Name"> from index.html
        #result = sid_obj.polarity_scores(result)
        #for sentence in blob.sentences:
            #result = sentence.sentiment.polarity # result = polarity value

        #return render_template('sentiment.html', result = result ) # renders template: index.html with argument result = polarity value calculated
    #else:
        #return render_template('sentiment.html')



if __name__ == '__main__':
    app.run(debug=True)