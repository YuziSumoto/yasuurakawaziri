# -*- coding: UTF-8 -*-
from google.appengine.ext import db

class MstByoumei(db.Model):
  CD       = db.IntegerProperty()                    # CD
  Kana     = db.StringProperty(multiline=False)      # カナ名
  Name     = db.StringProperty(multiline=False)      # 名称

  def GetAll(self):

    Sql  =   "SELECT * FROM " + self.__class__.__name__
    Sql  +=  " ORDER by Kana"
    Query = db.GqlQuery(Sql)

    if Query.count() == 0:
      Rec = MstByoumei()
      Rec.CD   = 0
      Rec.Name = u"その他"
      Rec.put()

    return Query.fetch(Query.count())

  def GetRec(self,CD): #指定CDのデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where CD = " + str(CD)
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())[0]

  def DelRec(self,CD): # 指定CDのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where CD = " + str(CD) 
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()
