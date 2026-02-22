import os
import markdown
try:
    from weasyprint import HTML, CSS
except ImportError:
    pass # Managed in requirements

def generate_wealth_pdf(markdown_text: str, client_id: str, output_dir: str = "reports") -> str:
    """
    Converts Markdown report to a styled PDF using WeasyPrint.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{client_id}_Wealth_Strategy.pdf"
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_text, extensions=['tables'])
    
    # FIX: Add UTF-8 Charset Meta Tag for Unicode (requested fix)
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Wealth Strategy - {client_id}</title>
    </head>
    <body>
        <div class="header">
            <h2>Ivy AI Wealth Advisor</h2>
            <p>Client Reference: {client_id}</p>
        </div>
        <div class="content">
            {html_content}
        </div>
        <div class="footer">
            <p>CONFIDENTIAL & PROPRIETARY. For compliance review only.</p>
        </div>
    </body>
    </html>
    """

    css = CSS(string='''
        @page { size: A4; margin: 2cm; 
                @bottom-center { content: "Page " counter(page); font-size: 10pt; color: #666; }
        }
        body { font-family: 'Helvetica', 'Arial', sans-serif; line-height: 1.6; color: #333; }
        h1, h2, h3 { color: #2C3E50; }
        .header { border-bottom: 2px solid #3498DB; margin-bottom: 20px; padding-bottom: 10px; }
        .footer { position: fixed; bottom: 0; width: 100%; text-align: center; font-size: 9pt; color: #7F8C8D; border-top: 1px solid #eee; padding-top: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 15px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    ''')

    # Generate PDF
    HTML(string=full_html).write_pdf(filename, stylesheets=[css])
    
    return filename
