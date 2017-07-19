#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール

from MstUser      import *   # 使用者マスタ
from DatKihon     import *   # 患者基本データ
from DatByoureki  import *   # 病歴データ
from MstByoumei   import *   # 病名マスタ

class MainHandler(webapp2.RequestHandler):

  @login_required

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    if self.request.get('KanzyaID') != "":
      KanzyaID = self.request.get('KanzyaID')
      cookieStr = 'KanzyaID=' + KanzyaID + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
    else:
      KanzyaID = self.request.cookies.get('KanzyaID', '')

    LblMsg = ""

    Snap = DatByoureki().GetList(KanzyaID)
    for Rec in Snap:
      if Rec.Byoumei =="":
        Rec.Byoumei = MstByoumei().GetRec(Rec.ByoumeiCD).Name
      Rec.IryoKikan = Rec.IryoKikan.replace("\n","<BR>")
      Rec.Keika = Rec.Keika.replace("\n","<BR>")
      Rec.Naiyo = Rec.Naiyo.replace("\n","<BR>")

    template_values = {
                       'Kihon'    : DatKihon().GetRec(KanzyaID),
                       'Snap'     : Snap
                      ,'LblMsg'   : LblMsg
                      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa220.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = " "

    KanzyaID = self.request.cookies.get('KanzyaID', '') # CooKie取得

    for param in self.request.arguments(): 
      if "BtnDel" in param:  # 削除ボタン？
        DatByoureki().DelRec(param.replace("BtnDel",""))
        LblMsg = "削除しました"

    Snap = DatByoureki().GetList(KanzyaID)
    for Rec in Snap:
      if Rec.Byoumei =="":
        Rec.Byoumei = MstByoumei().GetRec(Rec.ByoumeiCD).Name
      Rec.IryoKikan = Rec.IryoKikan.replace("\n","<BR>")
      Rec.Keika = Rec.Keika.replace("\n","<BR>")
      Rec.Naiyo = Rec.Naiyo.replace("\n","<BR>")

    template_values = {
                       'Kihon'    : DatKihon().GetRec(KanzyaID),
                       'Snap'     : Snap
                      ,'LblMsg'   : LblMsg
                      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa220.html')
    self.response.out.write(template.render(path, template_values))

####################################################################################################

app = webapp2.WSGIApplication([
    ('/Yasukawa220/', MainHandler)
], debug=True)
