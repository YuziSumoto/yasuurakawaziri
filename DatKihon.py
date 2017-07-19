# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール
import common    # 共通ルーチン
from MstKaigodo  import *   # 介護度マスタ
from MstTiiki    import *   # 使用者マスタ

class DatKihon(db.Model):
  KanzyaID          = db.IntegerProperty()                    # 利用者番号
  Tanto             = db.StringProperty(multiline=False)      # 担当者
  Kana              = db.StringProperty(multiline=False)      # 対象者名カナ
  Name              = db.StringProperty(multiline=False)      # 対象者名
  Sex               = db.IntegerProperty()                    # 性別
  BirthDay          = db.DateTimeProperty(auto_now_add=False) # 生年月日
  Tiiki             = db.IntegerProperty()                    # 地域コード
  Yubin             = db.StringProperty(multiline=False)      # 郵便番号
  Zyusyo            = db.StringProperty(multiline=True)       # 住所
  Tel               = db.StringProperty(multiline=False)      # 電話番号
  Soudanbi          = db.DateTimeProperty(auto_now_add=False) # 相談日
  Keitai            = db.IntegerProperty()                    # 相談形態
  Kaisu             = db.StringProperty(multiline=False)      # 回数 
  Zyokyo            = db.StringProperty(multiline=False)      # 状況 
  Sisetu            = db.StringProperty(multiline=False)      # 入院・入所施設 
  SyogaiZirituDo    = db.IntegerProperty()                    # 障害老人の自立度
  NintiZirituDo     = db.IntegerProperty()                    # 認知症の自立度
  Kaigodo           = db.IntegerProperty()                    # 認定介護度
  HokenStart        = db.DateTimeProperty(auto_now_add=False) # 保険開始日
  HokenEnd          = db.DateTimeProperty(auto_now_add=False) # 保険終了日
  HokenKaigodo      = db.IntegerProperty()                    # 前回介護度
  CheckList         = db.BooleanProperty()                    # 基本チェックリスト
  CheckDay          = db.DateTimeProperty(auto_now_add=False) # チェックリスト記入日
  Taiou             = db.StringProperty(multiline=True)       # 対応
  Keii              = db.StringProperty(multiline=True)       # 経緯
  Naiyo             = db.StringProperty(multiline=True)       # 内容
  KinkyuName1       = db.StringProperty(multiline=False)      # 緊急連絡先名1
  KinkyuZyusyo1     = db.StringProperty(multiline=False)      # 緊急連絡先住所1
  KinkyuTel1        = db.StringProperty(multiline=False)      # 緊急連絡先電話1
  KinkyuZokugara1   = db.StringProperty(multiline=True)       # 緊急連絡先続柄1
  KinkyuName2       = db.StringProperty(multiline=False)      # 緊急連絡先名2
  KinkyuZyusyo2     = db.StringProperty(multiline=False)      # 緊急連絡先住所2
  KinkyuTel2        = db.StringProperty(multiline=False)      # 緊急連絡先電話2
  KinkyuZokugara2   = db.StringProperty(multiline=True)       # 緊急連絡先続柄2
  KinkyuName3       = db.StringProperty(multiline=False)      # 緊急連絡先名3
  KinkyuZyusyo3     = db.StringProperty(multiline=False)      # 緊急連絡先住所3
  KinkyuTel3        = db.StringProperty(multiline=False)      # 緊急連絡先電話3
  KinkyuZokugara3   = db.StringProperty(multiline=True)       # 緊急連絡先続柄3
  KinkyuName4       = db.StringProperty(multiline=False)      # 緊急連絡先名3
  KinkyuZyusyo4     = db.StringProperty(multiline=False)      # 緊急連絡先住所3
  KinkyuTel4        = db.StringProperty(multiline=False)      # 緊急連絡先電話3
  KinkyuZokugara4   = db.StringProperty(multiline=True)       # 緊急連絡先続柄3
  Bikou             = db.StringProperty(multiline=True)       # 備考

  def GetAll(self): # 全データ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += "    Order By KanzyaID"
    Query = db.GqlQuery(Sql)
    WkTiiki   = MstTiiki()
    WkKaigodo = MstKaigodo()
    Snap = Query.fetch(Query.count())
    for Rec in Snap:
      Rec.Tanzyoubi = common.GetWareki(Rec.BirthDay)
      if Rec.Zyusyo is None:
        pass
      else:
        Rec.Zyusyo   = Rec.Zyusyo.replace("\n","<BR>")
      Rec.TiikiName   = WkTiiki.GetName(Rec.Tiiki)
      Rec.KaigodoName = WkKaigodo.GetName(Rec.Kaigodo)
      Rec.HokenKaigodoName = WkKaigodo.GetName(Rec.HokenKaigodo)

    return Snap

  def GetRec(self,KanzyaID): # 指定キーのデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where KanzyaID = " + str(KanzyaID)
    Snap = db.GqlQuery(Sql)
    Rec = Snap.fetch(Snap.count())

    return Rec[0]

  def DelRec(self,KanzyaID): # 指定キーのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where KanzyaID = " + str(KanzyaID)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

    return

