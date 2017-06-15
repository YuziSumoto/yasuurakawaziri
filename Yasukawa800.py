#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# 注文者ＥＸＣＥＬ出力
#

import webapp2

#import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import datetime
import time
from calendar import monthrange
import locale

import xlwt # EXCEL 出力ライブラリ
import StringIO
import copy

# from MstUser   import *   # 使用者マスタ
from DatKihon     import *   # 患者基本データ
from DatByoureki  import *   # 病歴データ
from MstByoumei   import *   # 病名マスタ

class MainHandler(webapp2.RequestHandler):

#  @login_required

  def get(self):

#    user = users.get_current_user() # ログオン確認
#    if MstUser().ChkUser(user.email()) == False:
#      self.redirect(users.create_logout_url(self.request.uri))
#      return


    WorkBook =  self.ExcelSet()

    self.response.headers['Content-Type'] = 'application/ms-excel'
    self.response.headers['Content-Transfer-Encoding'] = 'Binary'
    self.response.headers['Content-disposition'] = 'attachment; filename="Yasukawa800.xls"'
    WorkBook.save(self.response.out)

  def ExcelSet(self):

    WorkBook = xlwt.Workbook()  # 新規Excelブック

    Style = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_CENTER) 
    font = xlwt.Font() # Create the Font
    font.height = 230
    Style.font = font

    WorkSheet = WorkBook.add_sheet(u"フェイスシート")  # シート追加
    self.SetPrintParam(WorkSheet) # 用紙サイズ等セット
    self.SetTitle(WorkSheet,Style)      # 固定部分セット

    SnapKihon = DatKihon().GetAll()
    Row = 3

    for RecKihon in SnapKihon:
      WorkSheet.write(Row,0,RecKihon.Tanto,Style)
      WorkSheet.write(Row,1,RecKihon.Kana + "\n" + RecKihon.Name,Style)
      if RecKihon.Sex == 1:
        WorkSheet.write(Row,2,u"男",Style)
      else:
        WorkSheet.write(Row,2,u"女",Style)
      WorkSheet.write(Row,3,RecKihon.Zyusyo.replace("<BR>","\n"),Style)
      WorkSheet.write(Row,4,RecKihon.Tel,Style)
      WorkSheet.write(Row,5,RecKihon.Soudanbi,Style)
      for Col in range(6,30):
        WorkSheet.write(Row,Col," ",Style)
      Row = self.SetByoureki(WorkSheet,str(RecKihon.key()),Row,Style)
      
      Row += 1

    return  WorkBook
  
  def SetPrintParam(self,WorkSheet): # 用紙サイズ・余白設定
    WorkSheet.set_paper_size_code(9) # A4
    WorkSheet.set_portrait(1) # 縦
    WorkSheet.top_margin = 0.9 / 2.54    # 1インチは2.54cm
    WorkSheet.bottom_margin = 0.5 / 2.54    # 1インチは2.54cm
    WorkSheet.left_margin = 0.8 / 2.54    # 1インチは2.54cm
    WorkSheet.right_margin = 0.5 / 2.54    # 1インチは2.54cm
    WorkSheet.header_str = ''
    WorkSheet.footer_str = ''
