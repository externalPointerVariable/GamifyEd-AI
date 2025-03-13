import os
import sys

# Append the parent directory to sys path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import Appwrite SDK
import appwrite
from app.config.config import (
    appwriteBucketId,
    appwriteCollectionId,
    appwriteDatabaseId,
    appwriteProjectId
)

class AppwriteFunction:
    def __init__(self):
        self.client = appwrite.Client()
        self.client.set_endpoint("https://cloud.appwrite.io/v1")  # Update if needed
        self.client.set_project(appwriteProjectId)
        self.client.set_key("YOUR_SECRET_API_KEY")  # Replace with your Appwrite API key

        self.databases = appwrite.Databases(self.client)
        self.storage = appwrite.Storage(self.client)

    def getTopic(self, topicName):
        try:
            response = self.databases.list_documents(
                appwriteDatabaseId, appwriteCollectionId, 
                queries=[appwrite.Query.equal("name", topicName)]
            )
            return response.get("documents", [])
        except Exception as e:
            print(f"Error fetching topic '{topicName}':", e)
            return None

    def storePDFs(self, file_path):
        try:
            response = self.storage.create_file(appwriteBucketId, "unique()", open(file_path, "rb"))
            return response
        except Exception as e:
            print("Error storing PDF:", e)
            return None

    def setTopics(self, topic_data):
        try:
            response = self.databases.create_document(
                appwriteDatabaseId,
                appwriteCollectionId,
                "unique()",
                topic_data
            )
            return response
        except Exception as e:
            print("Error setting topic:", e)
            return None
