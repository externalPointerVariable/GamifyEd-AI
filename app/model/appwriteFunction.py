import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.query import Query



from app.config.config import (
    appwriteBucketId,
    appwriteCollectionId,
    appwriteDatabaseId,
    appwriteProjectId,
    appwriteSecretKey,
)

class AppwriteFunction:
    def __init__(self):
        self.client = Client()
        self.client.set_endpoint("https://cloud.appwrite.io/v1")
        self.client.set_project(appwriteProjectId)
        self.client.set_key(appwriteSecretKey)  
        self.databases = Databases(self.client)
        self.storage = Storage(self.client)

    def getTopic(self, topicName):
        try:
            response = self.databases.list_documents(
                appwriteDatabaseId, appwriteCollectionId, 
                queries=[Query.equal("name", topicName)]
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

    def setTopic(self, topic_data):
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
        
# if __name__ == "__main__":
#     appwrite_instance = AppwriteFunction()

#     # Set a new topic
#     new_topic = {"name": "AI", "content": "Artificial Intelligence discussion", "podcasturl":"www.google.com"}
#     topic_response = appwrite_instance.setTopic(new_topic)
#     print("Set Topic Response:", topic_response)

