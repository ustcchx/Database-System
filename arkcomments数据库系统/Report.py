from asyncio.windows_events import NULL
import imp
from unittest import result
import pymysql
import time
import datetime
def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db

#实现举报
#查看所有举报信息
def search_ALLReport():
    db = get_db()
    cursor = db.cursor()
    sql = "select RID,Uname,Report.UID,Ctime,Content,Ctable from Report,userpeople where Report.UID=userpeople.UID "
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return results

#根据ID查看具体举报信息
def select_Report(RID):
    db = get_db()
    cursor = db.cursor()
    sql = "select * from Report WHERE RID='%s'"%(RID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return results

def insert_Report(UID,CID,Content,CTime,Ctable):
    db = get_db()
    cursor = db.cursor()
    if len(search_ALLReport())<1:
        RID=10001
    else:
        RID=NULL
    sql = "INSERT INTO report VALUES('%s','%s','%s','%s','%s','%s')"%(RID,UID,CID,Content,CTime,Ctable)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

def delete_Report(RID):
    db = get_db()
    cursor = db.cursor()
    sql = "DELETE FROM report WHERE RID = '%s'"%(RID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

#根据举报找到原评论
def search_CommentFromReport(RID):
    db = get_db()
    cursor = db.cursor()
    results=select_Report(RID)
    CID=results[0][3]
    table=results[0][4]
    sql="select Content from '%s' WHERE CID='%s'"%(table,CID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

#删除评论
def delete_Report_Comment(RID,CID,Ctable):
    db = get_db()
    cursor = db.cursor()
    delete_Report(RID)
    sql = "DELETE FROM %s WHERE CID = '%s'"%(Ctable,CID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()