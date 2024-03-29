from App.database import db
from .student import Student
from datetime import datetime

class Review(db.Model):
  __tablename__ = 'review'
  ID = db.Column(db.Integer, primary_key=True)
  studentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
  createdByStaffID = db.Column(db.String(10),db.ForeignKey('staff.ID'))
  isPositive = db.Column(db.Boolean, nullable=False)
  studentName = db.Column(db.String(40), nullable=False)
  dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
  points = db.Column(db.Integer, nullable=False)
  details = db.Column(db.String(400), nullable=False)
  topics= db.relationship('Topics', backref='reviewTopics', lazy='joined')

  def __init__(self, staff,name, studentID, isPositive, points,details,topics):
    self.createdByStaffID = staff.ID
    self.studentID = studentID
    self.studentName=name
    self.isPositive = isPositive
    self.points= points
    self.details= details
    self.topics=topics 
    self.dateCreated = datetime.now()

  def get_id(self):
    return self.ID

    
  def to_json(self, student, staff):
    return {
        "reviewID": self.ID,
        "reviewer": staff.firstname + " " + staff.lastname,
        "studentID": student.ID,
        "studentName":self.studentName,
        "studentName": student.firstname + " " + student.lastname,
        "created":self.dateCreated.strftime("%d-%m-%Y %H:%M"),  #format the date/time
        "isPositive": self.isPositive,
        "points": self.points,
        "topics": [topic.to_json() for topic in self.topics],
        "details": self.details
    }