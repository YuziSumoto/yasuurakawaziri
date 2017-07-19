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
    self.response.headers['Content-disposition'] = 'attachment; filename="Yasukawa815.xls"'
    WorkBook.save(self.response.out)

  def ExcelSet(self):

    WorkBook = xlwt.Workbook()  # 新規Excelブック

    Style = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_CENTER) 
    font = xlwt.Font() # Create the Font
    font.height = 230
    Style.font = font

    WorkSheet = WorkBook.add_sheet(u"フェイスシート1")  # シート追加
    self.SetPrintParam(WorkSheet)   # 用紙サイズ等セット
    self.SetColSize(WorkSheet)      # 列幅セット
    self.SetTitle(WorkSheet,Style)  # 固定部分セット(１枚目)
    self.SetData(WorkSheet,Style)  # データセット(２枚目)
    WorkSheet = WorkBook.add_sheet(u"フェイスシート2")  # シート追加
#    self.SetTitle2(WorkSheet,Style)  # 固定部分セット(１枚目)
#    self.SetData2(WorkSheet,Style)  # データセット(２枚目)

#    SnapKihon = DatKihon().GetAll()
    
#    WorkSheet.write(Row,0,RecKihon.Tanto,Style)
#    WorkSheet.write(Row,1,RecKihon.Kana + "\n" + RecKihon.Name,Style)
#    if RecKihon.Sex == 1:
#      WorkSheet.write(Row,2,u"男",Style)
#    else:
#      WorkSheet.write(Row,2,u"女",Style)
#    WorkSheet.write(Row,3,RecKihon.Zyusyo.replace("<BR>","\n"),Style)
#    WorkSheet.write(Row,4,RecKihon.Tel,Style)
#    WorkSheet.write(Row,5,RecKihon.Soudanbi,Style)
#    for Col in range(6,30):
#      WorkSheet.write(Row,Col," ",Style)
#    Row = self.SetByoureki(WorkSheet,RecKihon.KanzyaID,Row,Style)

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

  def SetColSize(self,WorkSheet):  # 行,列サイズセット

    for i in range(0,34):
      WorkSheet.col(i).width = int(2.5 * 400)

    return

  def SetTitle(self,WorkSheet,Style):  # 固定部分セット

    StyleNoline = copy.deepcopy(Style)
    Border = xlwt.Borders()
    StyleNoline.borders = Border

    StyleNolineUnder = copy.deepcopy(Style)
    Border = xlwt.Borders()
    StyleNolineUnder.borders = Border
    StyleNolineUnder.font.underline = True

    WorkSheet.write_merge(1,1,0 ,32,u"利用者基本情報",StyleNoline)
    WorkSheet.write_merge(4,4,21 ,25,u"作成担当者",StyleNoline)
    WorkSheet.write_merge(6,6,0 ,6,u"《 基本情報 》",StyleNoline)
    WorkSheet.write_merge(6,6,21 ,25,u"利用者番号",StyleNoline)

    WorkSheet.write_merge(8,9,0 ,5,u"相談日",Style)
    WorkSheet.write_merge(10,10,0 ,5,u"本人の状況",Style)
    WorkSheet.write_merge(11,11,0 ,5,u"フリガナ",Style)
    WorkSheet.write_merge(12,12,0 ,5,u"本人氏名",Style)
    WorkSheet.write_merge(13,14,0 ,5,u"住所",Style)
    WorkSheet.write_merge(13,13,21,22,u"Tel",Style)
    WorkSheet.write_merge(14,14,21,22,u"Fax",Style)


    WorkSheet.write_merge(15,16,0 , 5,u"日常生活\n自立度",Style)
    WorkSheet.write_merge(15,15,6 ,15,u"障害高齢者の日常生活自立度",Style)
    WorkSheet.write_merge(16,16,6 ,15,u"認知症高齢者の日常生活自立度",Style)
    WorkSheet.write_merge(17,18,0 , 5,u"認定情報",Style)
    WorkSheet.write_merge(19,19,0 , 5,u"障害等認定",Style)
    WorkSheet.write_merge(19,19,6 , 8,u"身障(",StyleNoline)
    WorkSheet.write_merge(19,19,11,13,u"),療育(",StyleNoline)
    WorkSheet.write_merge(19,19,16,18,u"),精神(",StyleNoline)
    WorkSheet.write_merge(19,19,21,23,u"),難病(",StyleNoline)
    WorkSheet.write_merge(19,19,26,28,u"),その他(",StyleNoline)
    WorkSheet.write_merge(19,19,32,33,u")",Style)


    WorkSheet.write_merge(20,20,0 ,5,u"本人の住宅環境",Style)
    WorkSheet.write_merge(21,21,0 ,5,u"経済状況",Style)
    WorkSheet.write_merge(22,23,0 ,5,u"来所者\n(相談者)",Style)

    WorkSheet.write_merge(24,25,0 ,5,u"住所",Style)
    WorkSheet.write_merge(26,26,0 ,5,u"連絡先",Style)
    WorkSheet.write_merge(24,26,17 ,17,u"続柄",Style)

    WorkSheet.write_merge(27,35,0 ,5,u"緊急連絡先",Style)
    WorkSheet.write_merge(27,27,6 ,10,u"氏名",Style)
    WorkSheet.write_merge(27,27,11,12,u"続柄",Style)
    WorkSheet.write_merge(27,27,13 ,20,u"住所・連絡先",Style)

    WorkSheet.write_merge(22,35,21 ,21,u"家族構成",Style)
    WorkSheet.write_merge(22,22,22 ,25,u"家族構成",StyleNoline)
    WorkSheet.write_merge(22,22,28 ,33,u"◎＝本人，○＝女性，□＝男性",StyleNoline)
    WorkSheet.write_merge(23,23,28 ,33,u"●■＝死亡，☆＝ｷｰﾊﾟｰｿﾝ",StyleNoline)
    WorkSheet.write_merge(24,24,28 ,33,u"主介護者に　「主」",StyleNoline)
    WorkSheet.write_merge(25,25,28 ,33,u"副介護者に　「副」",StyleNoline)
    WorkSheet.write_merge(26,26,28 ,33,u"（同居家族は○で囲む)",StyleNoline)

    WorkSheet.write_merge(32,32,22 ,25,u"家族関係等の状況",StyleNoline)

    return


  def SetData(self,WorkSheet,Style):  # 固定部分セット

    StyleNoline = copy.deepcopy(Style)
    Border = xlwt.Borders()
    StyleNoline.borders = Border

    StyleNolineUnder = copy.deepcopy(Style)
    Border = xlwt.Borders()
    StyleNolineUnder.borders = Border
    StyleNolineUnder.font.underline = True

    WorkSheet.write_merge(4,4,26 ,32,u"担当者01",StyleNoline)
    WorkSheet.write_merge(6,6,26 ,32,u"1234567",StyleNoline)

    WorkSheet.write_merge(8,9,6 ,15,u"2017年06月30日",Style)
    WorkSheet.write_merge(8,8,16 ,24,u"来所・電話",Style)
    WorkSheet.write_merge(9,9,16 ,24,u"その他(）",Style)
    WorkSheet.write_merge(8,8,25 ,33,u"初回",Style)
    WorkSheet.write_merge(9,9,25 ,33,u"再来（前　／　　）",Style)

    WorkSheet.write_merge(10,10,6 ,33,u"在宅・入院又は入所中（　　　）",Style)

    WorkSheet.write_merge(11,11, 6 ,15,u"カンジャメイ０１",Style)
    WorkSheet.write_merge(12,12, 6 ,15,u"患者氏名０１",Style)
    WorkSheet.write_merge(11,12,16 ,19,u"男・女",Style)
    WorkSheet.write_merge(11,12,20 ,33,u"Ｓ４０年１２月３１日生（９９９）歳",Style)

    WorkSheet.write_merge(13,14,6 ,20,u"住所０１",Style)

    WorkSheet.write_merge(13,13,23,33,u"0823-70-0555",Style)
    WorkSheet.write_merge(14,14,23,33,u"0923-70-0557",Style)


    WorkSheet.write_merge(15,15,16 ,33,u"Ｂ２",Style)
    WorkSheet.write_merge(16,16,16 ,33,u"Ⅱｂ",Style)

    WorkSheet.write_merge(17,17,6 ,33,u"要支援１",Style)
    WorkSheet.write_merge(18,18,6 ,33,u"有効期限",Style)

    WorkSheet.write_merge(19,19, 9,10,u"〇",StyleNoline)
    WorkSheet.write_merge(19,19,14,15,u"〇",StyleNoline)
    WorkSheet.write_merge(19,19,19,20,u"〇",StyleNoline)
    WorkSheet.write_merge(19,19,24,25,u"〇",StyleNoline)
    WorkSheet.write_merge(19,19,30,31,u"〇",StyleNoline)

    WorkSheet.write_merge(20,20,6 ,33,u"自宅",Style)

    WorkSheet.write_merge(21,21,6 ,8,u"国民年金",Style)
    WorkSheet.write_merge(21,21,9 ,11,u"国民年金",Style)
    WorkSheet.write_merge(21,21,12,14,u"国民年金",Style)
    WorkSheet.write_merge(21,21,15,17,u"国民年金",Style)
    WorkSheet.write_merge(21,21,18,19,u"その他（",Style)
    WorkSheet.write_merge(21,21,22 ,25,u"共済",Style)
    WorkSheet.write_merge(21,21,26,27,u"月額（",Style)
    WorkSheet.write_merge(21,21,28,30,u"○○（",Style)
    WorkSheet.write_merge(21,21,31,33,u")円（",Style)

    WorkSheet.write_merge(22,23,6 ,20,u"来所者01",Style)

    WorkSheet.write_merge(24,25,6 ,16,u"来所者住所",Style)
    WorkSheet.write_merge(26,26,6 ,16,u"来所者連絡先",Style)

    WorkSheet.write_merge(24,26,18 ,20,u"来所者続柄",Style)

    WorkSheet.write_merge(28,29,6,10,u"緊急連絡先０１",Style)
    WorkSheet.write_merge(30,31,6,10,u"緊急連絡先０２",Style)
    WorkSheet.write_merge(32,33,6,10,u"緊急連絡先０３",Style)
    WorkSheet.write_merge(34,35,6,10,u"緊急連絡先０３",Style)

    WorkSheet.write_merge(28,29,11 ,12,u"続柄０１",Style)
    WorkSheet.write_merge(30,31,11 ,12,u"続柄０２",Style)
    WorkSheet.write_merge(32,33,11 ,12,u"続柄０３",Style)
    WorkSheet.write_merge(34,35,11 ,12,u"続柄０３",Style)
    
    WorkSheet.write_merge(28,29,13 ,20,u"住所０１",Style)
    WorkSheet.write_merge(30,31,13 ,20,u"住所０２",Style)
    WorkSheet.write_merge(32,33,13 ,20,u"住所０３",Style)
    WorkSheet.write_merge(34,35,13 ,20,u"住所０３",Style)

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
    ('/Yasukawa815/', MainHandler)
], debug=True)
