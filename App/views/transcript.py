from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
#from App.controllers.transcript import *
import os

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
import requests

from App.controllers.transcript import create_transcript

transcript_views = Blueprint('transcript_views', __name__)



@transcript_views.route('/upload_transcript', methods=['POST'])
def upload_transcript():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and file.filename.endswith('.pdf'):
        # Save the transcript PDF file
        filename = secure_filename(file.filename)
        file_path = os.path.join('App', 'Transcript', filename)  # Assuming 'App/Transcript' is the path to save transcript files
        file.save(file_path)
        print("saved transcript file!")

        # Call transcript parser service
        try:
            print('trying_to_parse_transcript')
            transcript_data = parse_transcript(file_path)  # Function to parse transcript using external service
            if transcript_data:
                # Assuming transcript_data is a dictionary containing parsed transcript data
                # Call controller function to create transcript
                #print("transcript data before attempting to use controller: ")
                #print(transcript_data)
                
                # Pass transcript_data dictionary as a single argument to create_transcript function
                success = create_transcript(transcript_data)
                if success:
                    print("transcript data stored in database!")
                    return jsonify({'message': 'Transcript uploaded and stored successfully'})
                else:
                    print("failed to store transcript data in database!")
                    return jsonify({'error': 'Failed to store transcript data in database'})
            else:
                print("transcript parsing failed!")
                return jsonify({'error': 'Transcript parsing failed'})
        except Exception as e:
            print("failed to create transcript")
            print(str(e))
            return jsonify({'error': 'Failed to parse transcript'})
    print("invalid file format!")
    return jsonify({'error': 'Invalid file format'})


# Function to parse transcript using external service
def parse_transcript(file_path):
    # API endpoint for transcript parser service
    parser_url = 'https://parser-service.onrender.com/parse'
    
    # Prepare file for uploading
    files = {'file': open(file_path, 'rb')}
    
    # Make POST request to transcript parser service
    response = requests.post(parser_url, files=files)
    
    # Check if request was successful and return parsed data
    if response.status_code == 200:
        parsed_data = response.json()  # Assuming response contains parsed transcript data
        #print("parsed transcript data from API: ")
        #print(parsed_data)
        return parsed_data
    else:
        return None