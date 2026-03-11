from flask import Flask, request, jsonify
from models import db, Employee, LeaveBalance, LeaveRequest, Holiday
from datetime import datetime, timedelta
from config import DevelopmentConfig, TestingConfig
import os

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    if os.environ.get('FLASK_ENV') == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/api/leaves/apply', methods=['POST'])
    def apply_leave():
        data = request.get_json()

        employee_id = data.get('employee_id')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        leave_type = data.get('leave_type')

        # Validate input
        if not all([employee_id, start_date_str, end_date_str, leave_type]):
            return jsonify({'error': {'code': 'INVALID_INPUT', 'message': 'Missing required fields.'}}), 400

        try:
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        except ValueError:
            return jsonify({'error': {'code': 'INVALID_DATE_FORMAT', 'message': 'Date fields must be in MM/DD/YYYY format.'}}), 400

        if start_date > end_date:
            return jsonify({'error': {'code': 'INVALID_DATE_RANGE', 'message': 'Start date cannot be after end date.'}}), 400

        allowed_leave_types = ['Sick Leave', 'Casual Leave', 'Earned Leave']
        if leave_type not in allowed_leave_types:
            return jsonify({'error': {'code': 'INVALID_LEAVE_TYPE', 'message': f'Unsupported leave type. Allowed types are: {", ".join(allowed_leave_types)}'}}), 400

        # Calculate working days
        holidays = {h.holiday_date for h in Holiday.query.all()}
        working_days = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5 and current_date not in holidays:
                working_days += 1
            current_date += timedelta(days=1)

        # Check leave balance
        leave_balance = LeaveBalance.query.filter_by(employee_id=employee_id, leave_type=leave_type).first()
        if not leave_balance or leave_balance.available_days < working_days:
            return jsonify({'error': {'code': 'INSUFFICIENT_LEAVE_BALANCE', 'message': f'Requested leave ({working_days} days) exceeds available balance ({leave_balance.available_days if leave_balance else 0} days) for {leave_type}.'}}), 400

        # Create leave request
        leave_request = LeaveRequest(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            leave_type=leave_type,
            days_requested=working_days,
            submission_date=datetime.utcnow()
        )

        # Update leave balance
        leave_balance.available_days -= working_days
        leave_balance.last_updated = datetime.utcnow()

        db.session.add(leave_request)
        db.session.commit()

        return jsonify({
            'message': 'Leave request submitted successfully.',
            'request_id': leave_request.request_id,
            'status': leave_request.status,
            'days_requested': leave_request.days_requested,
            'remaining_balance': leave_balance.available_days
        }), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
