from django.shortcuts import render, redirect
import csv
from .models import Books


def index(request):
    return render(request, 'index.html')


def books_upload(request):
    """
    This view handles the uploading of a CSV file and multiple PDF files.
    The CSV must contain a column 'PDFName' that matches the uploaded PDF files.
    """
    
    if request.method == 'POST':
        if 'csv_file' in request.FILES and 'pdf_files' in request.FILES:
            csv_file = request.FILES['csv_file']
            pdf_files = request.FILES.getlist('pdf_files')
            
            try:
                # Read and decode the CSV file
                decoded_csv = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_csv)
                
                # Print headers for debugging
                headers = reader.fieldnames
                print(f"CSV Headers: {headers}")  # Debugging line

                # Normalize headers by stripping whitespace
                headers = [header.strip() for header in headers]
                if 'PDFName' not in headers:
                    return render(request, 'books-upload.html', {'errors': ["CSV does not contain 'PDFName' column."]})

                # Create a dictionary of PDF files keyed by their names
                pdf_dict = {pdf.name.strip(): pdf for pdf in pdf_files}  # Strip PDF names too
                
                errors = []
                successful_books = []  # To track successfully saved books

                # Iterate through each row in the CSV
                for row in reader:
                    # Normalize row keys
                    normalized_row = {key.strip(): value for key, value in row.items()}

                    pdf_name = normalized_row.get('PDFName')  # Use the normalized key
                    if not pdf_name:
                        errors.append("Row does not contain 'PDFName'.")
                        continue  # Skip this iteration

                    # Attempt to retrieve the corresponding PDF file
                    pdf_file = pdf_dict.get(pdf_name)
                    
                    # Create a new book record
                    book = Books(
                        BookName=normalized_row['BookName'],
                        SubjectName=normalized_row['SubjectName'],
                        LevelName=normalized_row['LevelName'],
                    )
                    
                    # Attach the PDF file if it exists
                    if pdf_file:
                        book.UploadFile.save(pdf_file.name, pdf_file)
                        book.save()  # Save the book record here
                        successful_books.append(book.BookName)  # Track successful saves
                    else:
                        errors.append(f"PDF file '{pdf_name}' not found for book '{normalized_row['BookName']}'.")

                # Check if there are any errors
                if errors:
                    return render(request, 'books-upload.html', {'errors': errors})
                elif successful_books:
                    return redirect('index')  # Redirect to the index page on success

            except Exception as e:
                # Handle exceptions and optionally log them
                return render(request, 'books-upload.html', {'error': str(e)})
    
    # Render the upload form for GET requests or after processing the POST request
    return render(request, 'books-upload.html')

