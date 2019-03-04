# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール

class DatKeika(db.Model):
  OyaKey            = db.StringProperty(multiline=False)      # 親キー
  Hizuke            = db.DateTimeProperty(auto_now_add=True)  # 日付
  Bango             = db.IntegerProperty()                    # 連番  
  Naiyo             = db.StringProperty(multiline=True)       # 対応


  def GetAll(self,Oyakey): # 該当親キーの全データ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where OyaKey = '" + Oyakey + "'"
    Sql += "    Order By Hizuke Desc,Bango Desc"
    Query = db.GqlQuery(Sql)
    Snap = Query.fetch(Query.count())
    return Snap

  def GetRec(self,Key): # 指定キーのデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where __key__ = KEY('" + str(Key) + "')"
    Snap = db.GqlQuery(Sql)
    Rec = Snap.fetch(Snap.count())

    return Rec[0]

  def DelRec(self,Key): # 指定キーのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where __key__ = KEY('" + str(Key) + "')"
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

    return

  def DelRecOya(self,OyaKey): # 指定キーのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where OyaKey = '" + OyaKey + "'"
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

    return

  def GetLastBango(self,OyaKey,Hizuke): # 指定キー、日付の最終番号取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where OyaKey = '" + OyaKey + "'"
    Sql += "   And  Hizuke = DATE('" + Hizuke.strftime('%Y-%m-%d') + "')"
    Sql +=  "  Order by Bango Desc"
    Query = db.GqlQuery(Sql)
    if Query.count() == 0:
      LastNo = 0
    else:
      LastNo = Query.fetch(1)[0].Bango
    
    return LastNo
