# -*- coding = utf-8 -*-

from datetime import datetime as dt
from flask import Flask, render_template, request, jsonify
import json, glob

app = Flask(__name__)
@app.route('/')
def index():
  return render_template("index.html")

# サーバー側から条件を取得し、値を返す
@app.route("/post", methods=["GET","POST"])
def update():
  if request.headers["Content-Type"]!="application/json":
    print(request.headers["Content-Type"])
    return jsonify(res="error")
  
  
  return jsonify(image_path="./static/image/UseLicensePerDay_%s.png"%target_date.strftime("%Y_%m_%d"),\
    sum_fee_for_day=sum_fee_for_day, sum_fee_for_month=sum_fee_for_month, sum_fee_for_year=sum_fee_for_year)

if __name__=="__main__":
    app.run(host='localhost', port=8080)


