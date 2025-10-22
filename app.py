from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
import sqlite3
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# Load your trained AI model
model = joblib.load('diabetes_model.pkl')
DB_NAME = 'predictions.db'
CHAT_DB_NAME = 'chat_history.db'

# Define the route for the home page (serves the chat UI)
@app.route('/')
def home():
    return render_template('index.html')

# Define the route that handles the prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the JSON request sent by the chatbot
    data = request.get_json()
    
    # 1. Get all the data from the form
    # The order MUST match the list in train_model.py
    # Handle pregnancy data - if not provided (for males), default to 0
    pregnancies = float(data.get('pregnancies', 0))
    
    form_data = [
        pregnancies,
        float(data['glucose']),
        float(data['bp']),
        float(data['skin']),
        float(data['insulin']),
        float(data['bmi']),
        float(data['dpf']),
        float(data['age'])
    ]
    
    # 2. Make the AI prediction
    input_data = np.array([form_data])
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)
    
    if prediction[0] == 1:
        result = "Positive"
        confidence = prediction_proba[0][1] * 100
    else:
        result = "Negative"
        confidence = prediction_proba[0][0] * 100

    diagnosis_text = f"Diagnosis: {result} for Diabetes (Confidence: {confidence:.2f}%)"
    
    # 3. Use a cursor to save the prediction to the database
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        # Prepare data for SQL, adding result and confidence
        db_data = tuple(form_data + [result, confidence])
        
        c.execute("""
            INSERT INTO predictions (pregnancies, glucose, bp, skin, insulin, bmi, dpf, age, diagnosis, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, db_data)
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error saving to database: {e}")
    
    # 4. Save chat session to history
    session_id = str(uuid.uuid4())
    try:
        conn = sqlite3.connect(CHAT_DB_NAME)
        c = conn.cursor()
        
        # Save session data
        c.execute('''
            INSERT INTO chat_sessions (session_id, user_data, diagnosis, confidence)
            VALUES (?, ?, ?, ?)
        ''', (session_id, json.dumps(data), result, confidence))
        
        # Save individual messages for this session
        questions = [
            { 'key': 'gender', 'text': 'First, what is your gender? (Male/Female)' },
            { 'key': 'age', 'text': 'What is your age?' },
            { 'key': 'pregnancies', 'text': 'How many times have you been pregnant?', 'conditional': True, 'dependsOn': 'gender', 'showIf': 'Female' },
            { 'key': 'glucose', 'text': 'What is your Plasma Glucose concentration (mg/dl)?' },
            { 'key': 'bp', 'text': 'What is your Diastolic Blood Pressure (mm Hg)?' },
            { 'key': 'skin', 'text': 'What is your Triceps Skinfold Thickness (mm)?' },
            { 'key': 'insulin', 'text': 'What is your 2-Hour Serum Insulin (mu U/ml)?' },
            { 'key': 'bmi', 'text': 'What is your Body Mass Index (BMI)?' },
            { 'key': 'dpf', 'text': 'What is your Diabetes Pedigree Function value?' }
        ]
        
        # Add welcome messages
        c.execute('''
            INSERT INTO chat_messages (session_id, message_type, message_content)
            VALUES (?, ?, ?)
        ''', (session_id, 'bot', 'Hello! I am MedAI, your personalised medical diagnosis agent designed to assist with preliminary diabetes diagnosis.'))
        
        c.execute('''
            INSERT INTO chat_messages (session_id, message_type, message_content)
            VALUES (?, ?, ?)
        ''', (session_id, 'bot', '⚠️ Disclaimer: I am not a real doctor. This is an educational project. Please consult a medical professional for any health concerns.'))
        
        # Add Q&A messages
        for question in questions:
            if question['key'] in data:
                # Add bot question
                c.execute('''
                    INSERT INTO chat_messages (session_id, message_type, message_content)
                    VALUES (?, ?, ?)
                ''', (session_id, 'bot', question['text']))
                
                # Add user answer
                c.execute('''
                    INSERT INTO chat_messages (session_id, message_type, message_content)
                    VALUES (?, ?, ?)
                ''', (session_id, 'user', str(data[question['key']])))
        
        # Add final messages
        c.execute('''
            INSERT INTO chat_messages (session_id, message_type, message_content)
            VALUES (?, ?, ?)
        ''', (session_id, 'bot', 'Thank you. Analyzing your data now...'))
        
        c.execute('''
            INSERT INTO chat_messages (session_id, message_type, message_content)
            VALUES (?, ?, ?)
        ''', (session_id, 'bot', diagnosis_text))
        
        c.execute('''
            INSERT INTO chat_messages (session_id, message_type, message_content)
            VALUES (?, ?, ?)
        ''', (session_id, 'bot', 'This is an educational project. Please consult a real doctor for any health concerns.'))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error saving chat history: {e}")
    
    # 5. Return the result as JSON
    return jsonify({
        'diagnosis_text': diagnosis_text,
        'session_id': session_id
    })

# Route to get chat history
@app.route('/chat-history', methods=['GET'])
def get_chat_history():
    try:
        conn = sqlite3.connect(CHAT_DB_NAME)
        c = conn.cursor()
        
        c.execute('''
            SELECT session_id, created_at, diagnosis, confidence 
            FROM chat_sessions 
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        
        sessions = []
        for row in c.fetchall():
            sessions.append({
                'session_id': row[0],
                'created_at': row[1],
                'diagnosis': row[2],
                'confidence': row[3]
            })
        
        conn.close()
        return jsonify({'sessions': sessions})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get specific chat session
@app.route('/chat-session/<session_id>', methods=['GET'])
def get_chat_session(session_id):
    try:
        conn = sqlite3.connect(CHAT_DB_NAME)
        c = conn.cursor()
        
        c.execute('''
            SELECT user_data, diagnosis, confidence, created_at 
            FROM chat_sessions 
            WHERE session_id = ?
        ''', (session_id,))
        
        row = c.fetchone()
        if row:
            return jsonify({
                'user_data': json.loads(row[0]),
                'diagnosis': row[1],
                'confidence': row[2],
                'created_at': row[3]
            })
        else:
            return jsonify({'error': 'Session not found'}), 404
            
        conn.close()
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get chat messages for a session
@app.route('/chat-messages/<session_id>', methods=['GET'])
def get_chat_messages(session_id):
    try:
        conn = sqlite3.connect(CHAT_DB_NAME)
        c = conn.cursor()
        
        c.execute('''
            SELECT message_type, message_content, timestamp 
            FROM chat_messages 
            WHERE session_id = ? 
            ORDER BY timestamp ASC
        ''', (session_id,))
        
        messages = []
        for row in c.fetchall():
            messages.append({
                'type': row[0],
                'content': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return jsonify({'messages': messages})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)