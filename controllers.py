import io
import os
import zipfile
from flask import jsonify, request, send_file
from models import db, ScreenshotTask, Screenshot
from screenshot import screenshot_task
import threading
import uuid


def init_controllers(app):

    @app.route('/isalive', methods=['GET'])
    def is_alive():
        return "Service is alive", 200

    @app.route('/screenshots', methods=['POST'])
    def start_screenshots():
        data = request.json
        start_url = data['start_url']
        num_links = data['number_of_links']
        task_id = str(uuid.uuid4())

        task = ScreenshotTask(task_id=task_id)
        db.session.add(task)
        db.session.commit()

        thread = threading.Thread(target=screenshot_task,
                                  args=(app, task_id, start_url, num_links))
        thread.start()

        return jsonify({"task_id": task_id}), 202

    @app.route('/screenshots/<task_id>', methods=['GET'])
    def get_screenshots(task_id):
        task = ScreenshotTask.query.get(task_id)
        if not task or not task.screenshots:
            return jsonify({"error": "No screenshots found for the given ID"}), 404

        # Creating a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for screenshot in task.screenshots:
                # Ensure the file exists
                if os.path.exists(screenshot.file_path):
                    zip_file.write(screenshot.file_path,
                                   os.path.basename(screenshot.file_path))

        zip_buffer.seek(0)

        # Correct use of send_file
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"{task_id}_screenshots.zip"
        )
