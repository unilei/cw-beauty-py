from app import create_app
from app.models import User, Language
import uuid
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from mongoengine import disconnect
import traceback

def init_db():
    print("Starting database initialization...")
    
    try:
        # 确保断开所有现有连接
        disconnect()
        
        app = create_app()
        
        with app.app_context():
            print("Checking existing collections...")
            
            # 检查是否已经有数据
            existing_languages = Language.objects.count()
            existing_users = User.objects.count()
            print(f"Found {existing_languages} languages and {existing_users} users")
            
            # 添加初始语言数据
            languages = [
                {'name': 'TypeScript', 'name_zh': 'TypeScript', 'slug': 'typescript', 'popularity': 19},
                {'name': 'Python', 'name_zh': 'Python', 'slug': 'python', 'popularity': 11},
                {'name': 'PHP', 'name_zh': 'PHP', 'slug': 'php', 'popularity': 6},
                {'name': 'C#', 'name_zh': 'C#', 'slug': 'csharp', 'popularity': 4},
                {'name': 'JavaScript', 'name_zh': 'JavaScript', 'slug': 'javascript', 'popularity': 4},
                {'name': 'Rust', 'name_zh': 'Rust', 'slug': 'rust', 'popularity': 3},
                {'name': 'Java', 'name_zh': 'Java', 'slug': 'java', 'popularity': 2},
                {'name': 'Swift', 'name_zh': 'Swift', 'slug': 'swift', 'popularity': 2},
                {'name': 'HTML', 'name_zh': 'HTML', 'slug': 'html', 'popularity': 2},
                {'name': 'CSS', 'name_zh': 'CSS', 'slug': 'css', 'popularity': 2},
                {'name': 'Kotlin', 'name_zh': 'Kotlin', 'slug': 'kotlin', 'popularity': 1},
                {'name': 'C++', 'name_zh': 'C++', 'slug': 'cpp', 'popularity': 1},
                {'name': 'Go', 'name_zh': 'Go', 'slug': 'golang', 'popularity': 1},
                {'name': 'Elixir', 'name_zh': 'Elixir', 'slug': 'elixir', 'popularity': 1},
                {'name': 'Julia', 'name_zh': 'Julia', 'slug': 'julia', 'popularity': 1},
                {'name': 'Lua', 'name_zh': 'Lua', 'slug': 'lua', 'popularity': 1},
                {'name': 'Ruby', 'name_zh': 'Ruby', 'slug': 'ruby', 'popularity': 1},
                {'name': 'Solidity', 'name_zh': 'Solidity', 'slug': 'solidity', 'popularity': 1},
                {'name': 'SystemVerilog', 'name_zh': 'SystemVerilog', 'slug': 'systemverilog', 'popularity': 1}
            ]
            
            print("Adding languages...")
            for lang_data in languages:
                try:
                    existing_lang = Language.objects(slug=lang_data['slug']).first()
                    if existing_lang:
                        # 更新现有语言的流行度
                        existing_lang.popularity = lang_data['popularity']
                        existing_lang.save()
                        print(f"Updated language: {lang_data['name']}")
                    else:
                        language = Language(**lang_data)
                        language.save()
                        print(f"Added language: {lang_data['name']}")
                except Exception as e:
                    print(f"Error adding language {lang_data['name']}: {str(e)}")
                    print(traceback.format_exc())
            
            print("\nCreating admin user...")
            admin_email = 'admin@example.com'
            try:
                if not User.objects(email=admin_email).first():
                    admin = User(
                        email=admin_email,
                        name='Admin',
                        role='ADMIN'
                    )
                    admin.set_password('admin123')
                    admin.save()
                    print("Admin user created successfully")
                else:
                    print("Admin user already exists")
            except Exception as e:
                print(f"Error creating admin user: {str(e)}")
                print(traceback.format_exc())
            
            print("\nDatabase initialization completed!")
                
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        print(traceback.format_exc())
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(traceback.format_exc())

if __name__ == '__main__':
    try:
        print("Starting migration script...")
        init_db()
    except Exception as e:
        print(f"Migration script failed: {str(e)}")
        print(traceback.format_exc()) 