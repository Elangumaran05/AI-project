# MedAI: Personalised Medical Diagnosis Agent

A sophisticated AI-powered medical diagnosis chatbot built with Flask and machine learning, designed to assist with preliminary diabetes diagnosis through an intuitive conversational interface.

## 🚀 Features

### 🤖 **AI-Powered Diagnosis**
- Machine learning model for diabetes prediction
- Real-time analysis with confidence scores
- Comprehensive medical questionnaire

### 💬 **Intelligent Chat Interface**
- Dark theme with glass morphism design
- Conditional question flow (gender-aware)
- Float value support for precise medical data
- Real-time validation and error handling

### 📚 **Chat History Management**
- Complete conversation storage
- Session replay functionality
- Easy access to previous diagnoses
- New chat creation

### 🎨 **Modern UI/UX**
- Responsive dark theme design
- Glass morphism effects
- Smooth animations and transitions
- Professional medical-tech aesthetic

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite
- **Machine Learning**: scikit-learn
- **Styling**: Custom CSS with glass morphism effects

## 📋 Prerequisites

- Python 3.7+
- pip (Python package installer)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/medai-diagnosis-bot.git
cd medai-diagnosis-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask
pip install scikit-learn
pip install numpy
pip install joblib
```

### 4. Initialize Database
```bash
python setup_db.py
python setup_chat_db.py
```

### 5. Train the Model (if needed)
```bash
python train_model.py
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## 📖 Usage

### Starting a New Diagnosis
1. Click "New Chat" to begin a fresh consultation
2. Answer the questions in order:
   - Gender (Male/Female)
   - Age
   - Pregnancy count (for females only)
   - Medical measurements (glucose, blood pressure, etc.)
3. Receive your AI-powered diagnosis with confidence score

### Viewing Chat History
1. Click "Chat History" to see all previous sessions
2. Click on any session to replay the complete conversation
3. View diagnosis results and confidence scores

## 🏗️ Project Structure

```
medai-diagnosis-bot/
├── app.py                 # Main Flask application
├── train_model.py         # Model training script
├── setup_db.py           # Database initialization
├── setup_chat_db.py      # Chat history database setup
├── diabetes_model.pkl     # Trained ML model
├── diabetes.csv          # Training dataset
├── predictions.db        # Main database
├── chat_history.db       # Chat history database
├── TEMPLATES/
│   └── index.html        # Main UI template
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## 🔧 API Endpoints

- `GET /` - Main application interface
- `POST /predict` - AI diagnosis prediction
- `GET /chat-history` - Retrieve chat history
- `GET /chat-session/<id>` - Get specific session details
- `GET /chat-messages/<id>` - Get session messages

## 🎯 Key Features Explained

### Smart Question Flow
The application uses conditional logic to ask relevant questions:
- **Gender-based**: Pregnancy questions only for females
- **Medical data**: Comprehensive health metrics collection
- **Validation**: Real-time input validation with helpful error messages

### Chat History System
- **Complete Storage**: Every conversation is saved with timestamps
- **Message Replay**: View exact Q&A sequences
- **Session Management**: Easy navigation between old and new chats

### AI Diagnosis Process
1. **Data Collection**: Structured medical questionnaire
2. **ML Processing**: Trained model analyzes input data
3. **Result Generation**: Diagnosis with confidence percentage
4. **History Storage**: Automatic session saving

## 🎨 UI/UX Design

### Dark Theme Features
- **Gradient Backgrounds**: Professional blue gradients
- **Glass Morphism**: Semi-transparent containers with blur effects
- **Smooth Animations**: Hover effects and transitions
- **Responsive Design**: Works on all screen sizes

### User Experience
- **Intuitive Navigation**: Clear buttons and controls
- **Real-time Feedback**: Immediate validation and responses
- **Error Handling**: Helpful error messages instead of generic ones
- **Accessibility**: Clear typography and contrast

## 🔒 Privacy & Security

- **Local Storage**: All data stored locally in SQLite
- **No External APIs**: Complete offline functionality
- **Data Privacy**: No data transmission to external servers
- **Educational Purpose**: Clear disclaimers about medical advice

## 📝 Medical Disclaimer

⚠️ **Important**: This application is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- scikit-learn for machine learning capabilities
- Flask for the web framework
- The medical community for diabetes research and datasets

---

**Made with ❤️ for better healthcare accessibility**
