
# -*- coding: utf-8 -*-
from PyQt4.QtSql import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from PyQt4.QtCore import  Qt, QCoreApplication
from test import *

QCoreApplication.addLibraryPath("./plugins");
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

def smModel():
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
            MC = model.record(i).value("MC0000")
            parentBM.append(BM.toString())
            item = QStandardItem()
            item.setData(BM)
            item.setText(MC.toString())
            parentItem.append(item)
            i = i+1
    
    
    i = 0
    while i<len(parentItem):
        model.setFilter("PARENTBM = '"+parentBM[i]+"'")
        if (model.select()):
            d = 0
            while d < model.rowCount():
                item = QStandardItem()
                bm=model.record(d).value("BM0000")
                mc=model.record(d).value("MC0000")
                item.setData(bm, 0)
                item.setText(mc.toString())
                item.setCheckable(True)
                parentItem[i].appendRow(item)
                d = d+1
            
        i = i+1
    sm = QStandardItemModel()
    for a in parentItem :
        sm.appendRow(a)
    sm.setHorizontalHeaderLabels([u"证件类型"])
    db.close()
    return sm

class MainWindow(QMainWindow):
	def __init__(self,parent = None):
		super(MainWindow,self).__init__(parent)
		self.setWindowTitle(self.tr('TABEL的树结构显示'))
		self.resize(600,400)
		self.treeView = QTreeView()
		self.treeView.columnWidth(1)
		self.setCentralWidget(self.treeView)
		self.setContentsMargins(20, 20, 20, 20)
		self.treeView.setModel(smModel())


if __name__ == '__main__':
	app=QApplication(sys.argv)
	main=MainWindow()
	main.show()
	app.exec_()
