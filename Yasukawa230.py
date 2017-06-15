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

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    if self.request.get('Key') != "": # キー保存
      KihonKey = self.request.get('Key')
      cookieStr = 'Key=' + KihonKey + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
    else:
     KihonKey = self.request.cookies.get('Key', '')

    LblMsg = ""

    template_values = {
                       'Kihon'    : DatKihon().GetRec(KihonKey),
                       'Snap'   : DatService().GetList(KihonKey),
                       'LblMsg' : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa230.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = " "

    KihonKey = self.request.cookies.get('Key', '') # CooKie取得

    for param in self.request.arguments(): 
      if "BtnDel" in param:  # 削除ボタン？
        DatService().DelRec(param.replace("BtnDel",""))
        LblMsg = "削除しました"

    template_values = {
                       'Kihon'  : DatKihon().GetRec(KihonKey),
                       'Snap'   : DatService().GetList(KihonKey),
                       'LblMsg' : LblMsg
                      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa230.html')
    self.response.out.write(template.render(path, template_values))

####################################################################################################

#  テーブルセット
  def TableSet(self,Hizuke):

    retStr = ""

#    Snap = DatSoudan().GetMonthList(Hizuke)
    Snap = DatSoudan().GetAll()

#    for Ctr in range(1,10):
    for Rec in Snap:

      retStr += "<TR>"

      retStr += "<TD>"    # 更新ボタン（患者コード)
      retStr += u"<input type='submit' value = '更新'"
      retStr += " name='BtnSelect"
      retStr += str(Rec.key())
      retStr += "' style='width:80px'>"
      retStr += "</TD>"

      retStr += "<TD>"    # 患者名
      retStr += Rec.Hizuke.strftime('%Y/%m/%d')
      retStr += "</TD>"

      retStr += "<TD>"    # 患者名
      retStr += Rec.Name
      retStr += "</TD>"

      retStr += "<TD>"    # 印刷ボタン（患者コード)
      retStr += u"<input type='button' value = '印刷'"
      retStr += "onclick='window.open("
      retStr += '"/Ninchi025/'
      retStr += "?Key=" + str(Rec.key())
      retStr += '"'
      retStr += ");'"
      retStr += " style='width:50px'>"
      retStr += "</TD>"
      retStr += "<TD>"    # 削除ボタン（患者コード)
      retStr += u"<input type='submit' value = '削除'"
      retStr += "' name='BtnDel" 
      retStr += str(Rec.key())
      retStr += "' style='width:50px'>"
      retStr += "</TD>"

      retStr += "</TR>"

    return retStr

app = webapp2.WSGIApplication([
    ('/Yasukawa230/', MainHandler)
], debug=True)
