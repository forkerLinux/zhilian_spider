from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/zhilian_spider'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class ResumeSource(db.Model):
    __tablename__ = 'spider_resume_source'
    id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.String(40), nullable=False)
    source = db.Column(db.String(20), nullable=False)

    def __init__(self, cv_id, source):
        self.cv_id = cv_id
        self.source = source
