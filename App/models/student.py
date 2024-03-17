from App.database import db
from .user import User

class Student(User):
    __tablename__ = 'student'
    ID = db.Column(db.String(10), db.ForeignKey('user.ID'), primary_key=True)
    reviews = db.relationship('Review', backref='studentReviews', lazy='joined')
    accomplishments = db.relationship('Accomplishment', backref='studentAccomplishments', lazy='joined')
    incidents = db.relationship('IncidentReport', backref='studentincidents', lazy='joined')
    transcripts = db.relationship('Transcript', backref='student', lazy='joined')
    karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID'))

    def __init__(self, username, firstname, lastname, email, password):
        super().__init__(username=username, firstname=firstname, lastname=lastname, email=email, password=password)
        self.transcripts = []

    def get_id(self):
        return self.ID

    # Gets the student details and returns in JSON format
    def to_json(self, karma):
        return {
            "studentID": self.ID,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "reviews": [review.to_json() for review in self.reviews],
            "accomplishments": [accomplishment.to_json() for accomplishment in self.accomplishments],
            "incidents": [incident.to_json() for incident in self.incidents],
            "karmaScore": karma.score if karma else None,
            "karmaRank": karma.rank if karma else None,
            "transcripts": [transcript.to_json() for transcript in self.transcripts],
        }
