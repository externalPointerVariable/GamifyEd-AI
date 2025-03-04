# Configure all the environment variables here
from dotenv import load_dotenv
import os

load_dotenv()

cloudProjectId = os.getenv('GOOGLE_PROJECT_ID')
cloudProjectLocation = os.getenv('GOOGLE_PROJECT_LOCATION')
playnotesApiKey = os.getenv('PLAYNOTES_API_KEY')
playnotesUserId = os.getenv('PLAYNOTES_USER_ID')