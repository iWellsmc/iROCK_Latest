from weasyprint import HTML, CSS
from io import BytesIO
from custom_auth.models import Companies
from PIL import Image
from django.template.loader import render_to_string
import base64
from . import wcc_pdfstyle
from django.http import HttpResponse
from ..models import WorkCompletionValue
def pdf_view(request,template_name,context):
    companyImage= Companies.objects.filter(id=request.company.id).first()
    if companyImage.image:
        with open(companyImage.image.path, 'rb') as f:
            image_data = f.read()
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')  # Convert the image to RGB mode
        image = image.resize((120, 80))  # Resize the image to 150x100 pixels
        buffered = BytesIO()
        image.save(buffered, format="JPEG")      
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    output_coversheet = render_to_string(template_name,context,request)
    coversheet_style = wcc_pdfstyle(encoded_image)
    css = CSS(string=coversheet_style)

# Generate the PDF with WeasyPrint
    pdf_buffer = BytesIO()
    HTML(string=output_coversheet).write_pdf(pdf_buffer, stylesheets=[css])

# Create the Django response object with the PDF content
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')

# Set the Content-Disposition header to force a download
    #attachment
    response['Content-Disposition'] = 'inline; filename="WCC PDF.pdf"'

# Return the response
    return response

def wcc_number_generate(vendor_id,contract_number):
    serialno = WorkCompletionValue.objects.filter(vendor_id=vendor_id,status=1).count()+1
    return f'WCC/{serialno}/{contract_number}'