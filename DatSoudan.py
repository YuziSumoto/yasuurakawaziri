# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール
from MstKeitai  import *   # 相談方法マスタ

class DatSoudan(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 年月日
  Tanto             = db.StringProperty(multiline=False)      # 担当者
  SoudanHouhou      = db.IntegerProperty()                    # 相談方法  
  Kana              = db.StringProperty(multiline=False)      # 対象者名カナ
  Name              = db.StringProperty(multiline=False)      # 対象者名
  Sex               = db.IntegerProperty()                    # 性別
  BirthDay          = db.DateTimeProperty(auto_now_add=False) # 生年月日
  Zyusyo            = db.StringProperty(multiline=True)       # 住所
  Tel               = db.StringProperty(multiline=False)      # 電話番号
  SName             = db.StringProperty(multiline=False)      # 相談者
  SZokugara         = db.StringProperty(multiline=False)      # 続柄
  SRenrakusaki      = db.StringProperty(multiline=False)      # 連絡先 
  Naiyo             = db.StringProperty(multiline=True)       # 内容
  HKibou            = db.StringProperty(multiline=True)       # 本人希望
  KKibou            = db.StringProperty(multiline=True)       # 家族希望
  Zyokyo            = db.StringProperty(multiline=True)       # 支援状況 
  KazokuKousei      = db.StringProperty(multiline=True)       # 家族構成
  Byoumei           = db.StringProperty(multiline=False)      # 病名 
  Syuzii            = db.StringProperty(multiline=False)      # 主治医 
  Kioureki          = db.StringProperty(multiline=True)       # 既往歴
  Fukuyaku          = db.StringProperty(multiline=False)      # 服薬 
  Idou              = db.StringProperty(multiline=False)      # 移動 
  Syokuzi           = db.StringProperty(multiline=False)      # 食事 
  Haisetu           = db.StringProperty(multiline=False)      # 排泄 
  Nyuyoku           = db.StringProperty(multiline=False)      # 入浴 
  Sonota            = db.StringProperty(multiline=True)       # その他の情報
  Taiou             = db.StringProperty(multiline=True)       # 対応


  def GetAll(self,Kubun): # 全データ取得

    WKeitai = MstKeitai()

    Sql =  "SELECT * From " + self.__class__.__name__

    if int(Kubun) == 1:
      Sql += "    Order By Hizuke Desc"
    else:
      Sql += "    Order By Kana"

    Query = db.GqlQuery(Sql)
    Snap = Query.fetch(Query.count())
    for Rec in Snap:
      Rec.Houhou = WKeitai.GetName(Rec.SoudanHouhou)
    return Snap

  def GetList(self,Hizuke): # 指定日から一週間前のデータ取得

    Edate = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
    Sdate = Hizuke - datetime.timedelta(days=-7)

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += " Where Hizuke >= DATE('" + SDate.strftime('%Y-%m-%d') + "')"
    Sql += "  And  Hizuke <= DATE('" + EDate.strftime('%Y-%m-%d') + "')"
    Sql += "    Order By Hizuke Desc"
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

