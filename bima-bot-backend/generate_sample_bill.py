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
        ['S.No', 'Description', 'Days/Qty', 'Rate', 'Amount'],
        ['1', 'Room Rent (Private Ward)', '5 days', '4,000', '20,000'],
        ['2', 'Surgery Charges (Knee Replacement)', '-', '60,000', '60,000'],
        ['3', 'Knee Implant (Cobalt Chrome)', '-', '1,10,000', '1,10,000'],
        ['4', 'Pharmacy / Medicines', '-', '22,500', '22,500'],
        ['5', 'OT Consumables', '-', '8,000', '8,000'],
        ['6', 'Nursing & Physio Charges', '-', '9,000', '9,000'],
        ['7', 'Admission / Admin Charges', '-', '1,000', '1,000'],
        ['8', 'Bio-Medical Waste Disposal', '-', '750', '750'],
        ['9', 'Diet & F&B Charges', '5 days', '1,000', '5,000'],
        ['', '', '', 'TOTAL:', '2,36,250']  # 20+60+110+22.5+8+9+1+0.75+5 = 236250. Wait screenshot says 2,81,250. Let me check math.
        # Screenshot says 2,81,250. 
        # items: 20k + 60k + 1.1L + 22.5k + 8k + 1k + 750 + 9k = 231250.
        # Maybe I should add another item to match 2,81,250? Or just use screenshot total.
        # Let's add "Anesthetist Charges": 50,000 -> 2,81,250.
    ]
    
    # Update math: 231,250 + 50,000 = 281,250.
    # Re-writing bill data with Anesthetist to match total.
    
    bill_data = [
        ['S.No', 'Description', 'Days/Qty', 'Rate', 'Amount'],
        ['1', 'Room Rent (Private Ward)', '5 days', '4,000', '20,000'],
        ['2', 'Surgery Charges (Knee Replacement)', '-', '60,000', '60,000'],
        ['3', 'Knee Implant (Cobalt Chrome)', '-', '1,10,000', '1,10,000'],
        ['4', 'Anesthetist Charges', '-', '50,000', '50,000'],
        ['5', 'Pharmacy / Medicines', '-', '22,500', '22,500'],
        ['6', 'Nursing & Physio Charges', '-', '9,000', '9,000'],
        ['7', 'OT Consumables', '-', '8,000', '8,000'],
        ['8', 'Admission / Admin Charges', '-', '1,000', '1,000'],
        ['9', 'Bio-Medical Waste Disposal', '-', '750', '750'],
        ['', '', '', 'TOTAL:', '2,81,250']
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
