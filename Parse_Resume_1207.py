#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 19:18:47 2023

@author: GPT
"""
import spacy
import os
import re
import pandas as pd
from PyPDF2 import PdfReader

nlp = spacy.load('en_core_web_sm')

def extract_info_from_pdf(pdf_file):
    with open(pdf_file, "rb") as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

def extract_resume_info(text):
    
    doc = nlp(text)
    
    
    #get first two lines
    lines = text.split('\n')

    # Process the first two lines only
    first_two_lines = ' '.join(lines[:2])
    doc_first_two_lines = nlp(first_two_lines)
    
    
    #name_pattern = r"([A-Z][a-z]+ [A-Z][a-z]+)"
    phone_pattern = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    email_pattern = r"[\w.-]+@[\w.-]+"
    website_pattern = r"(?:https://)?[\w.-]+(?:\.com|\.io|\.net)"

    name = [ent.text for ent in doc_first_two_lines.ents if ent.label_ == "PERSON"]
    
    phone = re.search(phone_pattern, text).group(0) if re.search(phone_pattern, text) else ""
    email = re.search(email_pattern, text).group(0) if re.search(email_pattern, text) else ""
    website = re.search(website_pattern, text).group(0) if re.search(website_pattern, text) else ""
    
    return name, phone, email, website

# Main function to parse PDF resumes in a folder and save the information in a CSV file
def parse_resumes_in_folder(folder_path, output_csv):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            resume_text = extract_info_from_pdf(pdf_path)
            name, phone, email, website = extract_resume_info(resume_text)
            data.append([name, phone, email, website])

    # Create a pandas DataFrame from the extracted data and save it as a CSV file
    df = pd.DataFrame(data, columns=["Name", "Cellphone number", "Email", "Website"])
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    folder_path = "/Users/jiayili//Desktop/resume"
    output_csv = "/Users/jiayili/Desktop/resume/resume_data.csv"
    parse_resumes_in_folder(folder_path, output_csv) 