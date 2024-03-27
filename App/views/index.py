from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('login.html')


@index_views.route('/staffhome', methods=['GET'])
def get_staffHome_page():
    return render_template('Staff-Home.html')

@index_views.route('/incidentReport', methods=['GET'])
def staff_ir_page():
    return render_template('IncidentReport.html')

@index_views.route('/studentSearch', methods=['GET'])
def student_search_page():
    return render_template('StudentSearch.html')

@index_views.route('/reviewSearch', methods=['GET'])
def review_search_page():
    return render_template('ReviewSearch.html')

@index_views.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('/workspaces/Info3604_Project/images', filename)
