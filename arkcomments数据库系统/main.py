
from flask import Flask,flash
from flask import Flask, session
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from user import  update_user, user_login, db_close,register,select_user
from Administrator import Administrator_login, select_admin,update_admin
from Announcement import  get_ann,get_Announcement,write_Announcement,delete_Announcement,update_Announcement,search_Announcement
from Operator import search_ALLOperator,select_Operatorname,insert_Operator,delete_Operator,select_Operator
from Enemy import search_ALLEnemy,select_Enemyname,insert_Enemy,delete_Enemy,select_Enemy
from OComment import search_UIDOComment,update_OComment,delete_OComment,search_OIDOComment,write_OComment,search_CIDOCommmen
from EComment import search_UIDEComment,update_EComment,delete_EComment,search_EIDEComment,write_EComment,search_CIDECommmen
from Report import delete_Report, insert_Report,search_ALLReport,select_Report,delete_Report_Comment
from Shutup import search_ALLShutup
# 生成一个app
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'arknights_hw'
# 对app执行请求页面地址到函数的绑定
@app.route("/", methods=("GET", "POST"))
@app.route("/login", methods=("GET", "POST"))
def login(): 
    session.clear()
    print(session)
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        print(request.form)
        button_value = request.form["log_in"] if "log_in" in request.form else request.form["register"]
        print(button_value)
        if button_value=="log_in":
            Uname=request.form['Uname']
            Upassword=request.form['Upassword']
            UID= user_login(Uname, Upassword)
            db_close()
            print(Uname)
            if len(UID) != 1:
                return render_template("login_fail.html")
            else:
                session['UID'] = UID[0][0]
                session['Uname'] = Uname
                print(session)
               
                return redirect(url_for('table'))
        else:
            print(request.form)
            UgameID=request.form['UgameID']
            Uname=request.form['Uname']
            Upassword=request.form['Upassword_r']
            UID=register(Uname,Upassword,UgameID)
            if UID==None:
                return '<script> alert("昵称被占用"); window.location.href="login"</script>'
                # flash("昵称被占用")
                # return render_template("login.html")
            session['UID'] = UID[0][0]
            session['Uname'] = Uname
            
            return redirect(url_for('table'))
    else :
        #客户端GET 请求login页面时
        return render_template("login.html")

@app.route("/login_admin", methods=("GET", "POST"))
def login_admin(): 
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        print(request.form)
        AID=request.form['AId']
        Apassword=request.form['Apassword']
        Aname = Administrator_login(AID, Apassword)
        db_close()
        print(Aname)
        if len(Aname) != 1:
            return render_template("login_admin_fail.html")
        else:
            session['AID'] = AID
            session['Aname'] = Aname[0][0]
            print(session)
            return redirect(url_for('table'))
    else :
        #客户端GET 请求login页面时
        return render_template("login_admin.html")

@app.route("/table", methods=("GET", "POST"))
def table():
    administor_or_user_flag=0
    # 出于简单考虑，每次请求都需要连接数据库，可以尝试使用其它context保存数据库连接
    if 'UID' not in session and 'AID' not in session:
            return redirect(url_for('login'))
    if 'UID' in session:
        administor_or_user_flag=1
    tabs =get_Announcement()
    db_close()
    print(administor_or_user_flag)
    return render_template("table.html",rows = tabs,administor_or_user=administor_or_user_flag)

@app.route("/operate_ad",methods=("GET", "POST"))
def post_ad():
    if 'AID' not in session:
        return redirect(url_for('login'))
    tabs =get_Announcement()
    db_close()
    AID=session['AID']
    Aname=session['Aname']
    if request.method == "POST":
        if request.form['post_ad_content']!='':
            if write_Announcement(AID,request.form['post_ad_content'])=='操作频繁':
                return '<script> alert("操作频繁"); window.location.href="operate_ad"</script>'
        if 'delete_ad' in request.form:
            ANIDlist=request.form.getlist('delete_ad')
            for ANID in ANIDlist:
                delete_Announcement(ANID,AID)
                    
        return  redirect(url_for('table'))
    else:
        return render_template('operate_ad.html',rows = tabs,user_aministor=Aname)

