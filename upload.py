import os
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re
import json
import requests
from bs4 import BeautifulSoup
import uuid
import tkinter.simpledialog as simpledialog


from datetime import datetime
# Function to convert PDF to text and append to vault.txt
def set_flag_zero():
    FLAG_FILE_PATH = "flag.txt"
    with open(FLAG_FILE_PATH, 'w') as flag_file:
        flag_file.write('0')

# Function to extract text and metadata from the PDF file and append to vault
def convert_pdf_to_text():

    # Open file dialog to select PDF file
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if file_path:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ''
            metadata = []  # List to store metadata
            file_name = os.path.basename(file_path)  # Get the source file name
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
            
            # Loop through all pages to extract text
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    text += page_text + " "
                
                # Store metadata for each page
                metadata.append({
                    "page_number": page_num + 1,
                    "page_text_length": len(page_text.strip())  # Length of text on this page
                })
            
            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)  # split on spaces following sentence-ending punctuation
            chunks = []
            chunk_metadata = []  # List to store metadata for each chunk
            current_chunk = ""
            
            for sentence in sentences:
                # Check if the current sentence plus the current chunk exceeds the limit
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    # When the chunk exceeds 1000 characters, store it and start a new one
                    chunks.append(current_chunk.strip())
                    text_uuid = str(uuid.uuid4())
                    # text_uuid = uuid.uuid5(uuid.NAMESPACE_DNS,  current_chunk.strip())
                    chunk_metadata.append({
                        "UUID": text_uuid,
                        "page_number": page_num + 1,  # Metadata for the chunk
                        "sentence_count": len(current_chunk.split('. ')),
                        "text_length": len(current_chunk.strip()),
                        "source_file": file_name,  # Add source file name
                        "date": current_date  # Add current date
                    })
                    current_chunk = sentence + " "
            
            if current_chunk:  # Don't forget the last chunk!
                chunks.append(current_chunk.strip())
                text_uuid = str(uuid.uuid4())
                # text_uuid = uuid.uuid5(uuid.NAMESPACE_DNS,  current_chunk.strip())
                chunk_metadata.append({
                    "UUID": text_uuid,
                    "page_number": page_num + 1,
                    "sentence_count": len(current_chunk.split('. ')),
                    "text_length": len(current_chunk.strip()),
                    "source_file": file_name,  # Add source file name
                    "date": current_date  # Add current date
                })
            
            # Save chunks and metadata to vault files
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")  # One chunk per line
                print(f"PDF content appended to vault.txt with each chunk on a separate line.")
            set_flag_zero()
            
            # Save metadata to JSON file
            with open("metadata.json", "a", encoding="utf-8") as metadata_file:
                for meta in chunk_metadata:
                    metadata_file.write(json.dumps(meta) + "\n")
                print("Metadata for each chunk appended to metadata.json.")

def convert_url_to_text():
    # Open file dialog to input URL
    url = simpledialog.askstring("Input URL", "Enter the URL to extract text from:")
    
    if url:
        response = requests.get(url)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            metadata = []  # List to store metadata
            file_name = url  # Use URL as source file name
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
            
            # Clean and normalize the text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)  # split on spaces following sentence-ending punctuation
            chunks = []
            chunk_metadata = []  # List to store metadata for each chunk
            current_chunk = ""
            
            for sentence in sentences:
                # Check if the current sentence plus the current chunk exceeds the limit
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    # When the chunk exceeds 1000 characters, store it and start a new one
                    chunks.append(current_chunk.strip())
                    text_uuid = str(uuid.uuid4())
                    # text_uuid = uuid.uuid5(uuid.NAMESPACE_DNS,  current_chunk.strip())
                    chunk_metadata.append({
                        "UUID": text_uuid,
                        "sentence_count": len(current_chunk.split('. ')),
                        "text_length": len(current_chunk.strip()),
                        "source_file": file_name,  # Add source file name
                        "date": current_date  # Add current date
                    })
                    current_chunk = sentence + " "
            
            if current_chunk:  # Don't forget the last chunk!
                chunks.append(current_chunk.strip())
                text_uuid = str(uuid.uuid4())
                # text_uuid = uuid.uuid5(uuid.NAMESPACE_DNS,  current_chunk.strip())
                chunk_metadata.append({
                    "UUID": text_uuid,
                    "sentence_count": len(current_chunk.split('. ')),
                    "text_length": len(current_chunk.strip()),
                    "source_file": file_name,  # Add source file name
                    "date": current_date  # Add current date
                })
            
            # Save chunks and metadata to vault files
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    vault_file.write(chunk.strip() + "\n")  # One chunk per line
                print(f"URL content appended to vault.txt with each chunk on a separate line.")
            set_flag_zero()
            
            # Save metadata to JSON file
            with open("metadata.json", "a", encoding="utf-8") as metadata_file:
                for meta in chunk_metadata:
                    metadata_file.write(json.dumps(meta) + "\n")
                print("Metadata for each chunk appended to metadata.json.")

        else:
            print(f"Failed to retrieve URL content. HTTP status code: {response.status_code}")


