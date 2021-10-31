from flask import Flask , request , render_template
from pytesseract.pytesseract import Output
from werkzeug.user_agent import UserAgent
# from webcam import webcam
import subprocess as s
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_recaptcha  import ReCaptcha
import requests as r
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['RECAPTCHA_SITE_KEY'] = "6LchFgQdAAAAAM8uIYV-aPTebU9845CAFYxljytv"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LchFgQdAAAAAGhm4mxLR_Yrt_RLxWRj540Lytcm"
db = SQLAlchemy(app)
recaptcha = ReCaptcha(app)
user_data = []
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.String(30),nullable=False)
    old_addr = db.Column(db.String(1000),nullable=False)
    updated_addr = db.Column(db.String(1000),nullable=False)
    current_date = db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"\n-ID : {self.id} \n-  UID : {self.uid} \n- Date : {self.current_date}"

# app.register_blueprint(webcam,uri_prefix="/webcammm")

@app.route('/', methods=['GET','POST'])
@app.route('/home' ,methods=['GET',"POST"])
def home():
    # uid = request.form['uid']
    # db.Query.all()
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        if recaptcha.verify():
            message = "Captcha Verified !"    
        else:
            message = "Please fill prove you're a human first ."
        uid = request.form["uid"]
        p4 = s.run(f"python .\otp.py {uid}",shell=True,capture_output=True)
        user_data.append(uid)  
        response = p4.stdout
        print(response)
        if "\"status\":\"Y\"" in str(response):
            return render_template('get_otp.html',message=message)
        else:
            return "Not working seeddd"
    return render_template('login.html')
        
@app.route('/webcam', methods=['GET','POST'])
def webcam():
    return render_template('webcam.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #fs = request.files['snap'] # it raise error when there is no `snap` in form
        fs = request.files.get('snap')
        if fs:
            print('FileStorage:', fs)
            print('filename:', fs.filename)
            with open('txnId','r') as f:
                fname=f.read()
            fs.save("images/"+str(fname))
            # return 'Got Snap!'
        else:
            return 'You forgot Snap!'
    
    return None
    
@app.route('/auth', methods=['GET','POST'])

def auth():
    otp = request.form["otp"]
    with open('txnId','r') as f:
        txnId = f.read()
    # s.run(f"python auth.py {user_data[0]} {otp} {txnId}",shell=True)
    dict = {
        "uid" : user_data[0],
        "vid" : '',
        "txnId" : txnId,
        "otp" : otp,
    }
    print("dict : " + str(dict))
    req = r.post("https://stage1.uidai.gov.in/onlineekyc/getAuth/",json=dict)
    response = req.content.decode()
    print(str(response))
    if "\"status\":\"y\"" in str(response):
        return render_template('webcam.html')
    else:
        return "Wrong otp entered Please retry"
    

@app.route('/update', methods=['GET','POST'])
def extract():
    with open('txnId','r') as f:
        fname=f.read()
    s.call(f"python extract_text.py images/{fname}",shell=True)
    with open('text','r') as f:
        text = f.read()
        user_data.append(text)
        print(user_data)
    return render_template('address_update.html',text=text) 
    
@app.route('/fetch', methods=['GET','POST'])
def fetch():    
    return str(User.query.all())

@app.route('/final', methods=['GET','POST'])
def final():
    final_addr = request.form["final_addr"]
    user_data.append(final_addr)
    for data in user_data:
        print(data)
    data = User(uid=user_data[0],old_addr=user_data[1],updated_addr=user_data[2])
    db.session.add(data)
    db.session.commit()
    user_data.clear()
    
    return render_template('final.html')

if __name__ == '__main__':
    app.run()