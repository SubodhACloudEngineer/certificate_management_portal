"""
Discovery route - certificate discovery across network infrastructure
"""
from flask import Blueprint, render_template

discovery_bp = Blueprint('discovery', __name__)


@discovery_bp.route('/discovery')
def index():
    """Discovery overview page"""
    return render_template('base.html')
