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
from DatKeika    import *   # 経過データ

class MainHandler(webapp2.RequestHandler):

  @login_required

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""

    cookieStr = 'Key=' + self.request.get('Key') + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    template_values = {
      'Key'    : self.request.get('Key'),
      'Snap'   : DatKeika().GetAll(self.request.get('Key')),
      'LblMsg' : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa320.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""

    for param in self.request.arguments():
      if "BtnDel" in param:
        DatKeika().DelRec(param.replace("BtnDel",""))
        LblMsg = u"削除しました"

    Key = self.request.cookies.get('Key', '') # CooKie取得

    template_values = {
      'Key'    : Key,
      'Snap'   : DatKeika().GetAll(Key),
      'LblMsg' : LblMsg
                      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa320.html')
    self.response.out.write(template.render(path, template_values))

####################################################################################################

app = webapp2.WSGIApplication([
    ('/Yasukawa320/', MainHandler)
], debug=True)
