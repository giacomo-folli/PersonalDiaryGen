import os
import json
import logging
from openai import OpenAI

# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_personalized_questions(conversation_content, month, season, count=10):
    """
    Generate personalized reflection questions based on conversation content.
    
    Args:
        conversation_content (str): The extracted content from ChatGPT conversations
        month (int): The month (1-12)
        season (str): The season (winter, spring, summer, fall)
        count (int, optional): The number of questions to generate. Defaults to 10.
        
    Returns:
        list: A list of personalized reflection questions
    """
    try:
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_name = month_names[month - 1]
        
        system_prompt = f"""
        You are a thoughtful reflection coach and journal prompt creator. 
        Your task is to analyze the user's conversation history and create personalized daily reflection questions.
        
        Consider the following:
        - The current month is {month_name}
        - The current season is {season}
        - The questions should relate to themes, interests, goals, or challenges evident in the user's conversations
        - Questions should be specific enough to be meaningful but open-ended enough to allow for reflection
        - Questions should help the user gain insights about themselves and their journey
        - Each question should be a single sentence ending with a question mark
        
        Generate {count} reflection questions based on the conversation content provided.
        Format your response as a JSON array of strings, with each string being a question.
        """
        
        user_prompt = f"""
        Here is a summary of my recent conversations. Please create {count} personalized reflection 
        questions based on the themes, interests, and topics discussed:
        
        {conversation_content[:8000]}  # Limit content to avoid token limits
        """
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        if content is None:
            logging.error("OpenAI returned None content")
            return []
        result = json.loads(content)
        
        # Expect the response to be {"questions": [...]} or just an array
        if isinstance(result, dict) and "questions" in result:
            return result["questions"]
        elif isinstance(result, list):
            return result
        else:
            # Try to extract any array in the response
            for key, value in result.items():
                if isinstance(value, list):
                    return value
            
            logging.error(f"Unexpected response format: {result}")
            return []
            
    except Exception as e:
        logging.error(f"Error generating personalized questions: {str(e)}")
        return []


def extract_insights_from_conversations(conversation_content):
    """
    Extract insights and themes from conversation content.
    
    Args:
        conversation_content (str): The extracted content from ChatGPT conversations
        
    Returns:
        dict: A dictionary containing insights about the user's interests, goals, etc.
    """
    try:
        system_prompt = """
        You are an insightful analyst. Your task is to analyze the user's conversation history
        and extract key insights about their interests, goals, challenges, and themes.
        
        Provide your analysis in JSON format with the following structure:
        {
            "primary_interests": ["interest1", "interest2", ...],
            "goals": ["goal1", "goal2", ...],
            "challenges": ["challenge1", "challenge2", ...],
            "themes": ["theme1", "theme2", ...],
            "summary": "A brief summary of the conversation themes"
        }
        """
        
        user_prompt = f"""
        Here is a summary of my recent conversations. Please extract key insights:
        
        {conversation_content[:8000]}  # Limit content to avoid token limits
        """
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        if content is None:
            logging.error("OpenAI returned None content")
            return {
                "primary_interests": [],
                "goals": [],
                "challenges": [],
                "themes": [],
                "summary": "Unable to extract insights from the conversation."
            }
        return json.loads(content)
            
    except Exception as e:
        logging.error(f"Error extracting insights: {str(e)}")
        return {
            "primary_interests": [],
            "goals": [],
            "challenges": [],
            "themes": [],
            "summary": "Unable to extract insights from the conversation."
        }