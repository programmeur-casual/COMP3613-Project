from App.database import db

class Topics(db.Model):
  __tablename__ = 'topics'
  ID = db.Column(db.Integer , primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  review_id = db.Column(db.Integer, db.ForeignKey('review.ID'))

  def __init__(self, name, reviewID):
    self.name = name
    self.review_id=reviewID

  def to_json(self):
    return {
        "ID": self.ID,
        "name": self.name
    }