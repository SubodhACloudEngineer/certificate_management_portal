"""
Reports route - certificate lifecycle reports and exports
"""
from flask import Blueprint, render_template

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports')
def index():
    """Reports overview page"""
    return render_template('base.html')
