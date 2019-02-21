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
from DatCase   import *   # 基本データ

from MstSoudanSya     import *   # 相談者マスタ
from MstTanto         import *   # 担当者マスタ
from MstKeitai        import *   # 相談形態マスタ
from MstGyoumuSoudan  import *   # 業務・相談マスタ
from MstKakuninSyo    import *   # 確認書マスタ

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

    if self.request.get('Key') != "": # 更新モード
      cookieStr = 'Key=' + self.request.get('Key') + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
      Rec = DatCase().GetRec(self.request.get('Key'))
      Hizuke = Rec.Hizuke.strftime('%Y/%m/%d')
      cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    else: # 新規登録モード
      cookieStr = 'Key=;'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
      Hizuke = self.request.get('Hizuke')
      cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
      Rec = DatCase() # 空レコード
      Rec.GyoumuCD = 1

    LblMsg = ""

    template_values = {
      'Hizuke'          : Hizuke
      ,'Rec'            : Rec
      ,'MstSoudanSya'   : MstSoudanSya().GetAll()
      ,'MstTanto'       : MstTanto().GetAll()
      ,'MstKeitai'      : MstKeitai().GetAll()
      ,'MstGyoumu'      : MstGyoumuSoudan().GetGyoumu()
      ,'MstSoudan'      : MstGyoumuSoudan().GetSoudan(Rec.GyoumuCD)
      ,'MstKakuninSyo'  : MstKakuninSyo().GetAll()
      ,'LblMsg'         : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa360.html')
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

    Key = self.request.cookies.get('Key') # CooKie取得
    Hizuke = self.request.cookies.get('Hizuke') # CooKie取得

    for param in self.request.arguments():
      if "BtnEnd" in param:
        self.DBSet(True) # DB更新
        self.redirect("/Yasukawa350/?Hizuke=" + Hizuke) #

    Rec = self.DBSet(False) # レコードセットのみ
      
    template_values = {
      'Hizuke'          : Hizuke
      ,'Rec'            : Rec
      ,'MstSoudanSya'   : MstSoudanSya().GetAll()
      ,'MstTanto'       : MstTanto().GetAll()
      ,'MstKeitai'      : MstKeitai().GetAll()
      ,'MstGyoumu'      : MstGyoumuSoudan().GetGyoumu()
      ,'MstSoudan'      : MstGyoumuSoudan().GetSoudan(Rec.GyoumuCD)
      ,'MstKakuninSyo'  : MstKakuninSyo().GetAll()
      ,'LblMsg'         : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa360.html')
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
  def DBSet(self,SaveFlg):  # データ保存

    Key =  self.request.cookies.get('Key') # Cookieより
    if Key == "": # 新規登録
      Rec = DatCase() # 新規レコード
      Rec.Hizuke= datetime.datetime.strptime(self.request.cookies.get('Hizuke'), '%Y/%m/%d')
    else:
      Rec = DatCase().GetRec(Key) # 更新

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

    if SaveFlg == True:
      Ret = Rec.put()

    return Rec

#############################################################################
app = webapp2.WSGIApplication([
    ('/Yasukawa360/', MainHandler)
], debug=True)
