#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: yaofang.py
Author: baidu(baidu@baidu.com)
Date: 2016/04/27 22:27:36
"""
import tornado.ioloop
import tornado.web
import os
import random
import json

house_list_90=[]
house_list_120=[]
house_result_list_90=[]
house_result_list_120=[]

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "xsrf_cookies": True,
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/index.html")

class InitHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie("house_list_120","")
        self.set_cookie("house_list_90","")
        self.set_cookie("house_result_list_120","")
        self.set_cookie("house_result_list_90","")
        self.set_cookie("user_name","")
        self.write("init OK")

class InitDataHandler(tornado.web.RequestHandler):
    def get(self):
        result = {}
        result["house_list_120"]=house_list_120
        result["house_list_90"] = house_list_90
        result["house_result_list_120"] = house_result_list_120
        result["house_result_list_90"] = house_result_list_90
        self.write(json.dumps(result))

class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        name=self.get_argument('username')  
        pw=self.get_argument('password')
        if name == "admin" and pw == "xiajing":
            self.set_cookie("user_name","admin")
            self.redirect("/")
        else:
            pass

class indexHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_cookie("user_name")
        if name != "admin":
            self.redirect("/login.html")
        self.render("index.html")

class randomHandler(tornado.web.RequestHandler):
    def get(self):
        house_type = self.get_argument('type')
        index = self.get_argument('index')
        self.write(str(random.random()*100%7))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/init",InitHandler),
    (r"/initdata",InitDataHandler),
    (r"/login.html",AuthHandler),
    (r"/index.html",indexHandler),
    (r"/random",randomHandler),
], **settings)

def load_data():
    fp = open("./data/120.txt")
    lines = fp.readlines()
    for line in lines:
        house_list_120.append(line.split(" ")[0])
    fp.close()
    fp = open("./data/90.txt")
    lines = fp.readlines()
    for line in lines:
        house_list_90.append(line.split(" ")[0])
    fp.close()
    fp = open("./data/120_result.txt")
    lines = fp.readlines()
    for line in lines:
        house_list_120.append(line.split(" ")[0])
    fp.close()
    fp = open("./data/90_result.txt")
    lines = fp.readlines()
    for line in lines:
        house_list_90.append(line.split(" ")[0])
    fp.close()


if __name__ == "__main__":
    load_data()
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
