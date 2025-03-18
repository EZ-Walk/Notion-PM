from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

users_bp = Blueprint('users', __name__)

@users_bp.route('/initiate_auth', methods=['POST'])
def initiate_auth():
    data = request.json
    email = data.get('email')
    print(data)
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    try:
        # Check if the user exists
        user = supabase.auth
        print(user)
        
        if user:
            # User exists, send magic link
            response = supabase.auth.sign_in_with_otp({"email": email})
            print(response)
            return jsonify({"message": "Magic link sent to your email", "isNewUser": False}), 200
        else:
            # User doesn't exist, initiate sign up
            return jsonify({"message": "Please complete sign up", "isNewUser": True}), 200
    except Exception as e:
        print(f"Error in initiate_auth: {str(e)}")  # Log the error
        return jsonify({"error": str(e)}), 400
    
@users_bp.route('/complete_signup', methods=['POST'])
def complete_signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        return jsonify({"message": "User created successfully", "user": response.user.email}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return jsonify({"message": "Login successful", "user": response.user.email, "token": response.session.access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/logout', methods=['POST'])
def logout():
    try:
        supabase.auth.sign_out()
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ... other routes as needed ...
# ... other routes as needed ...