@app.route("/personal_info",methods=("GET", "POST"))
def personal_info():
    print(session)
    if 'UID' not in session and 'AID' not in session:
        return redirect(url_for('login'))
    if 'UID' in session:
        administor_or_user_flag=1
        UID=session['UID']
        Uname=session['Uname']
        my_infos=select_user(UID)
        if request.method == "POST":
            print(request.form)
            if 'log_out' in request.form:
                return redirect(url_for('login'))
        else:
            return render_template('personal_info.html',my_infos=my_infos,administor_or_user=administor_or_user_flag,user_aministor=Uname)
    if 'AID' in session:
        administor_or_user_flag=0
        AID=session['AID']
        Aname=session['Aname']
        administor_infos=select_admin(AID)
        if request.method == "POST":
            print(request.form)
            if 'log_out' in request.form:
                return redirect(url_for('login'))
        else:
            return render_template('personal_info.html',administor_infos=administor_infos,administor_or_user=administor_or_user_flag,user_aministor=Aname)

@app.route("/change_info",methods=("GET", "POST"))
def change_info():
    if 'UID' not in session and 'AID' not in session:
        return redirect(url_for('login'))
    if 'UID' in session:
        UID=session['UID']
        if request.method == "POST":
            user=select_user(UID)[0]
            UgameID=request.form['UgameID'] if request.form['UgameID']!='' else user[4]
            Uname=request.form['Uname'] if request.form['Uname']!='' else user[1]
            Usex=request.form['Usex'] if request.form['Usex']!='' else user[5]
            Usign=request.form['Usign'] if request.form['Usign']!='' else user[3]
            Upassword_orin=request.form['Upassword_orin']
            Upassword_now=request.form['Upassword_now'] if request.form['Upassword_now']!='' else user[2]
            Upassword=user[2]
            if Upassword_orin!='' and Upassword_orin!=Upassword:
                return '<script> alert("密码错误"); window.location.href="change_info"</script>'
            else:
                if update_user(UID,Uname,Upassword_now,Usign,UgameID,Usex)!='操作成功':
                    return '<script> alert("名称被占用"); window.location.href="change_info"</script>'
            return redirect(url_for('personal_info'))
        else:
            return render_template('change_info.html')
    if 'AID' in session:
        AID=session['AID']
        if request.method == "POST":
            admin=select_admin(AID)[0]
            print(request.form)
            UgameID=request.form['UgameID'] if request.form['UgameID']!='' else admin[4]
            Uname=request.form['Uname'] if request.form['Uname']!='' else admin[1]
            Usex=request.form['Usex'] if request.form['Usex']!='' else admin[5]
            Usign=request.form['Usign'] if request.form['Usign']!='' else admin[3]
            Upassword_orin=request.form['Upassword_orin'] 
            Upassword_now=request.form['Upassword_now'] if request.form['Upassword_now']!='' else admin[2]
            Upassword=admin[2]
            if Upassword_orin!='' and Upassword_orin!=Upassword:
                print("####")
                return '<script> alert("密码错误"); window.location.href="change_info"</script>'
            else:
                if update_admin(AID,Uname,Upassword_now,Usign,UgameID,Usex)!='操作成功':
                    return '<script> alert("名称被占用"); window.location.href="change_info"</script>'
            return redirect(url_for('personal_info'))
        else:
            return render_template('change_info.html')


@app.route("/user_comments",methods=("GET", "POST"))
def user_comments():
    administor_or_user_flag=0
    session['myECID']=session['myOCID']=''
    if 'UID' not in session and 'AID' not in session:
        return redirect(url_for('login'))
    if 'UID' in session:
        administor_or_user_flag=1
        UID=session['UID']
        my_operator_comments=search_UIDOComment(UID)
        my_enemy_comments=search_UIDEComment(UID)
        if request.method == "POST":
            print(request.form)
            if 'change_operator_ID' in request.form:
                session['myOCID']=request.form['change_operator_ID']
                return redirect(url_for('operate_my_comment_operator'))
            if 'change_enemy_ID' in request.form:
                session['myECID']=request.form['change_enemy_ID']
                return redirect(url_for('operate_my_comment_enemy'))
        else:
            return render_template('user_comments.html',my_operator_comments=my_operator_comments,my_enemy_comments=my_enemy_comments,administor_or_user=administor_or_user_flag)
    else:
        reports=search_ALLReport()
        shutups=search_ALLShutup()
        if request.method == "POST":
            print(request.form)
            RIDlist=request.form.getlist('report_ID')
            RIDlist_else=request.form.getlist('report_ID_else')
            for RID in RIDlist:
                report=select_Report(RID)
                print(report)
                CID=report[0][2]
                Ctable=report[0][5]
                delete_Report_Comment(RID,CID,Ctable)
            for RID in RIDlist_else:
                delete_Report(RID)
            return redirect(url_for('user_comments'))
        else:
            return render_template('user_comments.html',administor_or_user=administor_or_user_flag,reports=reports,shutups=shutups)

