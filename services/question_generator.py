import json
import os
import random
import logging
import calendar
from datetime import datetime

def generate_questions(month, year):
    """
    Generate reflection questions for each day of the month.
    
    This is a placeholder implementation that uses sample questions.
    In the future, this will use OpenAI's API to generate questions based on conversation history.
    
    Args:
        month (int): The month (1-12)
        year (int): The year
        
    Returns:
        dict: A dictionary mapping day numbers to questions
    """
    try:
        # Get the number of days in the month
        days_in_month = calendar.monthrange(year, month)[1]
        
        # Path to sample questions file
        sample_questions_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_data', 'questions.json')
        
        # Load sample questions
        with open(sample_questions_path, 'r') as f:
            sample_questions = json.load(f)
        
        # Get categories and their questions
        general_questions = sample_questions.get('general', [])
        monthly_questions = sample_questions.get('monthly', {}).get(str(month), [])
        seasonal_questions = []
        
        # Determine season based on month (Northern Hemisphere)
        if month in [12, 1, 2]:
            season = 'winter'
        elif month in [3, 4, 5]:
            season = 'spring'
        elif month in [6, 7, 8]:
            season = 'summer'
        else:
            season = 'fall'
        
        seasonal_questions = sample_questions.get('seasonal', {}).get(season, [])
        
        # Combine all questions
        all_questions = general_questions + monthly_questions + seasonal_questions
        
        # Ensure we have enough questions
        if len(all_questions) < days_in_month:
            # If we don't have enough unique questions, we'll repeat some
            all_questions = all_questions * (days_in_month // len(all_questions) + 1)
        
        # Shuffle the questions
        random.shuffle(all_questions)
        
        # Create a dictionary mapping day numbers to questions
        questions_dict = {day: all_questions[day-1] for day in range(1, days_in_month + 1)}
        
        return questions_dict
    except Exception as e:
        logging.error(f"Error generating questions: {str(e)}")
        # Fallback to basic questions if there's an error
        return {day: f"What was meaningful about today? (Day {day})" for day in range(1, 32)}
