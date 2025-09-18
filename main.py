from chatbot import Chatbot

def main():
    print("Welcome to the LearnJS!")
    print("Ask me about Javascript")

bot = Chatbot()

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['exit', 'quit']:
        print("LearnJS: Goodbye!")
        break
    response = bot.get_response(user_input)
    print(f"Bot: {response}")

if __name__ == "__main__":
    main()

    """
Main entry point for the JavaScript Learning Assistant
"""
import uvicorn
import os
from fastapi import FastAPI
from backend import app
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    """Main function to run the application"""
    try:
        # Get configuration from environment variables
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 8000))
        reload = os.getenv("RELOAD", "true").lower() == "true"
        
        logger.info(f"Starting JavaScript Learning Assistant API...")
        logger.info(f"Host: {host}")
        logger.info(f"Port: {port}")
        logger.info(f"Reload: {reload}")
        
        # Run the FastAPI application
        uvicorn.run(
            "backend:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

if __name__ == "__main__":
    main()