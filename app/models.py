from datetime import datetime, timezone
from flask_mongoengine import MongoEngine
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import hashlib
import jwt
from datetime import datetime, timedelta
from flask import current_app
from enum import Enum

db = MongoEngine()

def get_utc_now():
    return datetime.now(timezone.utc)

class UserRole(str, Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'

class PromptType(str, Enum):
    PROMPT = 'PROMPT'
    COMPLETION = 'COMPLETION'

class PromptStatus(str, Enum):
    PENDING = 'PENDING'
    PUBLISHED = 'PUBLISHED'
    REJECTED = 'REJECTED'

class ReviewStatus(str, Enum):
    PUBLISHED = 'PUBLISHED'
    REJECTED = 'REJECTED'

class BaseDocument(db.Document):
    meta = {'abstract': True}
    
    id = db.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.DateTimeField(default=get_utc_now)
    updated_at = db.DateTimeField(default=get_utc_now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = get_utc_now()
        self.updated_at = get_utc_now()
        return super().save(*args, **kwargs)

class User(UserMixin, BaseDocument):
    email = db.StringField(required=True, unique=True)
    name = db.StringField()
    image = db.StringField()
    password_hash = db.StringField()
    role = db.EnumField(UserRole, default=UserRole.USER)

    meta = {
        'collection': 'users',
        'indexes': ['email']
    }

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)
    
    @property
    def avatar_url(self):
        if self.image:
            return self.image
        
        # 使用邮箱生成唯一的种子
        email_hash = hashlib.md5(self.email.lower().encode()).hexdigest()
        # 使用 DiceBear 的 avataaars 风格
        return f"https://api.dicebear.com/7.x/avataaars/svg?seed={email_hash}"

    def generate_token(self):
        """生成 JWT token"""
        payload = {
            'user_id': str(self.id),
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """验证 JWT token"""
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.objects(id=payload['user_id']).first()
        except:
            return None

class Language(BaseDocument):
    name = db.StringField(required=True)
    name_zh = db.StringField(required=True)
    slug = db.StringField(required=True, unique=True)
    popularity = db.IntField(default=0)

    meta = {
        'collection': 'languages',
        'indexes': ['slug']
    }

class Prompt(BaseDocument):
    title = db.StringField(required=True)
    content = db.StringField(required=True)
    type = db.EnumField(PromptType, default=PromptType.PROMPT)
    status = db.EnumField(PromptStatus, default=PromptStatus.PENDING)
    language = db.ReferenceField(Language)
    author = db.ReferenceField(User)
    likes_count = db.IntField(default=0)
    favorites_count = db.IntField(default=0)

    meta = {
        'collection': 'prompts',
        'indexes': [
            'language',
            'author',
            'status',
            'type',
            '-created_at',
            '-likes_count',
            '-favorites_count',
            # 复合索引
            {
                'fields': ['status', '-created_at'],
                'name': 'status_created_at'
            },
            {
                'fields': ['status', 'language', '-created_at'],
                'name': 'status_language_created'
            },
            {
                'fields': ['status', '-likes_count'],
                'name': 'status_likes'
            }
        ]
    }

    def update_counts(self):
        """更新点赞和收藏计数"""
        self.likes_count = Like.objects(prompt=self).count()
        self.favorites_count = Favorite.objects(prompt=self).count()
        self.save()

class Like(db.Document):
    id = db.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = db.ReferenceField(User, required=True)
    prompt = db.ReferenceField(Prompt, required=True)
    created_at = db.DateTimeField(default=get_utc_now)

    meta = {
        'collection': 'likes',
        'indexes': [
            {'fields': ['user', 'prompt'], 'unique': True},
            'prompt',
            'user'
        ]
    }

class Favorite(db.Document):
    id = db.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    user = db.ReferenceField(User, required=True)
    prompt = db.ReferenceField(Prompt, required=True)
    created_at = db.DateTimeField(default=get_utc_now)

    meta = {
        'collection': 'favorites',
        'indexes': [
            {'fields': ['user', 'prompt'], 'unique': True},
            'prompt',
            'user'
        ]
    }

class Review(BaseDocument):
    prompt = db.ReferenceField(Prompt, required=True)
    reviewer = db.ReferenceField(User, required=True)
    status = db.EnumField(ReviewStatus, required=True)
    comment = db.StringField()

    meta = {
        'collection': 'reviews',
        'indexes': [
            'prompt',
            'reviewer',
            'created_at'
        ]
    } 