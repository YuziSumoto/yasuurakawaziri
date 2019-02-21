# -*- coding: UTF-8 -*-
from google.appengine.ext import db

class MstSoudanSya(db.Model):
  CD       = db.IntegerProperty()                    # 相談者CD
  Name     = db.StringProperty(multiline=False)      # 相談者名

  def GetAll(self):

    Sql  =   "SELECT * FROM " + self.__class__.__name__
    Sql  +=  " ORDER by CD"
    Query = db.GqlQuery(Sql)

    if Query.count() == 0:
      Rec = MstSoudanSya()
      Rec.CD   = 0
      Rec.Name = u"未指定"
      Rec.put()

    return Query.fetch(Query.count())

  def GetRec(self,Key): # 指定キーのデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where __key__ = KEY('" + str(Key) + "')"
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())[0]

  def DelRec(self,Key): # 指定キーのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where __key__ = KEY('" + str(Key) + "')"
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

  def GetName(self,CD): # CDキーのデータ取得
    if CD is None:
      return ""
    
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where CD = " + str(CD) 
    Query = db.GqlQuery(Sql)
    if Query.count() == 0:
      RetStr = ""
    else:
      RetStr = Query.fetch(1)[0].Name

    return RetStr

    return
