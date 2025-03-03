# Configure all the environment variables here
from dotenv import load_dotenv
import os

load_dotenv()

podcastGeneratorApi = os.getenv('APP_VOICE_GENERTOR')
cloudProjectId = os.getenv('GOOGLE_PROJECT_ID')
cloudProjectLocation = os.getenv('GOOGLE_PROJECT_LOCATION')