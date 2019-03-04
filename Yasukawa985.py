#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from MstUser   import *   # 使用者マスタ

from MstGyoumuSoudan import *   # 業務相談マスタ 
import datetime

#from dateutil import relativedelta

class MainHandler(webapp2.RequestHandler):

  @login_required

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg =  ""

    Key = self.request.get('Key',"")
    cookieStr = 'Key=' + self.request.get('Key') + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))


    if  Key == "":
      Rec = MstGyoumuSoudan() # 空レコード
    else:
      Rec = MstGyoumuSoudan().GetRecKey(Key)

    template_values = {
                       'Rec'     :Rec
                      ,'LblMsg'  :LblMsg
                      }

    path = os.path.join(os.path.dirname(__file__), 'Yasukawa985.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""
    MstGyoumuSoudan().DelRec(self.request.get('GyoumuCD'),self.request.get('SoudanCD'))

    Rec = MstGyoumuSoudan()
    Rec.GyoumuCD    = int(self.request.get('GyoumuCD'))
    Rec.SoudanCD    = int(self.request.get('SoudanCD'))
    Rec.Name        = self.request.get('Name')
    Rec.put()

    self.redirect("/Yasukawa980/")
    return

app = webapp2.WSGIApplication([
    ('/Yasukawa985/', MainHandler)
], debug=True)
