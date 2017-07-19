#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import webapp2
import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from MstUser   import *   # 使用者マスタ (利用者チェック用)

import wsgiref.handlers
import os
import csv
from StringIO import StringIO

from DatKihon   import *  # 患者基本情報
from DatSeikatu import *  # 患者生活情報
import datetime

class MainHandler(webapp2.RequestHandler):

  @login_required # ログインしてないとダメ！

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    template_values = {'Msg': ""
                      }
    path = os.path.join(os.path.dirname(__file__), "Yasukawa990.html")
    self.response.out.write(template.render(path, template_values))

  def post(self):

    Msg  = "bbb"

    Sql =  "SELECT * FROM DatKihon"   # 現データ削除(基本情報)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
      Rec.delete()

    Sql =  "SELECT * FROM DatSeikatu"   # 現データ削除(生活情報)
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
      Rec.delete()

    rawfile = self.request.get('file')
    csvfile = csv.reader(StringIO(rawfile))
    for row in csvfile:
      if unicode(row[0], 'cp932').isnumeric() == False:
        continue # 数値以外は無視

      Msg +=  unicode(row[0], 'cp932') + " "

      # 基本情報
      Rec = DatKihon(
            KanzyaID         = int(unicode(row[0], 'cp932')),
            Tanto            = unicode(row[1], 'cp932'),
            Name             = unicode(row[8], 'cp932'),
            Zyusyo           = unicode(row[13], 'cp932'),
            Tel              = unicode(row[14], 'cp932').replace("\n",","),
            KinkyuName1      = unicode(row[33], 'cp932').replace("\n",","),
            KinkyuZokugara1  = unicode(row[34], 'cp932').replace("\n",","),
            KinkyuZyusyo1    = unicode(row[35], 'cp932').replace("\n",","),
            KinkyuTel1       = unicode(row[35], 'cp932').replace("\n",","),
            KinkyuName2      = unicode(row[36], 'cp932').replace("\n",","),
            KinkyuZokugara2  = unicode(row[37], 'cp932').replace("\n",","),
            KinkyuZyusyo2    = unicode(row[38], 'cp932').replace("\n",","),
            KinkyuTel2       = unicode(row[38], 'cp932').replace("\n",","),
            KinkyuName3      = unicode(row[39], 'cp932').replace("\n",","),
            KinkyuZokugara3  = unicode(row[40], 'cp932').replace("\n",","),
            KinkyuZyusyo3    = unicode(row[41], 'cp932').replace("\n",","),
            KinkyuTel3       = unicode(row[41], 'cp932').replace("\n",","),
            KinkyuName4      = unicode(row[42], 'cp932').replace("\n",","),
            KinkyuZokugara4  = unicode(row[43], 'cp932').replace("\n",","),
            KinkyuZyusyo4    = unicode(row[44], 'cp932').replace("\n",","),
            KinkyuTel4       = unicode(row[44], 'cp932').replace("\n",","),
            Kaisu            = unicode(row[4], 'cp932'),
            Zyokyo           = unicode(row[6], 'cp932'),
            Sisetu           = unicode(row[7], 'cp932')
      )

      Rec.BirthDay = datetime.datetime.strptime(unicode(row[10], 'cp932'), '%Y/%m/%d')
      Rec.Soudanbi = datetime.datetime.strptime(unicode(row[2], 'cp932'), '%Y/%m/%d')

      if unicode(row[9], 'cp932') == "M": # 性別
        Rec.Sex = 1
      else:
        Rec.Sex = 2

      if unicode(row[17], 'cp932') == u"要支1": # 認定
        Rec.Kaigodo = 1
      elif unicode(row[17], 'cp932') == u"要支2": # 認定
        Rec.Kaigodo = 2
      elif unicode(row[17], 'cp932') == u"要介1": # 認定
        Rec.Kaigodo = 3
      elif unicode(row[17], 'cp932') == u"要介2": # 認定
        Rec.Kaigodo = 4
      elif unicode(row[17], 'cp932') == u"要介3": # 認定
        Rec.Kaigodo = 5
      elif unicode(row[17], 'cp932') == u"要介4": # 認定
        Rec.Kaigodo = 6
      elif unicode(row[17], 'cp932') == u"要介5": # 認定
        Rec.Kaigodo = 7
      elif unicode(row[17], 'cp932') == u"未申請": # 認定
        Rec.Kaigodo = 0

      if unicode(row[3], 'cp932') == u"電話":   # 相談形態
        Rec.Keitai = 1
      elif unicode(row[3], 'cp932') == u"訪問": 
        Rec.Keitai = 2
      elif unicode(row[3], 'cp932') == u"来所": 
        Rec.Keitai = 3
      else:
        Rec.Keitai = 9
        
      if unicode(row[18], 'cp932') != "":
        Rec.HokenStart = common.WarekiHenkan(self,unicode(row[18], 'cp932'))
      if unicode(row[19], 'cp932') != "":
        Rec.HokenEnd = common.WarekiHenkan(self,unicode(row[19], 'cp932'))
      
      Rec.put()

      # 生活情報
      Rec = DatSeikatu(
            KanzyaID    = int(unicode(row[0], 'cp932')),
            Soudansya   = unicode(row[29], 'cp932').replace("\n",",")[0:500],
            SoudanHoka  = unicode(row[30], 'cp932').replace("\n",",")[0:500],
            SoudanZ     = unicode(row[31], 'cp932').replace("\n",",")[0:500],
            SoudanR     = unicode(row[32], 'cp932').replace("\n",",")[0:500],
            Kazoku      = unicode(row[45], 'cp932').replace("\n",",")[0:500],
            Syumi       = unicode(row[48], 'cp932')[0:500],
            SeikatuReki = unicode(row[46], 'cp932')[0:500],
            Seikatu     = unicode(row[47], 'cp932')[0:500],
            Yuzin       = unicode(row[49], 'cp932')[0:500],
            Zyutaku     = unicode(row[22], 'cp932')[0:500],
            Kaisyu      = unicode(row[23], 'cp932')[0:500],
      )
      Rec.put()
      
      Msg +=  unicode(row[0], 'cp932') + " "
      Msg +=  unicode(row[1], 'cp932') + " "
      Msg +=  unicode(row[8], 'cp932') + "<BR>"
      
    template_values = {'Msg': Msg
                       }
    path = os.path.join(os.path.dirname(__file__), "Yasukawa990.html")
    self.response.out.write(template.render(path, template_values))

    return
  
app = webapp2.WSGIApplication([
    ('/Yasukawa990/', MainHandler)
], debug=True)
