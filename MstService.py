# -*- coding: UTF-8 -*-
from google.appengine.ext import db

class MstService(db.Model):
  CD       = db.IntegerProperty()                    # CD
  Kubun    = db.IntegerProperty(default=0)           # 区分 0:公的 1:非公
  Name     = db.StringProperty(multiline=False)      # 名称

  def GetAll(self):

    Sql  =   "SELECT * FROM " + self.__class__.__name__
    Sql  +=  " ORDER by CD"
    Query = db.GqlQuery(Sql)

    return Query.fetch(Query.count())

  def DelRec(self,CD): # 指定CDのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where CD = " + str(CD) 
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

  def GetRec(self,CD): # CDキーのデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where CD = " + str(CD) 
    Query = db.GqlQuery(Sql)
    if Query.count() == 0:
      RetRec = MstService()
    else:
      RetRec = Query.fetch(1)[0]

    return RetRec

    return
