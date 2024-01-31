from asyncio.windows_events import NULL
import pymysql
import time
import datetime
#这个表格用来记录管理员上次发公告时间

def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db

#查找管理员上次发公告时间
def select_Time(AID):
    db = get_db()
    cursor = db.cursor()
    sql="SELECT ATime FROM announcetime WHERE AID = '%s' "%(AID)
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

#根据现在时间判断和上次发时间的间隔，如过间隔小于gap，不能发公告
def write_Time(AID,currenttime):
    db = get_db()
    cursor = db.cursor()
    gap=datetime.timedelta(seconds=20)
    if select_Time(AID)==():
        sql="INSERT INTO announcetime VALUES('%s','%s')"%(AID,currenttime)
    else:
        if (currenttime-select_Time(AID)[0][0])<gap:
            print(currenttime-select_Time(AID)[0][0])
            return '频繁'
        else:
            sql="UPDATE announcetime SET ATime = '%s' WHERE AID = '%s'"%(currenttime,AID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

def db_close():
    db = get_db()
    if db is not None:
        db.close()

if __name__ == "__main__":
    db_close()   