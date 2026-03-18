"""
Certificate data model
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
import json


@dataclass
class Certificate:
    """Certificate data model"""
    id: str
    hostname: str
    device_type: str
    site_code: str
    service_type: str
    
    # Certificate details
    common_name: str
    subject_alternative_names: List[str]
    issuer: str
    serial_number: str
    
    # Validity
    not_before: str  # ISO format datetime
    not_after: str   # ISO format datetime
    days_until_expiry: int
    
    # Security
    key_algorithm: str
    key_size: int
    signature_algorithm: str
    is_self_signed: bool
    
    # Metadata
    certificate_fingerprint: str
    discovered_at: str
    environment: str = "production"
    
    @property
    def status(self) -> str:
        """Get certificate status based on days until expiry"""
        if self.days_until_expiry <= 0:
            return "expired"
        elif self.days_until_expiry <= 7:
            return "critical"
        elif self.days_until_expiry <= 30:
            return "warning"
        elif self.days_until_expiry <= 90:
            return "attention"
        else:
            return "healthy"
    
    @property
    def status_color(self) -> str:
        """Get color for status badge"""
        colors = {
            "expired": "danger",
            "critical": "danger",
            "warning": "warning",
            "attention": "info",
            "healthy": "success"
        }
        return colors.get(self.status, "secondary")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)


class CertificateService:
    """Service for managing certificates"""
    
    def __init__(self, mock_data_path: str):
        self.mock_data_path = mock_data_path
        self._certificates = None
    
    def load_certificates(self) -> List[Certificate]:
        """Load certificates from mock data"""
        if self._certificates is None:
            with open(self.mock_data_path, 'r') as f:
                data = json.load(f)
            
            self._certificates = [
                Certificate(**cert_data) for cert_data in data
            ]
        
        return self._certificates
    
    def get_all(self) -> List[Certificate]:
        """Get all certificates"""
        return self.load_certificates()
    
    def get_by_id(self, cert_id: str) -> Optional[Certificate]:
        """Get certificate by ID"""
        certs = self.load_certificates()
        for cert in certs:
            if cert.id == cert_id:
                return cert
        return None
    
    def get_by_status(self, status: str) -> List[Certificate]:
        """Get certificates by status"""
        certs = self.load_certificates()
        return [cert for cert in certs if cert.status == status]
    
    def get_by_site(self, site_code: str) -> List[Certificate]:
        """Get certificates by site"""
        certs = self.load_certificates()
        return [cert for cert in certs if cert.site_code == site_code]
    
    def get_statistics(self) -> dict:
        """Get certificate statistics"""
        certs = self.load_certificates()
        
        total = len(certs)
        expired = len([c for c in certs if c.status == "expired"])
        critical = len([c for c in certs if c.status == "critical"])
        warning = len([c for c in certs if c.status == "warning"])
        attention = len([c for c in certs if c.status == "attention"])
        healthy = len([c for c in certs if c.status == "healthy"])
        
        # Group by site
        sites = {}
        for cert in certs:
            if cert.site_code not in sites:
                sites[cert.site_code] = 0
            sites[cert.site_code] += 1
        
        # Group by device type
        device_types = {}
        for cert in certs:
            if cert.device_type not in device_types:
                device_types[cert.device_type] = 0
            device_types[cert.device_type] += 1
        
        return {
            'total': total,
            'expired': expired,
            'critical': critical,
            'warning': warning,
            'attention': attention,
            'healthy': healthy,
            'sites': sites,
            'device_types': device_types
        }