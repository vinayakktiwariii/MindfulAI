# 🧠 NAINA - Mental Wellness AI Platform

> Your Personal AI Mental Wellness Companion  
> Built by ArqonX AI Technologies | Founder: Vinayak Tiwari

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

## 🌟 Features

- ✅ **Crisis Detection**: Real-time mental health crisis identification
- ✅ **Emotion Analysis**: Advanced NLP for emotion intensity tracking
- ✅ **Context Memory**: Remembers conversation themes and patterns
- ✅ **Wellness Insights**: AI-generated personalized recommendations
- ✅ **Analytics Dashboard**: Detailed conversation analytics
- ✅ **Dark/Light Theme**: Customizable UI experience
- ✅ **Privacy-First**: Encrypted conversations and secure data storage

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Bytez API Key ([Get one here](https://bytez.com))

### Installation

1. **Clone the repository**
git clone https://github.com/vinayakktiwariii/MindfulAI.git
cd MindfulAI

2. **Create virtual environment**
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Set up environment variables**
cp .env.example .env

5. **Run the backend**
python data/crisis_api_server.py

6. **Run the frontend** (in another terminal)
cd frontend
python -m http.server 5500

7. **Open in browser**
http://127.0.0.1:5500



## 📁 Project Structure
MindfulAI/
├── mindfulai_backend/ # Backend core modules
│ ├── chatbot/ # AI chatbot engine
│ ├── analytics/ # Analytics & insights
│ └── core/ # Core utilities
├── data/ # Data processing & API server
├── frontend/ # Web UI (HTML/CSS/JS)
├── training/ # Model training scripts
└── requirements.txt # Python dependencies


## 🛠️ Technologies

- **Backend**: Python, Bytez SDK, Advanced NLP
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI Model**: Qwen2.5-3B-Instruct
- **Deployment**: Render, Vercel

## 📊 Features Overview

### Week 4: Production Features
- User profiles
- Conversation history with metadata
- Analytics dashboard
- Export functionality (JSON/TXT)

### Week 5: Advanced NLP
- Emotion intensity analysis
- Intent detection
- Context tracking & memory
- Wellness recommendations

## 🔐 Security

- API keys stored in environment variables
- User data encrypted at rest
- No sensitive data in repository
- CORS protection enabled

## 📝 Environment Variables

Required variables (see `.env.example`):

- `BYTEZ_API_KEY`: Your Bytez API key
- `API_HOST`: Backend host (default: 127.0.0.1)
- `API_PORT`: Backend port (default: 5000)

## 🚀 Deployment

### Deploy to Render

1. Push to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Add environment variables
5. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👨‍💻 Author

**Vinayak Tiwari**  
Founder, ArqonX AI Technologies

- GitHub: [@yourusername](https://github.com/yourusername)
- Website: [arqonx.com](https://arqonx.com)

## 🙏 Acknowledgments

- Bytez AI for the powerful SDK
- Mental health professionals for consultation
- Open-source community

## 📞 Support

For support, email support@arqonx.com or open an issue.

---

**⭐ Star this repo if you find it helpful!**