# Function to upload a text file and append to vault.txt
def upload_txtfile():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as txt_file:
            text = txt_file.read()
            
            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)  # split on spaces following sentence-ending punctuation
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                # Check if the current sentence plus the current chunk exceeds the limit
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    # When the chunk exceeds 1000 characters, store it and start a new one
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:  # Don't forget the last chunk!
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    # Write each chunk to its own line
                    vault_file.write(chunk.strip() + "\n")  # Two newlines to separate chunks
            print(f"Text file content appended to vault.txt with each chunk on a separate line.")


# Function to upload a text file and append to vault.txt
def upload_txtfile():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as txt_file:
            text = txt_file.read()
            
            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)  # split on spaces following sentence-ending punctuation
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                # Check if the current sentence plus the current chunk exceeds the limit
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    # When the chunk exceeds 1000 characters, store it and start a new one
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:  # Don't forget the last chunk!
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    # Write each chunk to its own line
                    vault_file.write(chunk.strip() + "\n")  # Two newlines to separate chunks
            print(f"Text file content appended to vault.txt with each chunk on a separate line.")

# Function to upload a JSON file and append to vault.txt
def upload_jsonfile():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            
            # Flatten the JSON data into a single string
            text = json.dumps(data, ensure_ascii=False)
            
            # Normalize whitespace and clean up text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Split text into chunks by sentences, respecting a maximum chunk size
            sentences = re.split(r'(?<=[.!?]) +', text)  # split on spaces following sentence-ending punctuation
            chunks = []
            current_chunk = ""
            for sentence in sentences:
                # Check if the current sentence plus the current chunk exceeds the limit
                if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                    current_chunk += (sentence + " ").strip()
                else:
                    # When the chunk exceeds 1000 characters, store it and start a new one
                    chunks.append(current_chunk)
                    current_chunk = sentence + " "
            if current_chunk:  # Don't forget the last chunk!
                chunks.append(current_chunk)
            with open("vault.txt", "a", encoding="utf-8") as vault_file:
                for chunk in chunks:
                    # Write each chunk to its own line
                    vault_file.write(chunk.strip() + "\n")  # Two newlines to separate chunks
            print(f"JSON file content appended to vault.txt with each chunk on a separate line.")

# Create the main window
root = tk.Tk()
root.title("Upload .pdf, .txt, or .json")

# Create a button to open the file dialog for PDF
pdf_button = tk.Button(root, text="Upload PDF", command=convert_pdf_to_text)
pdf_button.pack(pady=10)

# Create a button to open the file dialog for webpage
webpage_button = tk.Button(root, text="Upload Webpage", command=convert_url_to_text)
webpage_button.pack(pady=10)

# Create a button to open the file dialog for JSON file
json_button = tk.Button(root, text="Upload JSON File", command=upload_jsonfile)
json_button.pack(pady=10)

# Create a button to update the 
webpage_button = tk.Button(root, text="Upload Webpage", command=convert_url_to_text)
webpage_button.pack(pady=10)


# Run the main event loop
root.mainloop()
