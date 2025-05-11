import logging
import trafilatura

def extract_chat_content(url):
    """
    Extract the content from a ChatGPT shared conversation link.
    
    Args:
        url (str): The URL of the shared ChatGPT conversation
        
    Returns:
        str: The extracted content, or an empty string if extraction failed
    """
    try:
        # Download the content from the URL
        downloaded = trafilatura.fetch_url(url)
        
        if not downloaded:
            logging.error(f"Failed to download content from URL: {url}")
            return ""
        
        # Extract the main text content
        content = trafilatura.extract(downloaded)
        
        if not content:
            logging.error(f"Failed to extract content from downloaded HTML for URL: {url}")
            return ""
        
        return content
    except Exception as e:
        logging.error(f"Error extracting chat content from {url}: {str(e)}")
        return ""