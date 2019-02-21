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
from DatCase     import *   # ケースデータ

class MainHandler(webapp2.RequestHandler):

  @login_required

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""

    # パラメタで日付取得→未指定なら当日
    Hizuke = self.request.get('Hizuke',datetime.date.today().strftime('%Y/%m/%d'))
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
    Yokuzitu = Hizuke - datetime.timedelta(days=-1)
    Zenzitu  = Hizuke - datetime.timedelta(days=+1)

    template_values = {
      'Hizuke'   : Hizuke.strftime('%Y/%m/%d'),
      'Zenzitu'  : Zenzitu.strftime('%Y/%m/%d'),
      'Yokuzitu' : Yokuzitu.strftime('%Y/%m/%d'),
      'Snap'     : DatCase().GetList(Hizuke.strftime('%Y/%m/%d')),
      'LblMsg'   : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa350.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""

    for param in self.request.arguments():
      if "BtnDel" in param:
        DatCase().DelRec(param.replace("BtnDel",""))
        LblMsg = u"削除しました"

    Hizuke = self.request.cookies.get('Hizuke') # CooKie取得
    Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
    Yokuzitu = Hizuke - datetime.timedelta(days=-1)
    Zenzitu  = Hizuke - datetime.timedelta(days=+1)

    template_values = {
      'Hizuke'   : Hizuke.strftime('%Y/%m/%d'),
      'Zenzitu'  : Zenzitu.strftime('%Y/%m/%d'),
      'Yokuzitu' : Yokuzitu.strftime('%Y/%m/%d'),
      'Snap'     : DatCase().GetList(Hizuke.strftime('%Y/%m/%d')),
      'LblMsg'   : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa350.html')
    self.response.out.write(template.render(path, template_values))

####################################################################################################

app = webapp2.WSGIApplication([
    ('/Yasukawa350/', MainHandler)
], debug=True)
