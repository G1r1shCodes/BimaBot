"""
Generate Sample Hospital Bill PDF for BimaBot Demo

Creates a realistic hospital discharge summary that will trigger
multiple audit flags when processed with the sample policy.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime

def create_sample_bill():
    """Generate realistic hospital bill PDF"""
    
    filename = "sample_hospital_bill.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12
    )
    
    # Hospital Header
    elements.append(Paragraph("APOLLO HOSPITALS", title_style))
    elements.append(Paragraph("Discharge Summary & Final Bill", styles['Heading3']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Patient Information
    elements.append(Paragraph("PATIENT INFORMATION", header_style))
    
    patient_data = [
        ['Patient Name:', 'John Doe', 'Patient ID:', 'P-2026-001234'],
        ['Age:', '45 years', 'Gender:', 'Male'],
        ['Admission Date:', '20-Jan-2026', 'Discharge Date:', '25-Jan-2026'],
        ['Duration:', '5 days', 'Room Type:', 'Private AC']
    ]
    
    patient_table = Table(patient_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E5E7EB')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#E5E7EB')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(patient_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Diagnosis
    elements.append(Paragraph("DIAGNOSIS", header_style))
    diagnosis_data = [
        ['Primary:', 'Type 2 Diabetes Mellitus (E11)'],
        ['Secondary:', 'Hypertension (I10), Diabetic Nephropathy (E11.21)'],
        ['Procedure:', 'Medical Management & Stabilization']
    ]
    
    diagnosis_table = Table(diagnosis_data, colWidths=[1.5*inch, 5.5*inch])
    diagnosis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E5E7EB')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    elements.append(diagnosis_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Itemized Bill
    elements.append(Paragraph("ITEMIZED BILL SUMMARY", header_style))
    
    bill_data = [
        ['S.No', 'Description', 'Days/Qty', 'Rate (₹)', 'Amount (₹)'],
        ['1', 'Room Charges (Private AC)', '5', '5,000', '25,000'],
        ['2', 'ICU Charges (2 days)', '2', '40,000', '80,000'],
        ['3', 'Doctor Consultation Fees', '-', '10,000', '10,000'],
        ['4', 'Nursing & Attendant Charges', '5', '1,500', '7,500'],
        ['5', 'Diagnostics (HbA1c, Lipid Profile, Kidney Function)', '-', '8,000', '8,000'],
        ['6', 'Pharmacy (Insulin, Anti-hypertensives)', '-', '6,500', '6,500'],
        ['7', 'Consumables (Syringes, Gloves, Catheters)', '-', '4,000', '4,000'],
        ['8', 'Physiotherapy Sessions', '3', '3,000', '9,000'],
        ['', '', '', 'TOTAL:', '1,50,000']
    ]
    
    bill_table = Table(bill_data, colWidths=[0.5*inch, 3*inch, 0.8*inch, 1.2*inch, 1.5*inch])
    bill_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data rows
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E5E7EB')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('ALIGN', (3, -1), (3, -1), 'RIGHT'),
        
        # Grid
        ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(bill_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Payment Summary
    elements.append(Paragraph("PAYMENT SUMMARY", header_style))
    
    payment_data = [
        ['Total Bill Amount:', '₹1,50,000'],
        ['Advance Paid:', '₹30,000'],
        ['Amount Due:', '₹1,20,000']
    ]
    
    payment_table = Table(payment_data, colWidths=[4.5*inch, 2.5*inch])
    payment_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 13)
    ]))
    
    elements.append(payment_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_text = """
    <para alignment="center" fontSize="9" textColor="#6B7280">
    <b>Apollo Hospitals</b><br/>
    Greams Road, Chennai - 600006<br/>
    Phone: 044-2829 3333 | Email: info@apollohospitals.com<br/>
    <br/>
    <i>This is a computer-generated document. Please submit this bill to your insurance provider for reimbursement.</i>
    </para>
    """
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Sample hospital bill created: {filename}")
    return filename


if __name__ == "__main__":
    create_sample_bill()
