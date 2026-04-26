import PyPDF2
import io


def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"


def extract_text_from_upload(uploaded_file):
    if uploaded_file is None:
        return ""
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    else:
        return uploaded_file.read().decode("utf-8")
