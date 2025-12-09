import pytest
from unittest.mock import patch, MagicMock
from opt.services.security.acme_certificates import ACMECertificateManager, ACMEConfig, CertificateStatus

@pytest.fixture
def acme_manager():
    config = ACMEConfig(
        email="test@example.com",
        cert_dir="/tmp/certs",
        account_dir="/tmp/account",
        webroot="/tmp/webroot"
    )
    return ACMECertificateManager(config)

@pytest.mark.asyncio
async def test_request_certificate_success(acme_manager):
    with patch.object(acme_manager, '_issue_certificate', return_value=True) as mock_issue:
        success, cert = await acme_manager.request_certificate(["example.com"])
        
        assert success is True
        assert cert.common_name == "example.com"
        assert cert.status == CertificateStatus.VALID
        assert cert.issued_at is not None

@pytest.mark.asyncio
async def test_request_certificate_failure(acme_manager):
    with patch.object(acme_manager, '_issue_certificate', return_value=False) as mock_issue:
        success, cert = await acme_manager.request_certificate(["example.com"])
        
        assert success is False
        assert cert.status == CertificateStatus.ERROR

@pytest.mark.asyncio
async def test_issue_certificate_calls_certbot(acme_manager):
    # Create a dummy cert object
    from opt.services.security.acme_certificates import Certificate, ACMEProvider
    cert = Certificate(id="123", domains=["example.com"], common_name="example.com", provider=ACMEProvider.LETSENCRYPT)
    
    with patch('opt.services.security.acme_certificates.subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        
        # We need to mock _parse_certificate_info as well since it reads files
        with patch.object(acme_manager, '_parse_certificate_info'):
            result = await acme_manager._issue_certificate(cert)
            
            assert result is True
            # Verify certbot was called
            args, _ = mock_run.call_args
            cmd = args[0]
            assert "certbot" in cmd
            assert "certonly" in cmd
            assert "-d" in cmd
            assert "example.com" in cmd
