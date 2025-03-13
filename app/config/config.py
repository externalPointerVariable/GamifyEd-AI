from dotenv import load_dotenv
import os

load_dotenv()

cloudProjectId = os.getenv('GOOGLE_PROJECT_ID')
cloudProjectLocation = os.getenv('GOOGLE_PROJECT_LOCATION')
playnotesApiKey = os.getenv('PLAYNOTES_API_KEY')
playnotesUserId = os.getenv('PLAYNOTES_USER_ID')
appwriteProjectId = os.getenv('APPWRITE_PROJECT_ID')
appwriteDatabaseId = os.getenv('APPWRITE_DATABASE_ID')
appwriteCollectionId = os.getenv('APPWRITE_COLLECTION_ID')
appwriteBucketId = os.getenv('APPWRITE_BUCKET_ID')
appwriteSecretKey = os.getenv('APPWRITE_SECRET_KEY')