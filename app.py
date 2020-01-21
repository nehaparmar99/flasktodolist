from flask import Flask,render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False) #nullable shows it cannot be left blank
    completed=db.Column(db.Integer,default=0)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        #return 'hello' redirects to page having hello
        task_content=request.form['content'] #content from html
        new_task=todo(content=task_content) #creATION OF OBJECT OFTODO MODEL

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue in adding'

    else:
        tasks=todo.query.order_by(todo.data_created).all() #.first to grab the first record
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "prob deleting"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task=todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "isse updating"
    else:
        return render_template('update.html',task=task)
if __name__=="__main__":
    app.run(debug=True)
