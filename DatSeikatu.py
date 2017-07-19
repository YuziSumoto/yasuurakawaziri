# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール
import common    # 共通ルーチン
from MstKaigodo  import *   # 介護度マスタ
from MstTiiki    import *   # 使用者マスタ

class DatSeikatu(db.Model):
  KanzyaID          = db.IntegerProperty()                    # 利用者番号
  ZiritudoS         = db.IntegerProperty()                    # 障害自立度
  ZiritudoN         = db.IntegerProperty()                    # 認知症自立度
  Kazoku            = db.StringProperty(multiline=True)      # 家族関係
  NanbyoFlg         = db.BooleanProperty()                    # 難病有無
  Nanbyo            = db.StringProperty(multiline=False)      # 難病名
  Keizai1           = db.BooleanProperty()                    # 経済状況
  Keizai2           = db.BooleanProperty()                    # 経済状況
  Keizai3           = db.BooleanProperty()                    # 経済状況
  Keizai            = db.StringProperty(multiline=False)      # 難病名
  Getugaku          = db.StringProperty(multiline=False)      # 難病名
  Soudansya         = db.StringProperty(multiline=False)      # 相談者
  SoudanHoka        = db.StringProperty(multiline=False)      # 相談者その他
  SoudanZ           = db.StringProperty(multiline=False)      # 相談者住所
  SoudanR           = db.StringProperty(multiline=False)      # 相談者連絡先
#  Renrakusaki       = db.StringProperty(multiline=False)      # 連絡先
#  RenrakuHoka       = db.StringProperty(multiline=False)      # 連絡先その他
#  RenrakuZ          = db.StringProperty(multiline=False)      # 連絡先住所
#  RenrakuR          = db.StringProperty(multiline=False)      # 連絡先連絡先
  Syumi             = db.StringProperty(multiline=True)       # 趣味
  Yuzin             = db.StringProperty(multiline=True)       # 友人
  Seikatu           = db.StringProperty(multiline=True)       # 生活状況
  SeikatuReki       = db.StringProperty(multiline=True)       # 生活歴
  Zyutaku           = db.StringProperty(multiline=False)      # 住宅環境
  Kaisyu            = db.StringProperty(multiline=False)      # 住宅改修の有無

  def GetRec(self,KanzyaID): # 指定キーのデータ取得

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where KanzyaID = " + str(KanzyaID)
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Rec = DatSeikatu()
    else:
      Rec = Snap.fetch(Snap.count())[0]
      
    return Rec

  def DelRec(self,Key): # 指定キーのデータ削除

    Sql =  "SELECT * FROM " + self.__class__.__name__
    Sql +=  " Where KanzyaID = " + str(KanzyaID)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

    return

