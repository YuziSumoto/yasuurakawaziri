#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール

from MstUser   import *   # 使用者マスタ

from DatKeika  import *   # 経過データ

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

    cookieStr = 'Key=' + self.request.get('Key') + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    if self.request.get('Key') == "":
      OyaKey = self.request.get('OyaKey')

    if  self.request.get('Key') == "":
      Rec = DatKeika() # 空レコード
    else:
      Rec = DatKeika().GetRec(self.request.get('Key'))
      OyaKey = Rec.OyaKey

    cookieStr = 'OyaKey=' + OyaKey + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    LblMsg = ""

    template_values = {
      'OyaKey'      :OyaKey
      ,'Rec'        :Rec
      ,'LblMsg'     : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa330.html')
    self.response.out.write(template.render(path, template_values))
#-------------------------------------------------------------
# ボタン押下時
#-------------------------------------------------------------
  def post(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""

    OyaKey = self.request.cookies.get('OyaKey', '') # CooKie取得

    self.DBSet()
    self.redirect("/Yasukawa320/?Key=" + OyaKey) #
    return
      
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
  def DBSet(self):  # データ保存

    Key    =  self.request.cookies.get('Key', '')    # Cookieより

    if Key == "":
      Rec = DatKeika() # 新規レコード
      Rec.OyaKey = self.request.cookies.get('OyaKey', '')
    else:
      Rec = DatKeika().GetRec(Key) # 更新

    Hizuke = Rec.Hizuke
      
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

    setattr(Rec,"BirthDay",common.WarekiHenkan(self,self.request.get("Tanzyoubi")))

    if Key == "": # 新規登録時
      Rec.Bango =  DatKeika().GetLastBango(Rec.OyaKey,Rec.Hizuke) + 1
    elif Rec.Hizuke != Hizuke: # 日付変更時,新規登録時は番号変更
      Rec.Bango =  DatKeika().GetLastBango(Rec.OyaKey,Rec.Hizuke) + 1

    Rec.put()

    return

#############################################################################
app = webapp2.WSGIApplication([
    ('/Yasukawa330/', MainHandler)
], debug=True)
