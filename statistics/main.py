# -*- coding: utf-8 -*-
from json import dumps
import json
import requests
from flask import Flask, render_template,request, jsonify,g, redirect,url_for, session, logging, flash, request, Markup
from flask_restful import Resource, Api
import urllib3
import collections


app = Flask(__name__)
api = Api(app)
    
#calculates the change of percentage of gdp
def real_gdp_growth(value, base_year):
    pos = 0
    result = []

    for x in value:
        if pos == 0:
            #change = ((x - base_year)/base_year)*100
            result.append(0.0)
            pos+=1
        else:
            change = ((float(x)/float(value[pos-1])))-1
            result.append(change)
            pos+=1
            

    return result
    
#connects to World Bank and Statistik Databasen
def db_connect():
    link = 'http://api.worldbank.org/v2/countries/mx/indicators/NY.GDP.MKTP.CD/?format=json'
    r = requests.get(link)
    
    #statistik data basen
    url = 'http://api.scb.se/OV0104/v1/doris/en/ssd/START/NR/NR0103/NR0103E/NR0103ENS2010T02A'
    data = {
  "query": [
    {
      "code": "TranspostProducent",
      "selection": {
        "filter": "item",
        "values": [
          "B1m"
        ]
      }
    },
    {
      "code": "ContentsCode",
      "selection": {
        "filter": "item",
        "values": [
          "NR0103CQ"
        ]
      }
    },
    {
      "code": "Tid",
      "selection": {
        "filter": "item",
        "values": [
          "2000",
          "2001",
          "2002",
          "2003",
          "2004",
          "2005",
          "2006",
          "2007",
          "2008",
          "2009",
          "2010",
          "2011",
          "2012",
          "2013",
          "2014",
          "2015"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
  
  
}
    resp = requests.post(url, json=data)
    
    return r, resp
    
@app.route('/')
def index():

    r, resp = db_connect()
    as_json = r.json()
    wb_info = as_json[1]
    result2=[]
    result3=[]
    country =wb_info[0]['country']['value']
    title = wb_info[0]['indicator']['value']
    for x in wb_info[2:18]:
        result2.append(x['value'])
    for x in wb_info[2:18]:
        result3.append(x['date'])
    base_year1 = 343792792161.261
    change = real_gdp_growth(result2[::-1], base_year1)
    
    data2 = resp.json()
    
    values = []
    text = []
    key = []
    ex = [1,2,3,4,5,6,7,8,9]
    
    for x in data2:
        for y in data2[x]:
            try:
                values.append(y['values'][0])
    
            except KeyError:
                pass

    for x in data2:
        for y in data2[x]:
            try:
                text.append(y['text'])
    
            except KeyError:
                pass
    for x in data2:
        for y in data2[x]:
            try:
                key.append(y['key'][1])
    
            except KeyError:
                pass
    sw_change = real_gdp_growth(values,0)
    return render_template( 'index.html', values = values, text = text, key = key, wb_value= result2, wb_year = result3, wb_country = country, wb_title=title, change_wb = change, change_sw = sw_change)
    
    


@app.route('/gdp')
def gdp():
    r, resp = db_connect()
    as_json = r.json()
    wb_info = as_json[1]
    result2=[]
    result3=[]
    country =wb_info[0]['country']['value']
    title = wb_info[0]['indicator']['value']
    for x in wb_info[2:18]:
        result2.append(x['value'])
    for x in wb_info[2:18]:
        result3.append(x['date'])
    base_year1 = 343792792161.261
    change = real_gdp_growth(result2[::-1], base_year1)
    
    data2 = resp.json()
    
    values = []
    text = []
    key = []
    ex = [1,2,3,4,5,6,7,8,9]
    
    for x in data2:
        for y in data2[x]:
            try:
                values.append(y['values'][0])
    
            except KeyError:
                pass

    for x in data2:
        for y in data2[x]:
            try:
                text.append(y['text'])
    
            except KeyError:
                pass
    for x in data2:
        for y in data2[x]:
            try:
                key.append(y['key'][1])
    
            except KeyError:
                pass
    return render_template('gdp.html',values = values, text = text, key = key, wb_value= result2, wb_year = result3, wb_country = country, wb_title=title)
    
       
