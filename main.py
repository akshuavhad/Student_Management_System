from flask import Flask,request,render_template,redirect
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user='root',
  database="mydatabase"
)
mycursor = mydb.cursor()
app= Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    if request.method=='POST':
        sids=request.form.get('sid')
        snames=request.form.get('sname').capitalize()
        scitys=request.form.get('scity').capitalize()
        mycursor.execute("insert into Student(sid,sname,scity) values(%s,%s, %s)", (sids,snames, scitys))
        mydb.commit()   

    mycursor.execute("select * from Student")
    allres= mycursor.fetchall()

    return render_template('index.html',allres=allres)

@app.route('/delete/<int:id>')
def delete(id):
    mycursor.execute("delete from Student where sid={0}".format(id))
    mydb.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    mycursor.execute("select * from Student where sid={0}".format(id))
    allres = mycursor.fetchone()
    return render_template('edit.html',allres=allres)

@app.route('/update',methods=["GET","POST"])
def update():
    if request.method=='POST':
        sids=request.form.get('sid')
        snames=request.form.get('sname').capitalize()
        scitys=request.form.get('scity').capitalize()
        query="update Student set sname=%s ,scity=%s where sid=%s"
        val=(snames, scitys,sids)
        mycursor.execute(query,val)
        mydb.commit()
    return redirect('/')
    


if __name__=='__main__':
    app.run(debug=True)