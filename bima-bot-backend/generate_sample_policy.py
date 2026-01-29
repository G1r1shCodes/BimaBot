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
    elements.append(Paragraph("HDFC ERGO HEALTH INSURANCE", title_style))
    elements.append(Paragraph("Individual Mediclaim Policy", styles['Heading3']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Policy Details
    elements.append(Paragraph("POLICY SCHEDULE", header_style))
    
    policy_data = [
        ['Policy Number:', 'POL-2025-XYZ123', 'Issue Date:', '01-Jan-2025'],
        ['Policy Holder:', 'John Doe', 'Date of Birth:', '15-Mar-1981'],
        ['Policy Term:', '1 Year', 'Renewal Date:', '01-Jan-2026'],
        ['Sum Insured:', '₹5,00,000', 'Premium Paid:', '₹15,000'],
        ['Policy Type:', 'Individual', 'Plan:', 'Standard Mediclaim']
    ]
    
    policy_table = Table(policy_data, colWidths=[1.8*inch, 2.2*inch, 1.5*inch, 2*inch])
    policy_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FEE2E2')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#FEE2E2')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(policy_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Coverage Details
    elements.append(Paragraph("COVERAGE & BENEFITS", header_style))
    
    coverage_text = """
    This policy provides coverage for hospitalization expenses including room rent, ICU charges, 
    doctor fees, diagnostics, surgery, and other medical expenses as per the terms and conditions 
    outlined below. The policy is subject to the limits, exclusions, and waiting periods specified.
    """
    elements.append(Paragraph(coverage_text, section_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Room Rent & ICU Limits
    elements.append(Paragraph("SUB-LIMITS & RESTRICTIONS", header_style))
    
    limits_data = [
        ['Benefit Type', 'Limit', 'Remarks'],
        ['Room Rent (Per Day)', '₹3,000', 'Single Private AC Room Only'],
        ['ICU Charges (Per Day)', '₹10,000', 'Maximum 5 days, Total cap: ₹50,000'],
        ['Ambulance Charges', '₹2,000', 'Per hospitalization'],
        ['Doctor Consultation', 'Covered', 'As per actuals, no limit']
    ]
    
    limits_table = Table(limits_data, colWidths=[2.5*inch, 2*inch, 2.5*inch])
    limits_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC2626')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(limits_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Co-Payment Clause
    elements.append(Paragraph("CO-PAYMENT TERMS", header_style))
    
    copay_text = """
    <b>10% Co-Payment Clause:</b> The insured shall bear 10% of all admissible claims under this policy. 
    This co-payment is applicable to all claims and will be deducted from the claim settlement amount. 
    For example, if the approved claim is ₹1,00,000, the insurer will pay ₹90,000 and the insured 
    will bear ₹10,000.
    """
    elements.append(Paragraph(copay_text, section_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Pre-Existing Diseases
    elements.append(Paragraph("PRE-EXISTING DISEASE (PED) CLAUSE", header_style))
    
    ped_text = """
    <b>Waiting Period: 48 Months</b><br/>
    <br/>
    Pre-existing diseases are covered only after a continuous waiting period of 48 months from the 
    policy inception date. Any disease, ailment, injury, or condition that existed or manifested 
    prior to the policy start date is considered pre-existing.
    <br/><br/>
    <b>Declared Pre-Existing Conditions for Insured (John Doe):</b>
    <br/>
    • Type 2 Diabetes Mellitus (since 2018)<br/>
    • Essential Hypertension (since 2020)<br/>
    • Asthma (since 2015)
    <br/><br/>
    <i>Note: As this policy was issued on 01-Jan-2025, PED coverage will commence from 01-Jan-2029. 
    Any hospitalization related to these conditions before 01-Jan-2029 will NOT be covered.</i>
    """
    elements.append(Paragraph(ped_text, section_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # General Waiting Periods
    elements.append(Paragraph("GENERAL WAITING PERIODS", header_style))
    
    waiting_data = [
        ['Waiting Period Type', 'Duration', 'Description'],
        ['Initial Waiting Period', '30 days', 'No claims admissible in first 30 days (except accident)'],
        ['Specific Diseases', '24 months', 'Cataract, Hernia, Stones, Sinusitis, etc.'],
        ['Pre-Existing Diseases', '48 months', 'As declared in proposal form']
    ]
    
    waiting_table = Table(waiting_data, colWidths=[2.2*inch, 1.5*inch, 3.3*inch])
    waiting_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FEE2E2')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(waiting_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Exclusions
    elements.append(Paragraph("PERMANENT EXCLUSIONS", header_style))
    
    exclusions_text = """
    The following items are <b>NOT COVERED</b> under this policy:
    <br/><br/>
    1. <b>Consumables:</b> Items like surgical gloves, syringes, cotton, bandages, plasters, 
    needles, disposable caps/shoe covers, masks, and similar disposable items.
    <br/><br/>
    2. <b>Cosmetic Surgery:</b> Any treatment for cosmetic or aesthetic purposes.
    <br/><br/>
    3. <b>Dental Treatment:</b> Unless arising from accident requiring hospitalization.
    <br/><br/>
    4. <b>Refractive Error Correction:</b> LASIK, spectacles, contact lenses.
    <br/><br/>
    5. <b>Treatment Outside India:</b> Any expenses incurred for treatment taken outside India.
    <br/><br/>
    6. <b>Ayurveda/Homeopathy:</b> Unless provided by AYUSH-qualified practitioners in recognized hospitals.
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
