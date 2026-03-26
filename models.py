from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

class LeaveBalance(db.Model):
    __tablename__ = 'leave_balances'
    balance_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String, db.ForeignKey('employees.employee_id'), nullable=False)
    leave_type = db.Column(db.String, nullable=False)
    available_days = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    request_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String, db.ForeignKey('employees.employee_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    leave_type = db.Column(db.String, nullable=False)
    days_requested = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False, default='Pending')
    submission_date = db.Column(db.DateTime, nullable=False)

class Holiday(db.Model):
    __tablename__ = 'holidays'
    holiday_id = db.Column(db.Integer, primary_key=True)
    holiday_date = db.Column(db.Date, nullable=False, unique=True)
    holiday_name = db.Column(db.String, nullable=False)
