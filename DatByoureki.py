# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール

class DatByoureki(db.Model):
  KanzyaID          = db.IntegerProperty()                    # 利用者番号
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 年月日
  ByoumeiCD         = db.IntegerProperty()                    # 病名CD
  Byoumei           = db.StringProperty(multiline=False)      # 病名
  IryoKikanCD       = db.IntegerProperty()                    # 医療機関CD
  IryoKikan         = db.StringProperty(multiline=True)       # 医療機関
  Keika             = db.StringProperty(multiline=True)       # 経過
  Naiyo             = db.StringProperty(multiline=True)       # 治療内容・処方

  def GetList(self,KanzyaID): # 指定利用者番号のデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where KanzyaID = " + str(KanzyaID)
    Sql += "    Order By Hizuke"
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())

  def GetLast(self,KanzyaID): # 指定利用者番号の最終データ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where KanzyaID = " + str(KanzyaID)
    Sql += "    Order By Hizuke Desc"
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())

  def GetRec(self,Key): # 指定キーのデータ取得

    if Key == "": # キー未指定なら空レコードを返す
      return DatByoureki()
    
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

