from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from App.models import Student, User
from App.controllers import (
    jwt_authenticate,
    login 
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''
@student_views.route('/home', methods=['GET'])
def get_studentHome_page():
    return render_template('Student-Home.html')

@student_views.route('/leaderboard', methods=['GET'])
def get_leaderboard_page():
    return render_template('Leaderboard.html')

@student_views.route('/profile', methods=['GET'])
def get_profile_page():
    return render_template('StudentPage.html')