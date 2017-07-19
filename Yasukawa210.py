#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール

from MstUser        import *   # 使用者マスタ
from MstZiritudoS   import *   # 障害者自立度マスタ
from MstZiritudoN   import *   # 認知症自立度マスタ
from DatKihon       import *   # 相談データ
from DatSeikatu     import *   # 生活データ

class MainHandler(webapp2.RequestHandler):

  @login_required
#-------------------------------------------------------------
# 初期表示
#-------------------------------------------------------------
  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    cookieStr = 'KanzyaID=' + self.request.get('KanzyaID') + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Kihon = DatKihon().GetRec(self.request.get('KanzyaID'))

    LblMsg = ""

    template_values = {
      'Kihon'          : Kihon,
      'Seikatu'        : DatSeikatu().GetRec(self.request.get('KanzyaID')),
      'MstZiritudoS'   : MstZiritudoS().GetAll(),
      'MstZiritudoN'   : MstZiritudoN().GetAll(),
      'LblMsg'         : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa210.html')
    self.response.out.write(template.render(path, template_values))
#-------------------------------------------------------------
# ボタン押下時
#-------------------------------------------------------------
  def post(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    Rec = {} # 画面受け渡し用領域
    LblMsg = ""

    LblMsg = ""

    KanzyaID = self.request.cookies.get('KanzyaID', '') # CooKie取得

    for param in self.request.arguments():
      if "BtnYasukawa" in param:
        self.DBSet()
        self.redirect("/" + param.replace("Btn","") + "/?KanzyaID=" + KanzyaID) #

    Kihon = DatKihon().GetRec(KanzyaID)

    template_values = {
      'Kihon'     : Kihon,
      'Seikatu'   : DatSeikatu().GetRec(KanzyaID),
      'MstZiritudoS'   : MstZiritudoS().GetAll(),
      'MstZiritudoN'   : MstZiritudoN().GetAll(),
      'LblMsg'    : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa210.html')
    self.response.out.write(template.render(path, template_values))

#############################################################################
#------------------------------------------------------------------------------
  def ChkInput(self):   # 入力チェック

    ErrFlg = True
    LblMsg = ""

    if common.CheckTime(self,self.request.get('TxtZikoku_S')) == False:
      LblMsg = "開始時刻が正しくありません。(HH:MM)"
    elif common.CheckTime(self,self.request.get('TxtZikoku_E')) == False:
      LblMsg = "終了時刻が正しくありません。(HH:MM)"
    elif common.CheckDate(self,self.request.get('TxtBirthDay')) == False:
      LblMsg = "生年月日が正しくありません。(yyyy/mm/dd)"
    elif common.CheckDate(self,self.request.get('TxtZyusinKibou1')) == False:
      LblMsg = "受診希望日１件目が正しくありません。(yyyy/mm/dd)"
    elif common.CheckDate(self,self.request.get('TxtZyusinKibou2')) == False:
      LblMsg = "受診希望日２件目が正しくありません。(yyyy/mm/dd)"
    elif common.CheckDate(self,self.request.get('TxtZyusinKibou3')) == False:
      LblMsg = "受診希望日３件目が正しくありません。(yyyy/mm/dd)"
    else:
      ErrFlg = False

    return (ErrFlg,LblMsg)
#------------------------------------------------------------------------------
  def ReDisp(self,Rec):  # 画面再表示

    Rec["OptHouhou"   + self.request.get('OptHouhou')]   = "Checked"
    Rec["OptZyukyo"   + self.request.get('OptHouhou')]   = "Checked"
    Rec["OptSex"      + self.request.get('OptSex')]      = "Checked"
    Rec["OptZokugara" + self.request.get('OptZokugara')] = "Checked"

    for Ctr in range(1,5):
      if self.request.get('ChkTaiou' + str(Ctr)) == "on":
        Rec["ChkTaiou" + str(Ctr)] = "checked='checked'"

    return  # Recは構造体なんで参照→直接変更→戻り値不要

#------------------------------------------------------------------------------
  def DBSet(self):  # データ保存

    KanzyaID =  self.request.cookies.get('KanzyaID', '') # Cookieより
    if KanzyaID == "":
      Rec = DatSeikatu() # 新規レコード
    else:
      Rec = DatSeikatu().GetRec(KanzyaID) # 更新

    Rec.KanzyaID = int(KanzyaID)
    
    Dic = Rec.properties()
    DicKeys = Dic.keys()

    for DicKey in DicKeys: # Boolean項目初期化→チェックボックス項目
      if type(Dic[DicKey]) == db.BooleanProperty: 
        setattr(Rec,DicKey,False)

    ParaNames = self.request.arguments()
    for ParaName in ParaNames: # 前画面項目引き渡し
      if ParaName not in Dic: # 該当文字列が辞書にない
        ParaName = ParaName # 何もしない
      elif  type(Dic[ParaName]) == db.DateTimeProperty and self.request.get(ParaName)!= "": # 日付型
        setattr(Rec,ParaName,datetime.datetime.strptime(self.request.get(ParaName).replace("/","-"), '%Y-%m-%d'))
      elif  type(Dic[ParaName]) == db.IntegerProperty and self.request.get(ParaName)!= "": # 数値型
        setattr(Rec,ParaName,int(self.request.get(ParaName)))
      elif  type(Dic[ParaName]) == db.BooleanProperty:
        if self.request.get(ParaName) == "True":
          setattr(Rec,ParaName,True)
        else:
          setattr(Rec,ParaName,False)
      else:
        setattr(Rec,ParaName,self.request.get(ParaName))

    Rec.put()
    
    return

#############################################################################
app = webapp2.WSGIApplication([
    ('/Yasukawa210/', MainHandler)
], debug=True)
