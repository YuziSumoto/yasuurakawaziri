#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール

from MstUser     import *   # 使用者マスタ
from MstByoumei  import *   # 病名マスタ
from DatByoureki import *   # 病歴データ
from DatKihon    import *   # 患者基本データ

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

    if self.request.get('KanzyaID')  != "":
      KanzyaID = self.request.get('KanzyaID')   # 利用者番号
      cookieStr = 'KanzyaID=' + KanzyaID + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    if self.request.get('Key') == "": # パラメタ無し？
      Key = ""
    else:
      Key = self.request.get('Key')   # パラメタ取得
    cookieStr = 'Key=' + Key + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))


    LblMsg = "内容を指定し、決定を押してください。"

    template_values = {
      'Kihon'      : DatKihon().GetRec(KanzyaID),
      'Rec'        : DatByoureki().GetRec(Key),
      'MstByoumei' : MstByoumei().GetAll(),
      'LblMsg'     : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa225.html')
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

    Key = self.request.cookies.get('Key', '') # CooKie取得
    KanzyaID = self.request.cookies.get('KanzyaID', '') # CooKie取得

    ErrFlg,LblMsg = self.ChkInput() # 入力チェック
    if ErrFlg == False: # エラー無し
      self.DBSet()
      self.redirect("/Yasukawa220/?KanzyaID=" + KanzyaID) # 一覧に戻る
      return

    Rec = {}
    ParaNames = self.request.arguments()
    for ParaName in ParaNames: # 前画面項目引き渡し
      Rec[ParaName]    = self.request.get(ParaName)
    Rec["ByoumeiCD"] = int(Rec["ByoumeiCD"])
    if  Rec["Hizuke"] != "":
      if common.CheckDate(self,self.request.get('Hizuke')) == True:
        Rec["Hizuke"] = datetime.datetime.strptime(Rec["Hizuke"], '%Y/%m/%d')
    
    template_values = {
      'Kihon'      : DatKihon().GetRec(KanzyaID),
      'Rec'        : Rec,
      'MstByoumei' : MstByoumei().GetAll(),
      'LblMsg'     : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa225.html')
    self.response.out.write(template.render(path, template_values))

#############################################################################
#------------------------------------------------------------------------------
  def ChkInput(self):   # 入力チェック

    ErrFlg = False
    LblMsg = ""

#    if common.CheckDate(self,self.request.get('Hizuke').replace("-","/")) == False:
#      LblMsg = "年月日が正しくありませんでした。(yyyy/mm/dd)"
#    else:
#      ErrFlg = False

    return (ErrFlg,LblMsg)

#------------------------------------------------------------------------------
  def DBSet(self):  # データ保存

    Key = self.request.cookies.get('Key', '') # CooKie取得
    KanzyaID = self.request.cookies.get('KanzyaID', '') # CooKie取得

    if Key == "":
      Rec = DatByoureki() # 新規レコード
    else:
      Rec = DatByoureki().GetRec(Key) # 更新

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

    Rec.KanzyaID = int(KanzyaID)
    key = Rec.put()
    
    return

#############################################################################
app = webapp2.WSGIApplication([
    ('/Yasukawa225/', MainHandler)
], debug=True)
