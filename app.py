# from flask import Flask
# from flask_restplus import Resource, Api
# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/pythondb'


# app = Flask(__name__)
# # api = Api(app)
# db = SQLAlchemy(app)


# class Students(db.model):
   
#     name = db.Column(db.String(80), nullable=False)
#     age = db.Column(db.String(12), nullable=False)
#     state = db.Column(db.String(120), nullable=False)    
#     country = db.Column(db.String(120), nullable=False) 
# @api.route('/student',methods=["GET",'POST'])
# def student():
#     if(request.method=='POST'):
       
#         name = request.form.get('name')
#         age = request.form.get('age')
#         state= request.form.get('state')
#         country = request.form.get('country')
#         entry = Contacts(name=name, age = age, state = state,country = country )
#         db.session.add(entry)
#         db.session.commit()
#     return render_template('student.html')
# app.run(debug=True)
