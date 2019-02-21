# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール
from MstKeitai       import *   # 相談方法マスタ
from MstSoudanSya    import *   # 相談方法マスタ
from MstGyoumuSoudan import *   # 相談方法マスタ

class DatCase(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 年月日
  Bango             = db.IntegerProperty()                    # 連番
  CaseName          = db.StringProperty(multiline=False)      # ケース名
  SoudanSyaCD       = db.IntegerProperty()                    # 相談者CD
  SoudanHouhou      = db.IntegerProperty()                    # 相談方法  
  YakanKubun        = db.BooleanProperty()                    # 夜間区分
  GyoumuCD          = db.IntegerProperty()                    # 業務区分
  SoudanCD          = db.IntegerProperty()                    # 業務区分
  Naiyo             = db.StringProperty(multiline=True)       # 内容
  NintiYouin        = db.BooleanProperty()                    # 認知症要因
  TantouSyaCD       = db.IntegerProperty()                    # 担当者CD
  NintiSuisin       = db.BooleanProperty()                    # 認知症推進員対応
  KakuninSyoCD      = db.IntegerProperty()                    # 確認書CD
  KakuninGaitou     = db.BooleanProperty()                    # 確認書該当者

  def GetAll(self): # 全データ取得

    WKeitai    = MstKeitai()
    WSoudanSya = MstSoudanSya()

    Sql =  "SELECT * From " + self.__class__.__name__
    Sql += "    Order By Hizuke Desc"
    Query = db.GqlQuery(Sql)
    Snap = Query.fetch(Query.count())
    for Rec in Snap:
      Rec.Houhou    = WKeitai.GetName(Rec.SoudanHouhou)
      Rec.SoudanSya = WSoudanSya.GetName(Rec.SoudanSyaCD)
      Rec.Gyoumu    = WGyoumuSoudan.GetName(Rec.GyoumuCD,0)
      Rec.Soudan    = WGyoumuSoudan.GetName(Rec.GyoumuCD,Rec.SoudanCD)
    return Snap

  def GetList(self,Hizuke): # 指定日のデータ取得

    WKeitai    = MstKeitai()
    WSoudanSya = MstSoudanSya()
    WGyoumuSoudan = MstGyoumuSoudan()

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Hizuke = DATE('" + Hizuke.replace("/","-") + "')"
    Sql += "    Order By Bango"
    Query = db.GqlQuery(Sql)
    Snap = Query.fetch(Query.count())
    for Rec in Snap:
      Rec.Houhou = WKeitai.GetName(Rec.SoudanHouhou)
      Rec.SoudanSya = WSoudanSya.GetName(Rec.SoudanSyaCD)
      Rec.Gyoumu    = WGyoumuSoudan.GetName(Rec.GyoumuCD,0)
      Rec.Soudan    = WGyoumuSoudan.GetName(Rec.GyoumuCD,Rec.SoudanCD)

    return Snap

  def GetMonthData(self,Hizuke): # 指定月のデータ取得

    DHizuke  = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
    YokuGetu = DHizuke + datetime.timedelta(days=31)  # 01日の31日後は絶対翌月
    Yoku01   = YokuGetu.strftime('%Y/%m/01')

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Hizuke >= DATE('" + Hizuke.replace("/","-") + "')"
    Sql += "  And  Hizuke <  DATE('" + Yoku01.replace("/","-") + "')"
    Sql += "    Order By Hizuke"
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

