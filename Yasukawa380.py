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
from DatKaigi  import *   # 会議データ
from DatGeppou import *   # 基本データ


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

    # パラメタで日付取得→未指定なら当月
    Hizuke = self.request.get('Hizuke',datetime.date.today().strftime('%Y/%m/01'))
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Rec = self.DBGet(Hizuke)

    LblMsg = ""

    template_values = {
       'Rec'    : Rec
      ,'Hizuke' : datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
      ,'LblMsg' : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa380.html')
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

    Hizuke = self.request.cookies.get('Hizuke') # CooKie取得

    for param in self.request.arguments():
      if "BtnEnd" in param:
        self.DBSet(Hizuke)
        self.redirect("/Yasukawa370/?Hizuke=" + Hizuke) #

    Rec = {}

    template_values = {
       'Rec'    : Rec
      ,'Hizuke' : datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
      ,'LblMsg' : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa380.html')
    self.response.out.write(template.render(path, template_values))

#############################################################################
#------------------------------------------------------------------------------
  def DBGet(self,Hizuke):  # データ読み込み

    Snap = DatKaigi().GetList(Hizuke) # レコード読込

    RetRec = {}

    for Rec in Snap:
      RetRec["Hizuke" + str(Rec.Bango)] = Rec.Hizuke
      RetRec["Title" + str(Rec.Bango)] = Rec.Title
      RetRec["Naiyo" + str(Rec.Bango)] = Rec.Naiyo
      RetRec["Syusseki" + str(Rec.Bango)] = Rec.Syusseki
      RetRec["Kaisu" + str(Rec.Bango)] = Rec.Kaisu

    RetRec["KaisuKei"] = 0
    if RetRec["Kaisu6"] is not None:
      RetRec["KaisuKei"] +=  int(RetRec["Kaisu6"]) 
    if RetRec["Kaisu7"] is not None:
      RetRec["KaisuKei"] +=  int(RetRec["Kaisu7"]) 
    if RetRec["Kaisu8"] is not None:
      RetRec["KaisuKei"] +=  int(RetRec["Kaisu8"]) 
    if RetRec["Kaisu9"] is not None:
      RetRec["KaisuKei"] +=  int(RetRec["Kaisu9"]) 

    Snap = DatGeppou().GetList(Hizuke) # レコード読込

    for Rec in Snap:
      RetRec["Kensu" + str(Rec.Bango)] = Rec.Kensu

    RetRec["KensuKei1"] = 0
    if RetRec["Kensu12"] is not None:
      RetRec["KensuKei1"] +=  int(RetRec["Kensu12"]) 
    if RetRec["Kensu14"] is not None:
      RetRec["KensuKei1"] +=  int(RetRec["Kensu14"]) 
    if RetRec["Kensu16"] is not None:
      RetRec["KensuKei1"] +=  int(RetRec["Kensu16"]) 

    RetRec["KensuKei2"] = 0
    if RetRec["Kensu13"] is not None:
      RetRec["KensuKei2"] +=  int(RetRec["Kensu13"]) 
    if RetRec["Kensu15"] is not None:
      RetRec["KensuKei2"] +=  int(RetRec["Kensu15"]) 
    if RetRec["Kensu17"] is not None:
      RetRec["KensuKei2"] +=  int(RetRec["Kensu17"]) 

    return RetRec
#------------------------------------------------------------------------------
  def DBSet(self,Hizuke):  # データ保存

    DatKaigi().DelList(Hizuke) # 既存レコード削除

    for Ctr in range(10):

      Rec = DatKaigi() # 新規レコード
      Rec.Nengetu  = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
      if self.request.get("Hizuke" + str(Ctr)) != "":
        Rec.Hizuke   = datetime.datetime.strptime(self.request.get("Hizuke" + str(Ctr)), '%Y-%m-%d')
      Rec.Bango    = Ctr
      Rec.Title    = self.request.get("Title" + str(Ctr))
      Rec.Naiyo    = self.request.get("Naiyo" + str(Ctr))
      Rec.Syusseki = self.request.get("Syusseki" + str(Ctr))
      if  self.request.get("Kaisu" + str(Ctr)) != "":
        Rec.Kaisu    = int(self.request.get("Kaisu" + str(Ctr)))
      Rec.put()

    sql = DatGeppou().DelList(Hizuke) # 既存レコード削除
    for Ctr in range(19):

      Rec = DatGeppou() # 新規レコード
      Rec.Nengetu  = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
      Rec.Bango    = Ctr
      if  self.request.get("Kensu" + str(Ctr)) != "":
        Rec.Kensu    = int(self.request.get("Kensu" + str(Ctr)))
        Rec.put()

    return
  
#############################################################################
app = webapp2.WSGIApplication([
    ('/Yasukawa380/', MainHandler)
], debug=True)
