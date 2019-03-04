# -*- coding: UTF-8 -*-
from google.appengine.ext import db

class MstGyoumuSoudan(db.Model):
  GyoumuCD    = db.IntegerProperty()                    # 地域CD
  SoudanCD    = db.IntegerProperty()                    # 地域CD
  Name        = db.StringProperty(multiline=False)      # 地域名

  def GetAll(self):

    Sql  =   "SELECT * FROM " + self.__class__.__name__
    Sql  +=  " Where GyoumuCD > 0"
    Sql  +=  " ORDER by GyoumuCD,SoudanCD"
    Snap = db.GqlQuery(Sql)
    return Snap

  def GetGyoumu(self):

    Sql  =   "SELECT GyoumuCD,Name FROM " + self.__class__.__name__
    Sql  +=  " Where SoudanCD = 0"
    Sql  +=  " ORDER by GyoumuCD"
    Query = db.GqlQuery(Sql)

    if Query.count() == 0:
      Rec = MstGyoumuSoudan()
      Rec.GyoumuCD   = 0
      Rec.SoudanCD   = 0
      Rec.Name = u"未指定"
      Rec.put()

    return Query.fetch(Query.count())

  def GetSoudan(self,GyoumuCD):

    Sql  =   "SELECT SoudanCD,Name FROM " + self.__class__.__name__
    Sql  +=  " Where GyoumuCD = " + str(GyoumuCD)
    Sql  +=  "  And  SoudanCD > 0"
    Sql  +=  " ORDER by SoudanCD"
    Query = db.GqlQuery(Sql)

    return Query.fetch(Query.count())

  def GetRec(self,GyoumuCD,SoudanCD): # 指定CDのデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where GyoumuCD = " + str(GyoumuCD) 
    Sql +=  "  And  SoudanCD = " + str(SoudanCD) 
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())[0]

  def GetRecKey(self,Key): # 指定keyのデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where __key__ = KEY('" + str(Key) + "')"
    Query = db.GqlQuery(Sql)
    return Query.fetch(Query.count())[0]

  def DelRec(self,GyoumuCD,SoudanCD): # 指定CDのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where GyoumuCD = " + str(GyoumuCD) 
    Sql +=  "  And  SoudanCD = " + str(SoudanCD) 
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

  def DelRecKey(self,Key): # 指定キーのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where __key__ = KEY('" + str(Key) + "')"
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

  def GetName(self,GyoumuCD,SoudanCD): # CDキーのデータ取得

    if GyoumuCD is None:
      return ""
    if SoudanCD is None:
      SoudanCD = 0
    
    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where GyoumuCD = " + str(GyoumuCD) 
    Sql +=  "  And  SoudanCD = " + str(SoudanCD) 
    Query = db.GqlQuery(Sql)
    if Query.count() == 0:
      RetStr = ""
    else:
      RetStr = Query.fetch(1)[0].Name

    return RetStr

    return
