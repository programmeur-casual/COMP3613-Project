from App.models import Accomplishment
from App.database import db 
from .staff import (
    get_staff_by_name
)
from .student import (
    get_student_by_id
)

def create_accomplishment(studentID, verified, taggedStaffName,topic, details):
    student = get_staff_by_id(studentID)
    firstname, lastname = taggedStaffName.split(' ')
    staff = get_staff_by_name(firstname, lastname)
    if student is None:
        print("[accomplishment.create_accomplishment] Error occurred while creating new accomplishment: No student found.")
        return False
    if staff is None:
        print("[accomplishment.create_accomplishment] Error occurred while creating new accomplishment: No staff found.")
        return False

    newAccomplishment = Accomplishment(studentID=student.ID, verified=False, taggedStaffId=staff.ID,topic=topic, details=details)
    db.session.add(newAccomplishment)

    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[accomplishment.create_accomplishment] Error occurred while creating new accomplishment: ", str(e))
        db.session.rollback()
        return False

def delete_accomplishment(accomplishmentID):
    accomplishment = Accomplishment.query.filter_by(id=accomplishmentID).first()
    if accomplishment:
        db.session.delete(accomplishment)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[accomplishment.delete_accomplishment] Error occurred while deleting accomplishment: ", str(e))
            db.session.rollback()
            return False
    else:
        print("[accomplishment.delete_accomplishment] Error occurred while deleting accomplishment: Accomplishment not found.")
        return False
def get_accomplishment(id):
    accomplishment = Accomplishment.query.filter_by(id=id).first()
    if accomplishment:
        return accomplishment
    else:
        return None
        
def get_accomplishments_by_studentID(studentID):
    accomplishments = Accomplishment.query.filter_by(createdByStudentID=studentID).all()
    if accomplishments:
        return accomplishments
    else:
        return []

def get_accomplishments_by_staffID(staffID):
    accomplishments = Accomplishment.query.filter_by(taggedStaffId=staffID).all()
    if accomplishments:
        return accomplishments
    else:
        return []

        
