from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection():
    uri = os.environ.get("MONGODB_URI")
    print(f"Testing connection with URI: {uri}")

    try:
        # 创建客户端连接
        client = MongoClient(uri)

        # 测试连接
        client.admin.command("ping")

        print("Successfully connected to MongoDB!")

        # 获取数据库列表
        dbs = client.list_database_names()
        print("Available databases:", dbs)

        # 测试写入权限
        db = client.cwbeauty
        test_collection = db.test_collection
        test_doc = {"test": "test"}
        result = test_collection.insert_one(test_doc)
        print("Successfully inserted test document with id:", result.inserted_id)

        # 清理测试数据
        test_collection.delete_one({"_id": result.inserted_id})
        print("Successfully cleaned up test document")

        return True
    except ConnectionFailure as e:
        print("Server not available")
        return False
    except Exception as e:
        print("An error occurred:", str(e))
        print("Traceback:")
        import traceback

        print(traceback.format_exc())
        return False
    finally:
        if "client" in locals():
            client.close()


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