#    WorkSheet.fit_num_pages = 1
    return

  def SetColSize(self,WorkSheet,Col):  # 行,列サイズセット

    ColWidth = ["列の幅",2,10,10,9,2]
    for i in range(1,len(ColWidth)):
      WorkSheet.col(Col + i - 2).width = int(ColWidth[i] * 400)

    return

  def SetTitle(self,WorkSheet,Style):  # 固定部分セット

    StyleNoline = copy.deepcopy(Style)
    Border = xlwt.Borders()
    StyleNoline.borders = Border

    StyleNolineUnder = copy.deepcopy(Style)
    Border = xlwt.Borders()
    StyleNolineUnder.borders = Border
    StyleNolineUnder.font.underline = True

    Title = [u"担当",u"氏名",u"性別",u"生年月日",u"住所",u"電話",
             u"相談日",u"障害高齢者自立度",u"認知症高齢者自立度",
             u"認定",u"有効期限",u"前回介護度",u"基本チェックリスト",u"記入日",
             u"難病",u"家族関係の状況",
             u"本人の住居環境",u"経済状況",u"月額",
             u"相談者",u"続柄",u"相談者住所",u"相談者連絡先",
             u"緊急時氏名",u"緊急時続柄",u"緊急時住所",
             u"生活歴",u"趣味・楽しみ・特技",u"友人地域との関係",
             u"年月日",u"病名",u"医療機関",u"経過",u"治療内容",
             u"公的サービス",u"非公的サービス"
             ]
    Col = 0
    for strTitle in Title:
      WorkSheet.write(2,Col,strTitle,Style)
      Col += 1

    return

  def SetByoureki(self,WorkSheet,KihonKey,Row,Style):  # 病歴セット

    OutStr = ""
    for RecByoureki in DatByoureki().GetLast(KihonKey):
      if RecByoureki.ByoumeiCD == 0:
        WorkSheet.write(Row,30,RecByoureki.Byoumei,Style)
      else:
        Byoumei = MstByoumei().GetRec(RecByoureki.ByoumeiCD).Name       
        WorkSheet.write(Row,30,Byoumei,Style)
      WorkSheet.write(Row,31,RecByoureki.IryoKikan,Style)
      WorkSheet.write(Row,32,RecByoureki.Keika,Style)
      WorkSheet.write(Row,33,RecByoureki.Naiyo,Style)
      break

    return Row

  def SetData2(self,WorkSheet,Rec,Row,Style):  # データ部分セット

    Style2 = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_CENTER) 
    font = xlwt.Font() # Create the Font
    font.height = 130
    Style2.font = font

    StyleR = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_RIGHT) 
    font = xlwt.Font() # Create the Font
    font.height = 130
    StyleR.font = font

    WorkSheet.write(Row,0,Row - 1,Style2)
    WorkSheet.write(Row,1,Rec.Room,Style2)
    WorkSheet.write(Row,2,Rec.Name,Style2)

    Goukei = 0
    if Rec.Futan != None:
      Goukei -= Rec.Futan
      OutStr = int(Rec.Futan)
    else:
      OutStr = ""
    WorkSheet.write(Row,3,OutStr,StyleR) # 負担額

    if Rec.Haitu2Kei != None:
      Goukei += Rec.Haitu2Kei
      OutStr = int(Rec.Haitu2Kei)
    else:
      OutStr = ""

    WorkSheet.write(Row,4,int(Goukei),StyleR) # ハイツⅡ計-負担

    WorkSheet.write(Row,5,OutStr,StyleR) # ハイツ２計

    if Rec.Haitu2Kei != None:
      Goukei = Rec.Haitu2Kei
    else:
      Goukei = 0
      
    if Rec.Byouin != None:
      Goukei += Rec.Byouin
      OutStr = int(Rec.Byouin)
    else:
      OutStr = ""
    WorkSheet.write(Row,6,OutStr,StyleR)

    if Rec.Yakkyoku != None:
      Goukei += Rec.Yakkyoku
      OutStr = int(Rec.Yakkyoku)
    else:
      OutStr = ""
    WorkSheet.write(Row,7,OutStr,StyleR)

    if Rec.Byouin2 != None:
      Goukei += Rec.Byouin2
      OutStr = int(Rec.Byouin2)
    else:
      OutStr = ""
    WorkSheet.write(Row,8,OutStr,StyleR)

    OutStr = int(Goukei)
    WorkSheet.write(Row,9,OutStr,StyleR)

    if Rec.Ryosyubi != None:
      OutStr = Rec.Ryosyubi.strftime('%Y/%m/%d')
    else:
      OutStr = ""
    WorkSheet.write(Row,10,OutStr,StyleR)

    return

  def SetDataGoukei(self,WorkSheet,DataRecs,GoukeiOutCol,Style):  # データ部分セット

    OutStyle = copy.deepcopy(Style)
    OutStyle.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    OutStyle.pattern.pattern_fore_colour = xlwt.Style.colour_map['gray50']
    OutStyle.font.colour_index = xlwt.Style.colour_map['white']
    
    WorkSheet.write(3,GoukeiOutCol,u"合計",OutStyle)

    OutRow = 4
    for DataRec in DataRecs:
      WorkSheet.write(OutRow,GoukeiOutCol,getattr(DataRec,"Goukei",0),Style)
      OutRow += 1

    return

  def SetStyle(self,Top,Bottom,Right,Left,Vert,Horz):  # セルスタイルセット

    Style = xlwt.XFStyle()
    Border = xlwt.Borders()
    if Top == "THIN":
      Border.top     = xlwt.Borders.THIN
    elif Top == "DOTTED":
      Border.top     = xlwt.Borders.DOTTED

    if Bottom == "THIN":
      Border.bottom  = xlwt.Borders.THIN
    elif Bottom == "DOTTED":
      Border.bottom     = xlwt.Borders.DOTTED

    if   Left == "THIN":
      Border.left    = xlwt.Borders.THIN
    elif Left == "DOTTED":
      Border.left    = xlwt.Borders.DOTTED

    if   Right == "THIN":
      Border.right   = xlwt.Borders.THIN
    elif Right == "DOTTED":
      Border.right   = xlwt.Borders.DOTTED

    Style.borders = Border

    Alignment      = xlwt.Alignment()

    Alignment.wrap = 1 # これないとセル内改行が効かない

    if Vert != False:
      Alignment.vert = Vert

    if Horz != False:
      Alignment.horz = Horz

    Style.alignment = Alignment

    return Style

app = webapp2.WSGIApplication([
    ('/Yasukawa800/', MainHandler)
], debug=True)