@app.route("/operate_my_comment_enemy",methods=("GET", "POST"))
def operate_my_comment_enemy():
    UID=session['UID']
    if 'myECID' not in session or session['myECID']=='':
        return render_template("404.html")
    CID=session['myECID']
    if request.method == "POST":
        if '删除' in request.form:
            if delete_EComment(CID,UID) =='操作频繁':
                return '<script> alert("操作频繁"); window.location.href="operate_my_comment_enemy"</script>'
            return redirect(url_for('user_comments'))
        else:
            print(request.form)
            Strength=request.form['Strength']
            Hate=request.form['Hate']
            words=request.form['words']
            back=update_EComment(CID,UID,words,Strength,Hate)
            if back=='操作频繁':
                return '<script> alert("操作频繁"); window.location.href="operate_my_comment_enemy"</script>'
            if back!='操作成功':
                return '<script> alert("字数过多"); window.location.href="operate_my_comment_enemy"</script>'
            return redirect(url_for('user_comments'))
    return render_template('operate_my_comment_enemy.html')


@app.route("/operate_my_comment_operator",methods=("GET", "POST"))
def operate_my_comment_operator():
    UID=session['UID']
    if 'myOCID' not in session or session['myOCID']=='':
        return render_template("404.html")
    CID=session['myOCID']
    if request.method == "POST":
        if '删除' in request.form:
            if delete_OComment(CID,UID) =='操作频繁':
                return '<script> alert("操作频繁"); window.location.href="operate_my_comment_operator"</script>'
            return redirect(url_for('user_comments'))
        else:
            print(request.form)
            Strength=request.form['Strength']
            Generic=request.form['Generic']
            words=request.form['words']
            back=update_OComment(CID,UID,words,Strength,Generic)
            if back=='操作频繁':
                return '<script> alert("操作频繁"); window.location.href="operate_my_comment_operator"</script>'
            if back!='操作成功':
                return '<script> alert("字数过多"); window.location.href="operate_my_comment_operator"</script>'
            return redirect(url_for('user_comments'))
    return render_template('operate_my_comment_operator.html')

@app.route("/operator_all",methods=("GET", "POST"))
def operate_all():
    print(session)
    administor_or_user_flag=0
    # 出于简单考虑，每次请求都需要连接数据库，可以尝试使用其它context保存数据库连接
    if 'UID' not in session and 'AID' not in session:
            return redirect(url_for('login'))
    if 'UID' in session:
        administor_or_user_flag=1
    tabs =search_ALLOperator()
    db_close()
    print(administor_or_user_flag)
    if request.method == "POST":
        if '搜索' in request.form:
            Oname=request.form['Oname']
            operators=select_Operatorname(Oname)
            return render_template('operator_all.html',operators = operators,administor_or_user=administor_or_user_flag)
        session['OID']=request.form['OID']
        return redirect(url_for('operator_comments'))
    return render_template('operator_all.html',operators = tabs,administor_or_user=administor_or_user_flag)

@app.route("/enemy_all",methods=("GET", "POST"))
def enemy_all():
    administor_or_user_flag=0
    # 出于简单考虑，每次请求都需要连接数据库，可以尝试使用其它context保存数据库连接
    if 'UID' not in session and 'AID' not in session:
            return redirect(url_for('login'))
    if 'UID' in session:
        administor_or_user_flag=1
    tabs =search_ALLEnemy()
    db_close()
    if request.method == "POST":
        if '搜索' in request.form:
            Ename=request.form['Ename']
            enemys=select_Enemyname(Ename)
            return render_template('enemy_all.html',enemys = enemys,administor_or_user=administor_or_user_flag)
        session['EID']=request.form['EID']
        return redirect(url_for('enemy_comments'))
    return render_template('enemy_all.html',enemys = tabs,administor_or_user=administor_or_user_flag)

