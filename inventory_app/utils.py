import pdfkit
from django.template.loader import get_template
from django.conf import settings

def generate_pdf(template_name, context):
    template = get_template(template_name)
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options=options)
    return pdf