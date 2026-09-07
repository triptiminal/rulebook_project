import os
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)

text = """
Official University Fee Schedule and Financial Directives

1. Tuition Rates by Faculty
The tuition fees for the academic year are determined by the Board of Governors and are subject to an annual inflationary increase. For the Faculty of Arts and Humanities, the standard undergraduate tuition is set at $6,500 per semester for domestic students and $14,200 for international students. The Faculty of Science and Engineering charges a premium rate of $7,800 for domestic and $16,500 for international students, reflecting the higher cost of laboratory provisions and specialized equipment. The Business School maintains a rate of $8,200 for domestic students and $18,000 for international students. Postgraduate research degrees (MRes, MPhil, PhD) are charged at a flat rate of $9,000 annually for domestic candidates and $22,000 for international candidates, regardless of the faculty.

2. Mandatory Ancillary Fees
In addition to tuition, all registered students are required to pay mandatory ancillary fees that support non-academic student services. These include a Student Union fee of $150 per semester, a Campus Athletics fee of $120, and a comprehensive Health and Wellness fee of $200. Furthermore, a Technology Infrastructure fee of $85 is levied to support campus-wide Wi-Fi and the maintenance of general-access computing laboratories. These fees are non-negotiable and non-refundable.

3. Program-Specific Levies
Certain professional and highly specialized programs attract additional levies to cover unique costs associated with their delivery. For example, Nursing and Allied Health students must pay an annual clinical placement administration fee of $350. Architecture students are charged a studio materials fee of $200 per semester. Students enrolled in field-intensive programs, such as Geology or Environmental Science, are billed for specific field trip transportation and accommodation costs as they occur, which typically range from $100 to $500 per excursion.

4. Library and Administrative Fines
The University maintains a strict policy on library fines to ensure the equitable circulation of resources. Overdue standard loan books accrue a fine of $1.00 per day, while high-demand short-loan items accrue a fine of $5.00 per hour. Replacement of a lost student ID card incurs an administrative fee of $35. Late registration for courses beyond the designated add/drop period requires a payment of $150. Official transcript requests are processed for a fee of $20 per copy, with expedited courier services available for an additional $40.

5. Residence and Dining Plan Fees
Accommodation in University-owned hostels ranges in price depending on the room type and amenities. A standard single room in a traditional hall costs $3,500 per semester, while an en-suite room in a newer complex costs $4,800. Studio apartments for graduate students are priced at $1,200 per month. Students residing in traditional halls are mandated to purchase a minimum dining plan, which costs $2,200 per semester and provides 14 meals per week. Flexible dining points can be added to the student account in increments of $100.

6. International Student Requirements
International students must maintain comprehensive health insurance. The University-approved plan costs $850 annually and must be paid in full prior to the commencement of the Fall semester. Furthermore, international students requiring visa extension letters or specialized documentation for immigration purposes will be charged a processing fee of $50 per document request.

7. Payment Terms and Conditions
All listed fees are payable in the local currency. The University does not accept cash payments. Accepted methods of payment include electronic bank transfer, certified cheque, or major credit cards (subject to a 2% convenience surcharge). The University provides detailed electronic invoices via the student portal at least one month prior to the payment deadline. It is the responsibility of the student to ensure that their account balance is cleared by the stipulated dates outlined in the academic calendar. Failure to resolve financial obligations will lead to the withholding of academic transcripts and may prevent graduation.
"""

pdf.multi_cell(0, 10, txt=text)
os.makedirs('corpus', exist_ok=True)
pdf.output("corpus/fee_schedule.pdf")
