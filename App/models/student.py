from App.database import db
from .user import User

class Student(User):
    __tablename__ = 'student'
    ID = db.Column(db.String(10), db.ForeignKey('user.ID'), primary_key=True)
    UniId = db.Column(db.String(10))
    gpa = db.Column(db.String(10), nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    degree = db.Column(db.String(120), nullable=False)
    admittedTerm = db.Column(db.String(120), nullable=False)
    #yearOfStudy = db.Column(db.Integer, nullable=False)
    #faculty = db.Column(db.String(120), nullable=False)
    reviews = db.relationship('Review', backref='studentReviews', lazy='joined')
    accomplishments = db.relationship('Accomplishment', backref='studentAccomplishments', lazy='joined')
    incidents = db.relationship('IncidentReport', backref='studentincidents', lazy='joined')
    transcripts = db.relationship('Transcript', backref='student', lazy='joined')
    karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID'))

    def __init__(self,UniId, gpa, admittedTerm,  degree, faculty,fullname, username, firstname, lastname, email, password):
        super().__init__(username=username, firstname=firstname,lastname=lastname, email=email, password=password, faculty=faculty)
        self.UniId = UniId
        self.gpa = gpa
        self.admittedTerm = admittedTerm
        #self.yearOfStudy = yearofStudy
        self.degree = degree
        self.faculty = faculty
        self.fullname = fullname
        self.fullname2 = f"{firstname} {lastname}"
        self.reviews = []
        self.accomplishments = []
        self.incidents = []
        self.transcripts = []
        

    def get_id(self):
        return self.ID

    # Gets the student details and returns in JSON format
    def to_json(self, karma):
        return {
            "studentindexID": self.ID,
            "studentID": self.UniId,
            "gpa": self.gpa,
            "fullname": self.fullname,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "faculty": self.faculty,
            "degree": self.degree,
            "admittedTerm": self.admittedTerm,
            #"yearOfStudy": self.yearOfStudy,
            "reviews": [review.to_json() for review in self.reviews],
            "accomplishments": [accomplishment.to_json() for accomplishment in self.accomplishments],
            "incidents": [incident.to_json() for incident in self.incidents],
            "karmaScore": karma.score if karma else None,
            "karmaRank": karma.rank if karma else None,
            "transcripts": [transcript.to_json() for transcript in self.transcripts],
        }
