from flask import Flask, request, render_template
import pandas as pd
import time
import pyautogui as pg
import webbrowser as web


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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)