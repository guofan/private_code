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
house_result_list_90={}
house_result_list_120={}
house_area_info = {}
house_reserved_120 = {}
house_reserved_90 = {}

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "xsrf_cookies": True,
}

def writeResult(house_type):
    result_list = eval("house_result_list_"+house_type)
    fp = open("./data/"+house_type+"_result.txt","w")
    for key in result_list.keys():
        value = result_list[key]
        fp.write("%d\t%s\n"%(key,value))
    fp.close()

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
    def get_house(self,house_type, index):
        if house_type == '120':
            house_list = house_list_120
            house_result_list = house_result_list_120
            house_reserved = house_reserved_120
        else:
            house_list = house_list_90
            house_result_list = house_result_list_90
            house_reserved = house_reserved_90
        if house_reserved.has_key(index):
            house = house_reserved[index]
            random_num = house_list.index(house)
            house_list.remove(house)
            house_result_list[index]=house
            writeResult(house_type)
            return random_num
        random_num = int(random.random()*1000%len(house_list))
        if house_list[random_num] in house_reserved.values():
            return self.get_house(house_type, index)
        house = house_list[random_num]
        house_list.remove(house)
        house_result_list[index]=house
        writeResult(house_type)
        return random_num
        

    def get(self):
        house_type = self.get_argument('type')
        index = self.get_argument('index')
        self.write(str(self.get_house(house_type, int(index))))

def load_data():
    gethouselist = []
    fp = open("./data/120_result.txt")
    lines = fp.readlines()
    for line in lines:
        token = line.strip().split("\t")
        house_result_list_120[int(token[0])] = token[1]
        gethouselist.append(token[1])
    fp.close()
    fp = open("./data/90_result.txt")
    lines = fp.readlines()
    for line in lines:
        token = line.strip().split("\t")
        house_result_list_90[int(token[0])] = token[1]
        gethouselist.append(token[1])
    fp.close()
    fp = open("./data/120.txt")
    lines = fp.readlines()
    for line in lines:
        token = line.split(" ")
        house = token[0]
        area = token[1]
        house_area_info[house]=area
        if house in gethouselist:
            continue
        house_list_120.append(house)
    fp.close()
    fp = open("./data/90.txt")
    lines = fp.readlines()
    for line in lines:
        token = line.split(" ")
        house = token[0]
        area = token[1]
        house_area_info[house]=area
        if house in gethouselist:
            continue
        house_list_90.append(house)
    fp.close()

    fp = open("./data/120_reserved.txt")
    lines = fp.readlines()
    for line in lines:
        token = line.strip().split("\t")
        house_reserved_120[int(token[0])] = token[1]
    fp.close()
    fp = open("./data/90_reserved.txt")
    lines = fp.readlines()
    for line in lines:
        token = line.strip().split("\t")
        house_reserved_90[int(token[0])] = token[1]
    fp.close()

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/init",InitHandler),
    (r"/initdata",InitDataHandler),
    (r"/login.html",AuthHandler),
    (r"/index.html",indexHandler),
    (r"/random",randomHandler),
], **settings)


if __name__ == "__main__":
    load_data()
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
