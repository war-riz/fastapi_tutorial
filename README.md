# 🚀 FastAPI Social Media Account Management API

## 📌 Overview
FastAPI-based API for managing social media accounts, providing authentication, OAuth integration, and secure token storage.

## ⚡ Features
- High-performance API with async support
- OAuth integration for social media accounts
- JWT authentication & secure token storage
- Automatic validation with Pydantic
- Interactive API documentation (Swagger & ReDoc)

## 🔧 Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Running the API
```bash
uvicorn main:app --reload
```

## 📄 API Documentation
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
 

## 🛡 Security
- Uses OAuth for social media authentication
- Stores tokens securely
- Implements JWT authentication

## 🤝 Contributing
Pull requests are welcome! Please open an issue first to discuss changes.

## 📜 License
This project is licensed under the MIT License. 

## ⚡ Author
Created by war-riz (https://github.com/war-riz/fastapi_tutorial).

