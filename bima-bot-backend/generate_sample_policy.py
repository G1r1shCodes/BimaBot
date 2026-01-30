"""
Generate Sample Insurance Policy PDF for BimaBot Demo

Creates a realistic insurance policy document with specific terms
that will trigger audit flags when compared with the sample bill.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime

def create_sample_policy():
    """Generate realistic insurance policy PDF"""
    
    filename = "sample_insurance_policy.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#DC2626'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#DC2626'),
        spaceAfter=12
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    # Policy Header
    elements.append(Paragraph("RELIANCE GENERAL INSURANCE", title_style))
    elements.append(Paragraph("Reliance Individual Mediclaim Policy", styles['Heading3']))
    elements.append(Spacer(1, 0.3*inch))
    
    # ... (skipping some unchanged sections) ...
    
    # Exclusions & Annexure A (Non-Payable Items)
    elements.append(Paragraph("ANNEXURE A - NON-PAYABLE ITEMS (IRDAI)", header_style))
    
    exclusions_text = """
    The following items are <b>NOT COVERED</b> as per IRDAI Guidelines (Annexure A):
    <br/><br/>
    <b>List I - Optional Items:</b> Items like Baby Food, Body Lotion, Mosquito Repellant, 
    <b>Bio-Medical Waste Disposal</b> (Optional charge).
    <br/><br/>
    <b>List II - Non-Payable Items:</b> Housekeeping charges, Service charges, Surcharges.
    <br/><br/>
    <b>List III - Items Subsumed into Procedure Charges:</b> 
    Surgical blades, <b>OT Consumables</b>, Aprons, Drapes, Gauze, Cotton.
    <br/><i>(These are part of the surgery cost and cannot be billed separately)</i>
    <br/><br/>
    <b>List IV - Items Subsumed into Costs of Treatment:</b>
    <b>Admission / Registration Charges</b>, Urine container, File charges.
    """
    elements.append(Paragraph(exclusions_text, section_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Claim Process
    elements.append(Paragraph("CLAIM SETTLEMENT PROCESS", header_style))
    
    claim_text = """
    <b>Cashless Claims:</b> Available at network hospitals. Pre-authorization required 48 hours before planned admission.
    <br/><br/>
    <b>Reimbursement Claims:</b> Submit claim within 30 days of discharge with original bills, discharge summary, and diagnostic reports.
    <br/><br/>
    <b>Claim Settlement:</b> Claims will be settled within 30 days of receipt of all documents, subject to verification and policy terms.
    """
    elements.append(Paragraph(claim_text, section_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Important Note
    note_text = """
    <para alignment="center" fontSize="9" textColor="#DC2626" backColor="#FEE2E2" borderPadding="10">
    <b>IMPORTANT:</b> This policy is subject to all terms, conditions, exclusions, and limitations 
    as detailed in the complete policy document. Please read the policy wording carefully.
    </para>
    """
    elements.append(Paragraph(note_text, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    footer_text = """
    <para alignment="center" fontSize="9" textColor="#6B7280">
    <b>HDFC ERGO General Insurance Company Limited</b><br/>
    1st Floor, HDFC House, 165-166 Backbay Reclamation, Mumbai - 400020<br/>
    Toll Free: 1800-2700-700 | Email: customersupport@hdfcergo.com<br/>
    IRDAI Reg. No.: 146 | CIN: U66030MH2007PLC177117<br/>
    <br/>
    <i>Policy issued on: 01-Jan-2025 | Valid till: 01-Jan-2026</i>
    </para>
    """
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Sample insurance policy created: {filename}")
    return filename


if __name__ == "__main__":
    create_sample_policy()
