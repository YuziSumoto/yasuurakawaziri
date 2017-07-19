# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール

class DatService(db.Model):
  KanzyaID          = db.IntegerProperty()                    # 利用者番号
  CD                = db.IntegerProperty()                    # サービスCD
  Kubun             = db.IntegerProperty(default=0)           # 公的区分
  Name              = db.StringProperty(multiline=False)      # サービス名

  def GetList(self,KanzyaID): # 全データ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where KanzyaID = " + str(KanzyaID)
    Sql += "    Order By CD"
    Query = db.GqlQuery(Sql)
    Snap  = Query.fetch(Query.count())
    return Snap

  def GetRec(self,Key): # 指定キーのデータ取得

    if Key == "": # キー未指定なら空レコードを返す
      return DatService()

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

