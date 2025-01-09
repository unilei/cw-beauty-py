from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from functools import wraps

auth = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'message': 'Admin permission required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Missing authorization header'}), 401
        
        try:
            # 从 Authorization 头中提取 token
            token = auth_header.split(' ')[1]
            # 验证 token
            user = User.verify_token(token)
            if not user:
                return jsonify({'message': 'Invalid or expired token'}), 401
            # 登录用户
            login_user(user)
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Invalid token format'}), 401
    
    return decorated_function

@auth.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # 验证必要字段
        required_fields = ['email', 'name', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        # 验证邮箱是否已被使用
        if User.objects(email=data['email']).first():
            return jsonify({
                'message': 'Email already exists'
            }), 400
        
        # 创建新用户
        user = User(
            email=data['email'],
            name=data['name']
        )
        user.set_password(data['password'])
        user.save()
        
        # 登录用户
        login_user(user)
        
        # 生成 token
        token = user.generate_token()
        
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'avatar_url': user.avatar_url,
                'role': user.role
            }
        })
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'message': 'Registration failed'}), 500

@auth.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # 验证必要字段
        if 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Missing email or password'}), 400
        
        user = User.objects(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({
                'message': 'Invalid email or password'
            }), 401
        
        # 登录用户
        login_user(user, remember=data.get('remember', False))
        
        # 生成 token
        token = user.generate_token()
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email,
                'avatar_url': user.avatar_url,
                'role': user.role
            }
        })
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'Login failed'}), 500

@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    logout_user()
    return jsonify({
        'message': 'Logout successful'
    })

@auth.route('/me')
@jwt_required
def get_current_user():
    return jsonify({
        'user': {
            'id': str(current_user.id),
            'name': current_user.name,
            'email': current_user.email,
            'avatar_url': current_user.avatar_url,
            'role': current_user.role
        }
    }) 