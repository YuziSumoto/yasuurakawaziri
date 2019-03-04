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
from DatSoudan   import *   # 相談データ
from DatKeika    import *   # 経過データ(相談データ削除時に該当データ削除)

class MainHandler(webapp2.RequestHandler):

  @login_required

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""

    Kubun = self.request.cookies.get('Kubun', '1') # CooKie取得
    cookieStr = 'Kubun=' + Kubun + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    template_values = {
      'Snap'    : DatSoudan().GetAll(Kubun),
      'Kubun'   : Kubun,
      'LblMsg'  : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa300.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""

    Kubun = self.request.get("Kubun","1")  # 画面選択
    cookieStr = 'Kubun=' + Kubun + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    for param in self.request.arguments():
      if "BtnDel" in param:  # 削除
        DatKeika().DelRecOya(param.replace("BtnDel",""))
        DatSoudan().DelRec(param.replace("BtnDel",""))
        LblMsg = u"削除しました"

    template_values = {
      'Snap'    : DatSoudan().GetAll(Kubun),
      'Kubun'   : Kubun,
      'LblMsg' : LblMsg
    }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa300.html')
    self.response.out.write(template.render(path, template_values))

####################################################################################################

app = webapp2.WSGIApplication([
    ('/Yasukawa300/', MainHandler)
], debug=True)
