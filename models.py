from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ScreenshotTask(db.Model):
    task_id = db.Column(db.String, primary_key=True)
    screenshots = db.relationship('Screenshot', backref='task', lazy=True)


class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String, nullable=False)
    task_id = db.Column(db.String, db.ForeignKey(
        'screenshot_task.task_id'), nullable=False)
