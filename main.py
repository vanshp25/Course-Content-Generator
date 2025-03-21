from boltiotai import openai
import os
from flask import Flask, render_template_string, request

# Assign the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to create educational content based on the provided course name
def create_course_content(course_name):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an educational content expert."},
            {"role": "user", "content": f"Develop comprehensive educational material for a course named '{course_name}'. Include these sections: Course Objectives, Sample Syllabus, Three Measurable Outcomes using Bloom's Taxonomy (Knowledge, Comprehension, Application), Assessment Techniques, and Suggested Readings."}
        ]
    )
    return response['choices'][0]['message']['content']

# Instantiate the Flask app and define routes for handling requests
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_content = ""
    if request.method == 'POST':
        course_name = request.form['course_name']
        generated_content = create_course_content(course_name)

    # HTML template for the web page
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Course Content Generator</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <script>
            async function fetchContent() {
                const course_name = document.querySelector('#course_name').value;
                const outputArea = document.querySelector('#outputArea');
                outputArea.textContent = 'Generating content...';
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: new FormData(document.querySelector('#contentForm'))
                });
                const newContent = await response.text();
                outputArea.textContent = newContent;
            }
            function copyContent() {
                const outputArea = document.querySelector('#outputArea');
                const tempTextarea = document.createElement('textarea');
                tempTextarea.value = outputArea.textContent;
                document.body.appendChild(tempTextarea);
                tempTextarea.select();
                document.execCommand('copy');
                document.body.removeChild(tempTextarea);
                alert('Content copied to clipboard');
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1 class="my-4">Course Content Generator</h1>
            <form id="contentForm" onsubmit="event.preventDefault(); fetchContent();" class="mb-3">
                <div class="mb-3">
                    <label for="course_name" class="form-label">Course Name:</label>
                    <input type="text" class="form-control" id="course_name" name="course_name" placeholder="Enter the course name e.g. Introduction to Psychology" required>
                </div>
                <button type="submit" class="btn btn-primary">Generate Content</button>
            </form>
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    Generated Content:
                    <button class="btn btn-secondary btn-sm" onclick="copyContent()">Copy</button>
                </div>
                <div class="card-body">
                    <pre id="outputArea" class="mb-0" style="white-space: pre-wrap;">{{ generated_content }}</pre>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', generated_content=generated_content)

# Route to handle content generation requests
@app.route('/generate', methods=['POST'])
def generate():
    course_name = request.form['course_name']
    return create_course_content(course_name)

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
