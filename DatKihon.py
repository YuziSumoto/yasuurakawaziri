# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール
import common    # 共通ルーチン
from MstKaigodo  import *   # 介護度マスタ
from MstTiiki    import *   # 使用者マスタ

class DatKihon(db.Model):
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
  KinkyuName        = db.StringProperty(multiline=False)      # 緊急連絡先名
  KinkyuZyusyo      = db.StringProperty(multiline=False)      # 緊急連絡先住所
  KinkyuTel         = db.StringProperty(multiline=False)      # 緊急連絡先電話
  Bikou             = db.StringProperty(multiline=True)       # 備考

  def GetAll(self): # 全データ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql += "    Order By Kana"
    Query = db.GqlQuery(Sql)
    WkTiiki   = MstTiiki()
    WkKaigodo = MstKaigodo()
    Snap = Query.fetch(Query.count())
    for Rec in Snap:
      Rec.Tanzyoubi = common.GetWareki(Rec.BirthDay) 
      Rec.Zyusyo   = Rec.Zyusyo.replace("\n","<BR>")
      Rec.TiikiName   = WkTiiki.GetName(Rec.Tiiki)
      Rec.KaigodoName = WkKaigodo.GetName(Rec.Kaigodo)
      Rec.HokenKaigodoName = WkKaigodo.GetName(Rec.HokenKaigodo)

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

