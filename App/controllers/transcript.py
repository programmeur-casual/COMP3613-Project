from App.models.transcript import Transcript
from App.database import db
import json

def create_transcript(transcript_data):
    try:
        studentID = transcript_data.get('id')
        gpa = transcript_data.get('gpa')
        fullname = transcript_data.get('fullname')
        courses = transcript_data.get('courses', {})
        in_progress_courses = transcript_data.get('inProgressCourses', {})

        print('Transcript data:', transcript_data)

        # Function to split courses by semester
        def split_courses_by_semester(courses_dict):
            semesters = {}
            current_semester = None
            current_courses = {}
            for key, value in courses_dict.items():
                if 'Semester' in key:  # Assuming semester keys start with '20' for years
                    if current_semester:  # If there was a previous semester, store its courses
                        semesters[current_semester] = current_courses
                    current_semester = key
                    current_courses = {}
                else:
                    current_courses[key] = value
            if current_semester:  # Store the last semester's courses
                semesters[current_semester] = current_courses
            return semesters

        courses_by_semester = split_courses_by_semester(courses)
        in_progress_courses_by_semester = split_courses_by_semester(in_progress_courses)

        # Iterate through completed courses
        for semester, semester_courses in courses_by_semester.items():
            for course, grade in semester_courses.items():
                if grade:  # Check if grade is not empty
                    print(f"Adding completed course for {semester}: {course} - Grade: {grade}")
                    new_transcript = Transcript(studentID=studentID, gpa=gpa, fullname=fullname, semester=semester, course=course, grade=grade, isInProgress=False)
                    db.session.add(new_transcript)

        # Iterate through in-progress courses
        for semester, in_progress_semester_courses in in_progress_courses_by_semester.items():
            for in_progress_course in in_progress_semester_courses.keys():
                print(f"Adding in-progress course for {semester}: {in_progress_course}")
                new_transcript = Transcript(studentID=studentID, gpa=gpa, fullname=fullname, semester=semester, course=in_progress_course, grade='', isInProgress=True)
                db.session.add(new_transcript)

        db.session.commit()
        print("Transcript data stored in database!")
        return True
    except Exception as e:
        print("[transcript.create_transcript] Error occurred while creating new transcript: ", str(e))
        db.session.rollback()
        return False


    
def delete_transcript(studentID):
    transcript = Transcript.query.filter_by(studentID=studentID).first()

    if transcript:
        db.session.delete(transcript)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[transcript.delete_transcript] Error occurred while deleting transcript: ", str(e))
            db.session.rollback()
            return False
    
    else:
        print("[transcript.delete_transcript] Transcript not found for student with ID: ", studentID)
        return False

def get_transcript(studentID):
    transcripts = Transcript.query.filter_by(studentID=studentID).all()
    if transcripts:
        return transcripts
    else:
        return None

