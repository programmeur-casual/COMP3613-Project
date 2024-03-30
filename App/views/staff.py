from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from flask_login import login_required, current_user

from App.models import Student,Staff, User, IncidentReport
from App.controllers import (
    jwt_authenticate,
    login,
    create_incident_report,
    get_accomplishment,
    get_student_by_id,
    get_recommendations_staff,
    get_accomplishments_by_staffID,
    get_recommendation,
    get_student_by_name,
    get_students_by_faculty,
    get_staff_by_id
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''

@staff_views.route('/staffhome', methods=['GET'])
def get_staffHome_page():
    return render_template('Staff-Home.html')

@staff_views.route('/incidentReport', methods=['GET'])
def staff_ir_page():
    return render_template('IncidentReport.html')

@staff_views.route('/studentSearch', methods=['GET'])
def student_search_page():
    return render_template('StudentSearch.html')

@staff_views.route('/reviewSearch', methods=['GET'])
def review_search_page():
    return render_template('ReviewSearch.html')

@staff_views.route('/proposedAchievements', methods=['GET'])
def proposedAchievements_page():
    return render_template('ProposedAchivements.html')

@staff_views.route('/recRequests', methods=['GET'])
def recRequests_page():
    return render_template('RecommendationRequests.html')

@staff_views.route('/newIncidentReport', methods=['POST', 'GET'])
@login_required
def newIncidentReport():

  if not isinstance(current_user, Staff):
    return "Unauthorized", 401
  
  if request.method == 'POST':

    staff_id = current_user.get_id()
    student_id = request.form['studentID']

    student = get_student_by_id(student_id)
    if not student:
      flash("Student ID not found")
      return redirect('/incidentReport')
    
    topic = request.form['topic']
    report = request.form['details']
    points = request.form['points-dropdown']

    incidentReport = create_incident_report(student_id, staff_id, report,topic, points)
    return redirect('/incidentReport')
    
  return redirect('/incidentReport')

@staff_views.route('/searchStudent', methods=['GET'])
@login_required
def studentSearch():
    
    name = request.args.get('name')
    studentID = request.args.get('studentID')
    faculty = request.args.get('faculty')
    degree = request.args.get('degree')
    
    query = Student.query

    if name:  
        firstname, lastname = name.split(' ')
        # Filtering by firstname and lastname if they are provided
        query = query.filter_by(firstname=firstname, lastname=lastname)

    if studentID:  
        student = get_student_by_id(studentID)
        if student:
            # Render student profile immediately
            return jsonify(student.serialize()) 
        else:
            return "Student not found", 404

    if faculty:
        query = query.filter_by(faculty=faculty)

    if degree:
        query = query.filter_by(degree=degree)

    students = query.all()

    if students:
        return render_template('ssresult.html',students=students)
    else:
        return "No matching records", 404

@staff_views.route('/review_search/<string:reviewID>', methods=['GET'])
@login_required
def reviewSearch(reviewID):

    if not isinstance(current_user, Staff):
        return "Unauthorized", 401
  
    studentName = request.form.get('student_name')
    #TOPICS
    leadership = request.form.get('leadership')
    respect = request.form.get('respect')
    punctuality = request.form.get('punctuality')
    participation = request.form.get('participation')
    teamwork = request.form.get('teamwork')
    interpersonal = request.form.get('interpersonal')
    respect_authority = request.form.get('respect_authority')
    attendance = request.form.get('attendance')
    disruption = request.form.get('disruption')

    # Initialize query with Review model
    query = Review.query

    if studentName:
        query = query.filter_by(studentName=studentName)

    # Retrieve matching reviews
    reviews = query.all()

    if reviews:
        # Serialize reviews and return as JSON response
        serialized_reviews = [review.to_json() for review in reviews]
        return jsonify(serialized_reviews)
    else:
        return "No matching records", 404

@staff_views.route('/allAchievementApproval', methods=['GET'])
@login_required
def allAchievementApproval():
    
    staff_id = current_user.get_id()
    staff= get_staff_by_id(staff_id)
    
    return render_template('', achievements = achievements)

@staff_views.route('/allRecommendationRequests', methods=['GET'])
@login_required
def allRecommendationRequests():
    staffID= current_user.get_id()
    recommendations = get_recommendations_staff(staffID)
    return render_template('', recommendations = recommendations)

@staff_views.route('/recommendationRequest/<string:rrID>', methods=['GET'])
@login_required
def achievementApproval(rrID):

    recommendation = get_recommendation(rrID)
    student = get_student_by_id(recommendation.createdByStudentID)
    return render_template('', recommendation = recommendation, student=student)

@staff_views.route('/approveAchievement/<string:achievementID>', methods=['GET'])
@login_required
def approveAchievement(achievementID):

    achievement = get_accomplishment(achievementID)
    student = get_student_by_id(achievement.createdByStudentID)
    return render_template('FullReview.html', achievement = achievement, student=student)