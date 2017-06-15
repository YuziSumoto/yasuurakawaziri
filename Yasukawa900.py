#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール

from MstUser   import *   # 使用者マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

    LblMsg = ""

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return

    template_values = {
      'LblMsg'    : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa900.html')
    self.response.out.write(template.render(path, template_values))

################################################################################

app = webapp2.WSGIApplication([
    ('/Yasukawa900/', MainHandler),
], debug=True)
