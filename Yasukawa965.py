#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from MstUser   import *   # 使用者マスタ

from MstService import *
import datetime

#from dateutil import relativedelta

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg =  ""

    cookieStr = 'CD=' + self.request.get('CD') + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))


    if  self.request.get('CD') == "":
      Rec = MstService() # 空レコード
    else:
      Rec = MstService().GetRec(self.request.get('CD'))

    template_values = {
                       'Rec'     :Rec
                      ,'LblMsg'  :LblMsg
                      }

    path = os.path.join(os.path.dirname(__file__), 'Yasukawa965.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""
    MstService().DelRec(self.request.get('CD'))

    Rec = MstService()
    Rec.CD    = int(self.request.get('CD'))
    Rec.Kubun = int(self.request.get('Kubun'))
    Rec.Name  = self.request.get('Name')
    Rec.put()

    self.redirect("/Yasukawa960/")
    return

app = webapp2.WSGIApplication([
    ('/Yasukawa965/', MainHandler)
], debug=True)
