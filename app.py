from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy

app=Flask("assignment")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb/data.sqlite'
db=SQLAlchemy(app)
print(db)

class coupon(db.Model):
      id=db.Column(db.Integer, primary_key = True)
      code=db.Column(db.Text)
      valid_from=db.Column(db.Text)
      valid_to=db.Column(db.Text)
      discount=db.Column(db.Integer)
      upto=db.Column(db.Integer)
  
      def __init__(self,code,valid_from,valid_to, discount,upto):
                self.code=code
                self.valid_from=valid_from
                self.valid_to= valid_to
                self.discount= discount
                self.upto= upto
db.create_all()

@app.route("/")
def index():
    return "home" 

@app.route("/my1")
def my1():
    return "my1"   

@app.route("/me")
def me():
    return render_template("my.html")

@app.route("/data")
def mysearch():
    if request.method=="GET":
       code=request.args.get("c")
       valid_from=request.args.get("f")
       valid_to=request.args.get("t")
       discount=request.args.get("d")
       upto=request.args.get("u")
    
    code=coupon(code,valid_from,valid_to, discount,upto)
    db.session.add(code)
    db.session.commit()
    

    return "code  created...."   
@app.route("/list")
def list():
    import sqlite3
    import json
    import pandas as pd
    sql_connect = sqlite3.connect('mydb/data.sqlite')
    cursor = sql_connect.cursor()
    query = "SELECT * FROM coupon;"
    rv = cursor.execute(query).fetchall()
    row_headers=[x[0] for x in cursor.description]
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    final_list=json.dumps(json_data,indent=4) 
    return "<pre>" + final_list + "</pre>"

@app.route("/apply")
def apply():
    return render_template("apply.html")

@app.route("/price")
def price():
    if request.method=="GET":
       price=request.args.get("price")
       code=request.args.get("code")
    print(code)   
    import sqlite3
    import json
    import pandas as pd
    sql_connect = sqlite3.connect('mydb/data.sqlite')
    cursor = sql_connect.cursor()
    mycode=code
    print(type(mycode))
    res=coupon.query.filter_by(code=code)
    valid_from=res.all()[0].valid_from
    valid_to=res.all()[0].valid_to
    discount=res.all()[0].discount
    upto=res.all()[0].upto
    import time
    import datetime
    yr=time.localtime(time.time())[0]
    month=time.localtime(time.time())[1]
    day=time.localtime(time.time())[2]
    d1 = datetime.datetime(yr, month, day)
    today='{:%Y-%m-%d}'.format(d1)
    print(valid_from,valid_to,today,price,upto)
    print(valid_from<=today<=valid_to)
    print(price,upto)
    print(type(price))
    
    price=int(price)
    if valid_from<=today<=valid_to:
        if price>=upto:
            print(discount,price)
            dis=discount*price/100
            print(dis)
            amount=price-dis
            print(amount)
            return str(amount)
        else:
            return "price is less than {}".format(upto)
    else: 
        return "code is invalid"            

     

 

     

