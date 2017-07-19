#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール

from MstUser    import *   # 使用者マスタ
from DatKihon     import *   # 患者基本データ
from DatService import *   # サービスデータ

class MainHandler(webapp2.RequestHandler):

  @login_required

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    if self.request.get('KanzyaID') != "": # キー保存
      KanzyaID = self.request.get('KanzyaID')
      cookieStr = 'KanzyaID=' + KanzyaID + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
    else:
     KanzyaID = self.request.cookies.get('KanzyaID', '')

    LblMsg = ""

    template_values = {
                       'Kihon'    : DatKihon().GetRec(KanzyaID),
                       'Snap'   : DatService().GetList(KanzyaID),
                       'LblMsg' : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa230.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = " "

    KanzyaID = self.request.cookies.get('KanzyaID', '') # CooKie取得

    for param in self.request.arguments(): 
      if "BtnDel" in param:  # 削除ボタン？
        DatService().DelRec(param.replace("BtnDel",""))
        LblMsg = "削除しました"

    template_values = {
                       'Kihon'  : DatKihon().GetRec(KanzyaID),
                       'Snap'   : DatService().GetList(KanzyaID),
                       'LblMsg' : LblMsg
                      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa230.html')
    self.response.out.write(template.render(path, template_values))

####################################################################################################
app = webapp2.WSGIApplication([
    ('/Yasukawa230/', MainHandler)
], debug=True)
