from App.models import Student
from App.database import db 

def create_student(username, firstname, lastname, email, password):
    new_student = Student(username=username, firstname=firstname, lastname=lastname, email=email, password=password)
    db.session.add(new_student)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[student.create_student] Error occurred while creating new student: ", str(e))
        db.session.rollback()
        return False

def create_student_from_transcript(transcript_data):
    try:
                
        #storing UniId, gpa, fullname, faculty, degree, admittedTerm in Student object and linking it to the transcript object
        UniId = transcript_data.get('id')
        gpa = transcript_data.get('gpa')
        faculty = transcript_data.get('faculty')
        admittedTerm = transcript_data.get('admittedTerm')
        #yearOfStudy = transcript_data.get('yearOfStudy')
        degree = transcript_data.get('degree')
        fullname = transcript_data.get('fullname')
        

        #todo retrieve student from database and update the student object correctly
        new_student = Student(UniId=UniId, gpa=gpa, fullname=fullname, admittedTerm=admittedTerm, degree=degree, faculty=faculty, username=UniId, firstname=fullname, lastname="", email="", password="")
        #checking if student already exist based on id
        student = get_student_by_UniId(UniId)
        if student:
            print(f"Student with ID {UniId} already exists in database from controller!")
            return False
        else:
            db.session.add(new_student)
            db.session.commit()
            #printing data to be stored
            print(f"Added row: UniId: {UniId}, GPA: {gpa}, Faculty: {faculty}, Admitted Term: {admittedTerm}, Degree: {degree}, Fullname: {fullname}")
            print("Student data stored in database from controller!")
            return True


    except Exception as e:
        print("[transcript.create_transcript] Error occurred while creating new Student: ", str(e))
        db.session.rollback()
        return False


def get_student_by_id(id):
    student = Student.query.filter_by(ID=id).first()
    if student:
        return student
    else:
        return None
    
def get_student_by_UniId(UniId):
    student = Student.query.filter_by(UniId=UniId).first()
    if student:
        return student
    else:
        return None

def get_student_by_username(username):
    student = Student.query.filter_by(username=username).first()
    if student:
        return student
    else:
        return None

def get_students_by_faculty(faculty):
    students = Student.query.filter_by(faculty=faculty).all()
    return students

def get_students_by_degree(degree):
    students = Student.query.filter_by(degree=degree).all()
    return students

def get_all_students_json():
    students = Student.query.all()
    students_json = [student.to_json() for student in students]
    return students_json

def update_admittedTerm(studentID, newAdmittedTerm):
    student = get_student_by_id(studentID)
    if student:
        student.admittedTerm = newAdmittedTerm
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[student.update_admittedTerm] Error occurred while updating student admittedTerm:", str(e))
            db.session.rollback()
            return False
    else:
        print("[student.update_admittedTerm] Error occurred while updating student admittedTerm: Student "+str(studentID)+" not found")
        return False

def update_yearofStudy(studentID, newYearofStudy):
    student = get_student_by_id(studentID)
    if student:
        student.yearOfStudy = newYearofStudy
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[student.update_yearofStudy] Error occurred while updating student yearOfStudy:", str(e))
            db.session.rollback()
            return False
    else:
        print("[student.update_yearofStudy] Error occurred while updating student yearOfStudy: Student "+str(studentID)+" not found")
        return False

def update_degree(studentID, newDegree):
    student = get_student_by_id(studentID)
    if student:
        student.degree = newDegree
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[student.update_degree] Error occurred while updating student degree:", str(e))
            db.session.rollback()
            return False
    else:
        print("[student.update_degree] Error occurred while updating student degree: Student "+str(studentID)+" not found")
        return False