@app.route("/operator_comments",methods=("GET", "POST"))
def operator_comments():
    administor_or_user_flag=0
    if 'UID' not in session and 'AID' not in session:
            return redirect(url_for('login'))
    if 'UID' in session:
        UID=session['UID']
        administor_or_user_flag=1
    if 'OID' not in session or session['OID']=='':
        return render_template("404.html")
    OID=session['OID']
    Oname=select_Operator(OID)[0][1]
    print(OID)
    comment=search_OIDOComment(OID)
    if request.method == "POST":
        if 'insert' in request.form:
            print(request.form)
            words=request.form['words']
            Strength=request.form['Strength']
            Generic=request.form['Generic']
            back=write_OComment(OID,UID,words,Strength,Generic)
            if back=='操作频繁':
                return '<script> alert("操作频繁"); window.location.href="operator_comments"</script>'
            elif back!='操作成功':
                return '<script> alert("字数过多"); window.location.href="operator_comments"</script>'
            return redirect(url_for('operator_comments'))
        else:
            CID=request.form['Report']
            com=search_CIDOCommmen(CID)
            UIDget=com[0][2]
            CTime=com[0][4]
            Content=com[0][3]
            insert_Report(UIDget,CID,Content,CTime,'OComment')
    return render_template('operator_comments.html',comment=comment,administor_or_user=administor_or_user_flag,operator_enemy=Oname)

@app.route("/enemy_comments",methods=("GET", "POST"))
def enemy_comments():
    administor_or_user_flag=0
    if 'UID' not in session and 'AID' not in session:
            return redirect(url_for('login'))
    if 'UID' in session:
        UID=session['UID']
        administor_or_user_flag=1
    if 'EID' not in session or session['EID']=='':
        return render_template("404.html")
    EID=session['EID']
    Ename=select_Enemy(EID)[0][1]
    print(EID)
    comment=search_EIDEComment(EID)
    if request.method == "POST":
        if 'insert' in request.form:
            print(request.form)
            words=request.form['words']
            Strength=request.form['Strength']
            Hate=request.form['Hate']
            back=write_EComment(EID,UID,words,Strength,Hate)
            if back=='操作频繁':
               return '<script> alert("操作频繁"); window.location.href="enemy_comments"</script>'
            elif back!='操作成功':
                return '<script> alert("字数过多"); window.location.href="enemy_comments"</script>'

            return redirect(url_for('enemy_comments'))
        else:
            CID=request.form['Report']
            com=search_CIDECommmen(CID)
            UIDget=com[0][2]
            CTime=com[0][4]
            Content=com[0][3]
            insert_Report(UIDget,CID,Content,CTime,'EComment')
    return render_template('enemy_comments.html',comment=comment,administor_or_user=administor_or_user_flag,operator_enemy=Ename)


@app.route("/admin_op_change",methods=("GET", "POST"))
def admin_op_change():
    if 'AID' not in session:
            return redirect(url_for('login'))
    if request.method == "POST":
        print(request.form)
        if '搜索' in request.form:
            OID=request.form['OID']
            if OID!='':
                operators=select_Operator(OID)
                return render_template('admin_op_change.html',operators=operators)
        if 'delete' in request.form:
            OID=request.form['delete_operator']
        if 'insert' in request.form:
            Oname=request.form['Oname']
            Oprofession=request.form['Oprofession']
            Ostar=request.form['Ostar']
            Olife=request.form['Olife']
            Oattack=request.form['Oattack']
            Orecovery=request.form['Orecovery']
            Omagic=request.form['Omagic']
            insert_Operator(Oname,Oprofession,Ostar,Olife,Oattack,Orecovery,Omagic)
    return render_template('admin_op_change.html')

@app.route("/admin_ene_change",methods=("GET", "POST"))
def admin_ene_change():
    if 'AID' not in session:
            return redirect(url_for('login'))
    if request.method == "POST":
        print(request.form)
        if '搜索' in request.form:
            print(request.form)
            EID=request.form['EID']
            if EID!='':
                enemys=select_Enemy(EID)
                return render_template('admin_ene_change.html',enemys=enemys)
            EID=request.form['delete_enemy']
        if 'insert' in request.form:
            Ename=request.form['Ename']
            Ekind=request.form['Ekind']
            Elevel=request.form['Elevel']
            Eendure=request.form['Eendure']
            Eattack=request.form['Eattack']
            Erecovery=request.form['Erecovery']
            Emagic=request.form['Emagic']
            insert_Enemy(Ename,Ekind,Elevel,Eendure,Eattack,Erecovery,Emagic)
    return render_template('admin_ene_change.html')

















@app.route("/choice")
def choise():
    return render_template('choice.html')






















# 测试URL下返回html page
@app.route("/hello")
def hello():
    return "hello world!"

#返回不存在页面的处理
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80,debug=True)