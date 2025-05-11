import json
import os
import random
import logging
import calendar
from datetime import datetime

from app import db
from models import User, ChatLink
from services.chat_extractor import extract_chat_content
from services.openai_service import generate_personalized_questions

def generate_questions(month, year, user_id=None):
    """
    Generate reflection questions for each day of the month.
    
    This function uses a combination of sample questions and, if available and requested,
    personalized questions based on the user's ChatGPT conversation history.
    
    Args:
        month (int): The month (1-12)
        year (int): The year
        user_id (int, optional): The ID of the user for whom to generate personalized questions.
            If provided, the user's ChatGPT links will be used for personalization.
        
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
        
        # Add personalized questions if user_id is provided
        personalized_questions = []
        if user_id:
            personalized_questions = get_personalized_questions(user_id, month, season)
            if personalized_questions:
                # Add the personalized questions to the mix, giving them priority
                # by adding them multiple times to increase their chances of being selected
                all_questions = personalized_questions * 3 + all_questions
        
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
        
def get_personalized_questions(user_id, month, season):
    """
    Get personalized reflection questions based on the user's ChatGPT conversation links.
    
    Args:
        user_id (int): The ID of the user
        month (int): The month (1-12)
        season (str): The season (winter, spring, summer, fall)
        
    Returns:
        list: A list of personalized reflection questions
    """
    try:
        # Get the user's chat links
        chat_links = ChatLink.query.filter_by(user_id=user_id).order_by(ChatLink.created_at.desc()).limit(5).all()
        
        if not chat_links:
            logging.info(f"No chat links found for user {user_id}")
            return []
            
        # Extract content from each link
        all_content = []
        for link in chat_links:
            content = extract_chat_content(link.url)
            if content:
                all_content.append(content)
        
        if not all_content:
            logging.warning(f"Could not extract content from any chat links for user {user_id}")
            return []
            
        # Combine all content into a single string
        combined_content = "\n\n".join(all_content)
        
        # Generate personalized questions
        personalized_questions = generate_personalized_questions(
            conversation_content=combined_content,
            month=month,
            season=season,
            count=15  # Generate a few extra for variety
        )
        
        return personalized_questions
    except Exception as e:
        logging.error(f"Error getting personalized questions: {str(e)}")
        return []
