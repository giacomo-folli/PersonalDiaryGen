import os
import tempfile
import calendar
import logging
from datetime import datetime
from flask import render_template
import weasyprint
from models import Diary, DiaryEntry
from app import app

def generate_diary_pdf(diary_id):
    """
    Generate a PDF diary for the given diary ID.
    
    Args:
        diary_id (int): The ID of the diary to generate a PDF for.
        
    Returns:
        str: The path to the generated PDF file.
    """
    try:
        # Get the diary from the database
        diary = Diary.query.get(diary_id)
        if not diary:
            raise ValueError(f"Diary with ID {diary_id} not found")
        
        # Get all entries for this diary
        entries = DiaryEntry.query.filter_by(diary_id=diary.id).order_by(DiaryEntry.day).all()
        
        # Create a dictionary of entries by day
        entries_by_day = {entry.day: entry for entry in entries}
        
        # Get month and year
        month = diary.month
        year = diary.year
        
        # Get the number of days in the month
        days_in_month = calendar.monthrange(year, month)[1]
        
        # Get the month name
        month_name = calendar.month_name[month]
        
        # Create context for the template
        context = {
            'diary': diary,
            'entries_by_day': entries_by_day,
            'days_in_month': days_in_month,
            'month_name': month_name,
            'year': year,
            'current_year': datetime.now().year
        }
        
        # Render the HTML for the PDF
        html = render_template('pdf/diary_template.html', **context)
        
        # Create a temporary file for the PDF
        fd, path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd)
        
        # Generate the PDF
        weasyprint.HTML(string=html).write_pdf(path)
        
        return path
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        raise
