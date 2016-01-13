# -*- coding: utf-8 -*-


from PyQt4.QtSql import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from PyQt4.QtCore import QCoreApplication

QCoreApplication.addLibraryPath("./plugins")
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8")) 
def openDatabase():
    
    db = QSqlDatabase.addDatabase("QODBC3")
    connectionString = "DRIVER={SQL Server};SERVER=172.16.200.3;UID=sa;PWD=gxqsj@12345=;DATABASE=GXSJ_EHR_2;"
    db.setDatabaseName(connectionString)
    db.open()
    if(db.isOpen()):
        print u"连接成功！"
        return db
    else:
        print u"连接失败"
        
def loadData():
    db = openDatabase()
    model = QSqlTableModel()
    model.setTable("BM_GWLB2")
    model.setFilter("GRADE = 1")
    parentBM = []
    parentItem = []
    if (model.select()):
        i=0 
        while i<model.rowCount():
            BM = model.record(i).value("BM0000")
            parentBM.append(BM.toString())
            item = QStandardItem()
            item.setData(BM)
            parentItem.append(item)
            i = i+1
    
    
    i = 0
    while i<len(parentItem):
        #print "\"BM0000 = '"+parentBM[i]+"'\""
        model.setFilter("\"PARENTBM = '"+parentBM[i]+"'\"")
        if (model.select()):
            d = 0
            while d < model.rowCount():
                item = QStandardItem()
                item.setData(model.record(d).value("BM0000"), 0)
                parentItem[i].appendRow(item)
                d = d+1
            
        i = i+1
    sm = QStandardItemModel()
    for a in parentItem :
        sm.appendRow(a)
    db.close()
    return sm
        
