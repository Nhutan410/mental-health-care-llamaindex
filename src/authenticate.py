"""
User authentication module
"""

import yaml
import os
import hashlib
from src.global_settings import USERS_FILE


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Load users from YAML file"""
    if not os.path.exists(USERS_FILE):
        return {}
    
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        users = yaml.safe_load(file) or {}
    return users


def save_users(users):
    """Save users to YAML file"""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        yaml.dump(users, file, allow_unicode=True)


def register_user(username, password, email="", age="", gender=""):
    """
    Register a new user
    
    Args:
        username: Username
        password: Password
        email: Email address
        age: Age
        gender: Gender
        
    Returns:
        tuple: (success, message)
    """
    users = load_users()
    
    if username in users:
        return False, "Tên đăng nhập đã tồn tại!"
    
    users[username] = {
        'password': hash_password(password),
        'email': email,
        'age': age,
        'gender': gender
    }
    
    save_users(users)
    return True, "Đăng ký thành công!"


def login_user(username, password):
    """
    Login user
    
    Args:
        username: Username
        password: Password
        
    Returns:
        tuple: (success, user_info)
    """
    users = load_users()
    
    if username not in users:
        return False, None
    
    if users[username]['password'] == hash_password(password):
        user_info = users[username].copy()
        user_info.pop('password')
        return True, user_info
    
    return False, None


def get_user_info(username):
    """Get user information"""
    users = load_users()
    if username in users:
        user_info = users[username].copy()
        user_info.pop('password', None)
        return user_info
    return None