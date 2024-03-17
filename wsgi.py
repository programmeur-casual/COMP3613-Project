import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, get_transcript )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    # create_user(1,'bob','Bob', 'Donald', 'bobpass', 'bob@gmail.com','FST')
    print('database intialized')

# '''
# User Commands
# '''

# # Commands can be organized using groups

# # create a group, it would be the first argument of the comand
# # eg : flask user <command>
# # user_cli = AppGroup('user', help='User object commands') 

# # # Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(id, username, firstname,lastname , password, email, faculty):
#     create_user(id, username, firstname,lastname , password, email, faculty)
#     print(f'{username} created!')

# # this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

# app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StaffUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("recommendation", help="Run Recommendation tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "RecommendationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "RecommendationIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("karma", help="Run Karma tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("incidentreport", help="Run Incident Report tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "IncidentReportUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "IncidentReportIntegrationTests"]))
    # else:
    #     sys.exit(pytest.main(["-k", "App"]))

@test.command("accomplishment", help="Run Accomplishment tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AccomplishmentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "AccomplishmentIntegrationTests"]))
    # else:
    #     sys.exit(pytest.main(["-k", "App"]))

@test.command("grades", help="Run Grades tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "GradesUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "GradesIntegrationTests"]))
    # else:
    #     sys.exit(pytest.main(["-k", "App"]))

@test.command("admin", help="Run Admin tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "AdminUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
    # else:
    #     sys.exit(pytest.main(["-k", "App"]))

@test.command("karma", help="Run karma tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
    # else:
    #     sys.exit(pytest.main(["-k", "App"]))


@test.command("print", help="print get_transcript")
@click.argument("type", default="all")
def print_transcript(type):
    studentID = input("Enter student ID: ")  # Prompt user to enter student ID
    transcripts = get_transcript(studentID)   # Get transcript data for the student
    if transcripts:
        for transcript in transcripts:
            if type == "all":
                print(transcript.to_json())  # Print all transcript data as JSON
            elif type == "id":
                print(transcript.studentID)  # Print student ID
            elif type == "gpa":
                print(transcript.gpa)  # Print GPA
            elif type == "fullname":
                print(transcript.fullname)  # Print full name
            # Add more options as needed
            else:
                print("Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options.")
    else:
        print("Transcript not found for student with ID:", studentID)

app.cli.add_command(test)