"""
Dashboard route - main overview
"""
from flask import Blueprint, render_template, current_app
from app.models.certificate import CertificateService
import plotly
import plotly.graph_objects as go
import plotly.express as px
import json

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    """Main dashboard view"""
    cert_service = CertificateService(current_app.config['MOCK_DATA_PATH'])
    
    # Get statistics
    stats = cert_service.get_statistics()
    
    # Get all certificates for charts
    certificates = cert_service.get_all()
    
    # Create status distribution pie chart
    status_chart = create_status_pie_chart(stats)
    
    # Create site distribution bar chart
    site_chart = create_site_bar_chart(stats)
    
    # Create expiration timeline
    timeline_chart = create_expiration_timeline(certificates)
    
    # Get recent discoveries
    recent_certs = sorted(certificates, key=lambda x: x.discovered_at, reverse=True)[:5]
    
    # Get expiring soon
    expiring_soon = [c for c in certificates if 0 < c.days_until_expiry <= 30]
    expiring_soon = sorted(expiring_soon, key=lambda x: x.days_until_expiry)[:5]
    
    return render_template(
        'dashboard.html',
        stats=stats,
        status_chart=status_chart,
        site_chart=site_chart,
        timeline_chart=timeline_chart,
        recent_certificates=recent_certs,
        expiring_soon=expiring_soon
    )


def create_status_pie_chart(stats):
    """Create pie chart for certificate status distribution"""
    labels = ['Healthy', 'Attention', 'Warning', 'Critical', 'Expired']
    values = [
        stats['healthy'],
        stats['attention'],
        stats['warning'],
        stats['critical'],
        stats['expired']
    ]
    colors = ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.3
    )])
    
    fig.update_layout(
        title='Certificate Status Distribution',
        height=350,
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_site_bar_chart(stats):
    """Create bar chart for certificates by site"""
    sites = list(stats['sites'].keys())
    counts = list(stats['sites'].values())
    
    fig = go.Figure(data=[go.Bar(
        x=sites,
        y=counts,
        marker_color='#1e3a8a'
    )])
    
    fig.update_layout(
        title='Certificates by Site',
        xaxis_title='Site',
        yaxis_title='Count',
        height=350,
        margin=dict(l=20, r=20, t=40, b=60)
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_expiration_timeline(certificates):
    """Create timeline showing when certificates expire"""
    # Sort by expiration date
    sorted_certs = sorted(certificates, key=lambda x: x.days_until_expiry)
    
    # Take top 20
    top_certs = sorted_certs[:20]
    
    hostnames = [c.hostname.split('.')[0] for c in top_certs]  # Shorten names
    days = [c.days_until_expiry for c in top_certs]
    colors = [c.status_color for c in top_certs]
    
    # Map status colors to actual hex colors
    color_map = {
        'danger': '#dc3545',
        'warning': '#ffc107',
        'info': '#17a2b8',
        'success': '#28a745'
    }
    bar_colors = [color_map.get(c, '#6c757d') for c in colors]
    
    fig = go.Figure(data=[go.Bar(
        y=hostnames,
        x=days,
        orientation='h',
        marker=dict(color=bar_colors)
    )])
    
    fig.update_layout(
        title='Certificates Expiring Soon (Days Remaining)',
        xaxis_title='Days Until Expiry',
        yaxis_title='Device',
        height=500,
        margin=dict(l=150, r=20, t=40, b=40)
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)