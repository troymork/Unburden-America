#!/usr/bin/env python3
"""
Unburden America Petition Service
Handles petition signatures, certificate generation, and consent management.
"""

import os
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import structlog

# Initialize structured logging
logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Unburden America Petition Service", 
    description="Petition signatures and certificate generation",
    version="1.0.0"
)

# =============================================================================
# Data Models
# =============================================================================

class PetitionSignature(BaseModel):
    name: str
    email: EmailStr
    zip_code: str
    consent_marketing: bool = False
    consent_updates: bool = True
    utm_source: Optional[str] = None
    utm_campaign: Optional[str] = None

class CertificateRequest(BaseModel):
    signer_info: Dict[str, Any]
    petition_id: str
    mint_certificate: bool = True

class CertificateResponse(BaseModel):
    certificate_id: str
    certificate_uri: str
    serial_number: str
    ledger_entry: Dict[str, Any]
    timestamp: str

# =============================================================================
# Petition Engine
# =============================================================================

class PetitionEngine:
    def __init__(self):
        self.signatures = []
        self.certificates = {}
        self.serial_counter = 1000
        
    async def process_signature(self, signature: PetitionSignature) -> Dict[str, Any]:
        """Process a petition signature"""
        # Generate signature ID
        signature_data = f"{signature.name}{signature.email}{datetime.now().isoformat()}"
        signature_id = hashlib.sha256(signature_data.encode()).hexdigest()[:16]
        
        # Store signature
        signature_record = {
            "id": signature_id,
            "name": signature.name,
            "email": signature.email,
            "zip_code": signature.zip_code,
            "consent_marketing": signature.consent_marketing,
            "consent_updates": signature.consent_updates,
            "utm_source": signature.utm_source,
            "utm_campaign": signature.utm_campaign,
            "timestamp": datetime.now().isoformat(),
            "verified": True
        }
        
        self.signatures.append(signature_record)
        logger.info("Petition signature processed", signature_id=signature_id, name=signature.name)
        
        return {
            "signature_id": signature_id,
            "status": "verified",
            "message": "Thank you for signing the petition!"
        }

    async def mint_certificate(self, request: CertificateRequest) -> CertificateResponse:
        """Mint a personalized certificate"""
        # Generate certificate ID and serial number
        self.serial_counter += 1
        certificate_id = f"cert_{datetime.now().strftime('%Y%m%d')}_{self.serial_counter:06d}"
        serial_number = f"UA-{self.serial_counter:06d}"
        
        # Create certificate data
        certificate_data = {
            "id": certificate_id,
            "serial_number": serial_number,
            "signer_name": request.signer_info.get("name", "Unknown"),
            "signer_email": request.signer_info.get("email", "unknown@example.com"),
            "petition_id": request.petition_id,
            "issued_date": datetime.now().strftime("%B %d, %Y"),
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate certificate (mock)
        certificate_uri = await self._generate_certificate_pdf(certificate_data)
        
        # Create ledger entry
        ledger_entry = {
            "hash": hashlib.sha256(str(certificate_data).encode()).hexdigest(),
            "timestamp": datetime.now().isoformat(),
            "block_number": len(self.certificates) + 1
        }
        
        # Store certificate
        self.certificates[certificate_id] = {
            "data": certificate_data,
            "uri": certificate_uri,
            "ledger": ledger_entry
        }
        
        logger.info("Certificate minted", certificate_id=certificate_id, serial_number=serial_number)
        
        return CertificateResponse(
            certificate_id=certificate_id,
            certificate_uri=certificate_uri,
            serial_number=serial_number,
            ledger_entry=ledger_entry,
            timestamp=datetime.now().isoformat()
        )

    async def _generate_certificate_pdf(self, certificate_data: Dict[str, Any]) -> str:
        """Generate certificate PDF (mock implementation)"""
        # In a real implementation, this would use the HTML template
        # and wkhtmltopdf to generate an actual PDF certificate
        
        certificate_filename = f"{certificate_data['id']}.pdf"
        certificate_path = f"/app/certificates/{certificate_filename}"
        
        # Create mock certificate file
        with open(certificate_path, 'w') as f:
            f.write(f"CERTIFICATE OF PETITION SIGNATURE\n\n")
            f.write(f"This certifies that {certificate_data['signer_name']}\n")
            f.write(f"signed the Unburden America petition on {certificate_data['issued_date']}\n\n")
            f.write(f"Serial Number: {certificate_data['serial_number']}\n")
            f.write(f"Certificate ID: {certificate_data['id']}\n")
        
        return f"/petition/certificates/{certificate_filename}"

    def get_statistics(self) -> Dict[str, Any]:
        """Get petition statistics"""
        return {
            "total_signatures": len(self.signatures),
            "total_certificates": len(self.certificates),
            "recent_signatures": len([
                s for s in self.signatures 
                if datetime.fromisoformat(s["timestamp"]) > datetime.now().replace(hour=0, minute=0, second=0)
            ])
        }

# Initialize global engine
petition_engine = PetitionEngine()

# =============================================================================
# API Routes
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "signatures": len(petition_engine.signatures),
        "certificates": len(petition_engine.certificates)
    }

@app.post("/sign")
async def sign_petition_endpoint(signature: PetitionSignature):
    """Process petition signature"""
    logger.info("Petition signature received", name=signature.name, email=signature.email)
    return await petition_engine.process_signature(signature)

@app.post("/certificates", response_model=CertificateResponse)
async def mint_certificate_endpoint(request: CertificateRequest):
    """Mint a certificate for petition signer"""
    logger.info("Certificate mint requested", petition_id=request.petition_id)
    return await petition_engine.mint_certificate(request)

@app.get("/certificates/{certificate_id}")
async def get_certificate_endpoint(certificate_id: str):
    """Get certificate by ID"""
    if certificate_id not in petition_engine.certificates:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    return petition_engine.certificates[certificate_id]

@app.get("/statistics")
async def get_statistics_endpoint():
    """Get petition statistics"""
    return petition_engine.get_statistics()

@app.get("/signatures")
async def get_signatures_endpoint(limit: int = 100):
    """Get recent signatures (anonymized)"""
    signatures = petition_engine.signatures[-limit:]
    
    # Anonymize for privacy
    anonymized = [
        {
            "id": s["id"],
            "name_initial": s["name"][0] if s["name"] else "?",
            "zip_code": s["zip_code"],
            "timestamp": s["timestamp"]
        }
        for s in signatures
    ]
    
    return {"signatures": anonymized, "total": len(petition_engine.signatures)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)