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

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""

    template_values = {
                       'Snap'  :MstTiiki().GetAll()
                      ,'LblMsg':LblMsg
                      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa910.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    LblMsg = ""

    for param in self.request.arguments():
      if "BtnDel" in param:
        MstTiiki().DelRec(param.replace("BtnDel",""))
        LblMsg = u"削除しました"

    template_values = {
                       'Snap'  :MstTiiki().GetAll()
                      ,'LblMsg':LblMsg
                      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa910.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/Yasukawa910/', MainHandler)
], debug=True)
