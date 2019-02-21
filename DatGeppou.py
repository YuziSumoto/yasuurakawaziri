# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール

class DatGeppou(db.Model):
  Nengetu           = db.DateTimeProperty(auto_now_add=False) # 年月
  Bango             = db.IntegerProperty()                    # 番号
  Kensu             = db.IntegerProperty()                    # 件数

  def GetList(self,Nengetu): # 指定日のデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Nengetu = DATE('" + Nengetu.replace("/","-") + "')"
    Sql += "    Order By Bango"

    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())

  def DelList(self,Nengetu): # 指定日のデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Nengetu = DATE('" + Nengetu.replace("/","-") + "')"
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

    return

