#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from MstUser   import *   # 使用者マスタ

from MstTiiki import *
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

    cookieStr = 'Key=' + self.request.get('Key') + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))


    if  self.request.get('Key') == "":
      Rec = MstTiiki() # 空レコード
    else:
      Rec = MstTiiki().GetRec(self.request.get('Key'))

    template_values = {
                       'MstTiiki':Rec
                      ,'LblMsg'  :LblMsg
                      }

    path = os.path.join(os.path.dirname(__file__), 'Yasukawa915.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""
    Key = self.request.cookies.get('Key', '')
    if Key != "":
      MstTiiki().DelRec(Key)

    Rec = MstTiiki()
    Rec.CD   = int(self.request.get('CD'))
    Rec.Name = self.request.get('Name')
    Rec.put()

    self.redirect("/Yasukawa910/")
    return

app = webapp2.WSGIApplication([
    ('/Yasukawa915/', MainHandler)
], debug=True)
