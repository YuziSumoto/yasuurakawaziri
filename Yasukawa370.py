#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール
import calendar

from MstUser          import *   # 使用者マスタ
from MstGyoumuSoudan  import *   # 業務区分・相談内容マスタ
from DatCase          import *   # 基本データ

class MainHandler(webapp2.RequestHandler):

  @login_required
#-------------------------------------------------------------
# 初期表示
#-------------------------------------------------------------
  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    # パラメタで日付取得→未指定なら当月
    Hizuke = self.request.get('Hizuke',datetime.date.today().strftime('%Y/%m/01'))
    cookieStr = 'Hizuke=' + Hizuke + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    Hizuke = datetime.datetime.strptime(Hizuke, '%Y/%m/%d')
    YokuGetu = Hizuke + datetime.timedelta(days=31) # 01日の31日後は絶対翌月
    ZenGetu  = Hizuke - datetime.timedelta(days=1)  # 01日の前日は絶対前月

    LblMsg = ""

    SnapCase = DatCase().GetMonthData(Hizuke.strftime('%Y/%m/%d'))

    template_values = {
      'Hizuke'   : Hizuke,
      'ZenGetu'  : ZenGetu.strftime('%Y/%m/01'),
      'YokuGetu' : YokuGetu.strftime('%Y/%m/01'),
      'Snap1'    : self.GetSoudansyaBetu(SnapCase),
      'Snap2'    : self.GetGyoumuKubunBetu(SnapCase),
      'LblMsg'   : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa370.html')
    self.response.out.write(template.render(path, template_values))
#-------------------------------------------------------------
# ボタン押下時
#-------------------------------------------------------------
  def post(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    LblMsg = ""

    KanzyaID = self.request.cookies.get('KanzyaID', '') # CooKie取得

    for param in self.request.arguments():
      if "BtnYasukawa" in param:
#        self.DBSet()
        KanzyaID = self.request.get("KanzyaID")
        self.redirect("/" + param.replace("Btn","") + "/?KanzyaID=" + str(KanzyaID)) #

    template_values = {
       'Rec'     : self.request.arguments()
      ,'MstTiiki'  : MstTiiki().GetAll()
      ,'MstKaigodo'  : MstKaigodo().GetAll()
      ,'MstKeitai'  : MstKeitai().GetAll()
      ,'LblMsg'  : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Yasukawa200.html')
    self.response.out.write(template.render(path, template_values))

#############################################################################
  def GetSoudansyaBetu(self,SnapCase):  # 相談者別内訳取得

    Titles = [["電話相談",""],
             ["面接相談","訪問"],
             ["面接相談","来所"],
             ["Total",""]]
    Snap = [] # リスト

    Kensu = []
    for Title in Titles: # 数値テーブル作成
      Kensu.append([0,0,0,0,0,0])

    for RecCase in SnapCase: #データ集計
      if RecCase.SoudanHouhou <= 2: # 集計対象外は無視
        Kensu[RecCase.SoudanHouhou][0] += 1
        if RecCase.SoudanSyaCD == 1: # 相談者:本人
          Kensu[RecCase.SoudanHouhou][1] += 1
        if RecCase.SoudanSyaCD == 2: # # 相談者:家族
          Kensu[RecCase.SoudanHouhou][2] += 1
        if RecCase.SoudanSyaCD == 3: # 相談者:関係機関
          Kensu[RecCase.SoudanHouhou][3] += 1
        if RecCase.SoudanSyaCD == 99: # 相談者:その他
          Kensu[RecCase.SoudanHouhou][4] += 1

        if RecCase.YakanKubun == True: # 相談者:その他
          Kensu[RecCase.SoudanHouhou][5] += 1
    for Ctr in range(6):
      Kensu[3][Ctr]  = Kensu[0][Ctr] + Kensu[1][Ctr] + Kensu[2][Ctr] 

    Ctr = 0
    for Title in Titles:
      Rec = {} # 辞書
      Rec["Title1"] = Title[0]
      Rec["Title2"] = Title[1]
      Rec["Kensu"] = Kensu[Ctr]
      Snap.append(Rec)
      Ctr += 1

    return Snap
#############################################################################
  def GetGyoumuKubunBetu(self,SnapCase):  # 相談者別内訳取得

    SnapMst = MstGyoumuSoudan().GetAll()

    Snap = [] # リスト

    Kensu = []
    for Rec in SnapMst: # 数値テーブル作成
      Kensu.append([0,0,0,0,0,0,0])

    OutRow1 = 0
    OutRow2 = 0
    OutCol  = 0
    
    for RecCase in SnapCase: #データ集計
      if RecCase.GyoumuCD == 1: # 総合相談支援業務
        OutRow1 = 0
        if RecCase.SoudanCD == 99: #その他 
          OutRow2 = 5
        else:
          OutRow2 = RecCase.SoudanCD
          
      if RecCase.GyoumuCD == 2: # 権利擁護業務
        OutRow1 = 6
        if RecCase.SoudanCD == 99: #その他 
          OutRow2 = 9
        else:
          OutRow2 = 6 + RecCase.SoudanCD
      if RecCase.GyoumuCD == 3: # 介護予防ケアマネジメント業務
        OutRow1 = 10
        if RecCase.SoudanCD == 99: #その他 
          OutRow2 = 13
        else:
          OutRow2 = 10 + RecCase.SoudanCD
      if RecCase.GyoumuCD == 4: # 包括的ケアマネジメント業務
        OutRow1 = 14
        OutRow2 = 15

      if RecCase.SoudanSyaCD < 99: # 相談者:その他
        OutCol = RecCase.SoudanSyaCD
      else:
        OutCol = 4

      Kensu[OutRow1][OutCol] += 1
      Kensu[OutRow2][OutCol] += 1

      if RecCase.NintiYouin == True: # 認知症要因
        if RecCase.NintiSuisin == True: # 認知症地域推進員対応
          Kensu[OutRow1][5] += 1
          Kensu[OutRow2][5] += 1
        else:                        # その他職員対応
          Kensu[OutRow1][6] += 1
          Kensu[OutRow2][6] += 1



    for WKensu in Kensu: # 件数セット
      WKensu[0] = WKensu[1] + WKensu[2] + WKensu[3] + WKensu[4]

    Ctr = 0
    for RecMst in SnapMst:
      Rec = {} # 辞書
      if RecMst.SoudanCD == 0: # 業務区分
        Rec["Title"] = RecMst.Name
        Rec["Align"] = "left"
      else: # 相談内容
        Rec["Title"] = u"　　　" + RecMst.Name
        Rec["Align"] = "right"

      Rec["Kensu"] = Kensu[Ctr]
      Snap.append(Rec)
      Ctr += 1

    Goukei = [0,0,0,0,0,0,0] # 合計分
    for Rec in Snap: # 件数セット
      if Rec["Align"] == "left":
        for Ctr in range(7):
          Goukei[Ctr] += Rec["Kensu"][Ctr]

    Rec = {} # 辞書
    Rec["Title"] = "ToTal"
    Rec["Kensu"] = Goukei
    Snap.append(Rec)

    return Snap
#############################################################################
app = webapp2.WSGIApplication([
    ('/Yasukawa370/', MainHandler)
], debug=True)
