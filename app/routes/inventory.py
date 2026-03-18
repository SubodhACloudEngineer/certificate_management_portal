"""
Certificate inventory route
"""
from flask import Blueprint, render_template, request, jsonify, current_app
from app.models.certificate import CertificateService

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory')
def list_certificates():
    """List all certificates with filtering and search"""
    cert_service = CertificateService(current_app.config['MOCK_DATA_PATH'])
    
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    site_filter = request.args.get('site', 'all')
    search_query = request.args.get('search', '')
    
    # Get all certificates
    certificates = cert_service.get_all()
    
    # Apply filters
    if status_filter != 'all':
        certificates = [c for c in certificates if c.status == status_filter]
    
    if site_filter != 'all':
        certificates = [c for c in certificates if c.site_code == site_filter]
    
    if search_query:
        search_lower = search_query.lower()
        certificates = [
            c for c in certificates
            if search_lower in c.hostname.lower()
            or search_lower in c.common_name.lower()
            or search_lower in c.site_code.lower()
        ]
    
    # Get unique sites for filter dropdown
    all_certs = cert_service.get_all()
    sites = sorted(list(set(c.site_code for c in all_certs)))
    
    # Get statistics for summary cards
    stats = cert_service.get_statistics()
    
    return render_template(
        'inventory.html',
        certificates=certificates,
        sites=sites,
        current_status=status_filter,
        current_site=site_filter,
        search_query=search_query,
        stats=stats
    )


@inventory_bp.route('/api/certificates')
def api_certificates():
    """API endpoint for certificate data"""
    cert_service = CertificateService(current_app.config['MOCK_DATA_PATH'])
    certificates = cert_service.get_all()
    
    return jsonify([c.to_dict() for c in certificates])


@inventory_bp.route('/api/certificate/<cert_id>')
def api_certificate_detail(cert_id):
    """API endpoint for single certificate details"""
    cert_service = CertificateService(current_app.config['MOCK_DATA_PATH'])
    certificate = cert_service.get_by_id(cert_id)
    
    if certificate:
        return jsonify(certificate.to_dict())
    else:
        return jsonify({'error': 'Certificate not found'}), 404