# FluxPad 📊

> A lightweight, full-stack web application for intelligent data interaction through LLM-powered agents

FluxPad enables users to upload, visualize, and transform structured datasets (CSV, Excel) with an intuitive interface backed by AI-driven querying and analysis capabilities.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-15.4.5-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)
![Python](https://img.shields.io/badge/Python-3.12+-3776ab)

## ✨ Key Features

### 🚀 **Currently Implemented:**
- **🔐 Secure Authentication**: Production-ready JWT authentication with auto-generated secrets
- **👤 User Management**: Registration, login, and protected dashboard
- **🎨 Modern UI**: Responsive interface built with Next.js 15 and Tailwind CSS 4
- **🔒 Security**: Bcrypt password hashing, secure token storage, CORS protection
- **⚡ Fast API**: High-performance FastAPI backend with automatic documentation

### 🚧 **Coming Soon:**
- **📤 Data Upload & Management**: CSV and Excel file import with automatic schema detection
- **🔍 Intelligent Querying**: Natural language queries powered by LLM integration
- **🤖 AI-Powered Insights**: Automated metadata generation and column mapping
- **🔄 Data Transformation**: Advanced filtering through prompt-to-SQL interface
- **📈 Extensible Architecture**: Enterprise workflows and API integrations

## 🛠️ Tech Stack

### Frontend
- **Next.js 15.4.5** - React framework with App Router
- **React 19** - UI library with latest features
- **Tailwind CSS 4** - Utility-first CSS framework
- **TypeScript 5** - Type-safe development

### Backend
- **FastAPI 0.104.1** - High-performance Python web framework
- **Uvicorn** - ASGI server for production deployment
- **PyJWT** - JSON Web Token implementation
- **Passlib + Bcrypt** - Secure password hashing
- **Pydantic** - Data validation and serialization
- **Python 3.12+** - Modern Python runtime

### Database & Storage
- **SQLite** - Lightweight, fast, zero-config database
- **SQLAlchemy** - Modern async ORM with full SQL support
- **aiosqlite** - Async SQLite driver for high performance

### Security & Authentication
- **Custom JWT System** - Auto-generated secrets, access + refresh tokens
- **Bcrypt Password Hashing** - Industry-standard password security
- **CORS Protection** - Cross-origin request security
- **Secure Token Storage** - Automatic secret generation and file permissions

### Planned Integrations
- **HuggingFace Transformers** - Local LLM hosting (planned)
- **OpenAI API** - Enhanced language capabilities (optional)

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** and **pnpm**
- **Python 3.12+** and **pip**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fluxpad.git
cd fluxpad
```

### 2. Backend Setup

```bash
cd api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

**✨ Auto-Configuration:**
- **JWT Secret**: Automatically generated on first run (512-bit entropy)
- **Database**: SQLite database auto-creates with proper schema
- **No manual setup**: Just install dependencies and run!

### 3. Frontend Setup

```bash
cd web

# Install dependencies
pnpm install

# Run development server
pnpm dev
```

The application will be available at `http://localhost:3000`

### 4. Test the Full System

1. **Visit** `http://localhost:3000`
2. **Register** a new account (Click "Get Started")
3. **Login** and access the protected dashboard
4. **Restart the server** - your account persists!
5. **Check database**: `sqlite3 api/fluxpad.db "SELECT email, full_name FROM users;"`

## 📊 **Current Implementation Status**

### ✅ **Completed Features:**
- **Authentication System**: Full JWT implementation with registration, login, logout
- **Database Integration**: SQLite database with persistent user storage
- **Frontend Pages**: Landing page, login, register, protected dashboard
- **Security**: Auto-generated JWT secrets, bcrypt password hashing
- **API Documentation**: Automatic Swagger/OpenAPI docs at `/docs`
- **Development Setup**: Easy local development with hot reload
- **Data Persistence**: Users and data survive server restarts

### 🔄 **In Progress:**
- File upload system for CSV/Excel files
- Data visualization and management interface

### 📋 **Next Steps:**
1. File upload system for CSV/Excel files
2. Data visualization and table display
3. AI-powered natural language querying
4. Production deployment configuration
5. Advanced data transformation features

## 🔧 Configuration

### SQLite Database

FluxPad uses SQLite for fast, reliable local storage:

- **Zero Configuration**: Database auto-creates on first run
- **File-based**: Single `fluxpad.db` file contains everything
- **Fast Queries**: Direct file access, no network latency
- **Full SQL Support**: Complex queries, joins, indexes, transactions
- **Production Ready**: Scales to thousands of users and GBs of data

### LLM Integration

The application supports multiple LLM backends:

1. **Local HuggingFace Models**: 
   - Recommended: `microsoft/DialoGPT-medium` or `facebook/blenderbot-400M`
   - Runs entirely offline for data privacy

2. **OpenAI API**: 
   - GPT-3.5/GPT-4 for enhanced capabilities
   - Requires API key and internet connection

3. **Custom Models**: 
   - Extensible architecture for proprietary models
   - Implements standard prompt-to-SQL interface

### Prompt-to-SQL Engine

The core AI functionality translates natural language queries into SQL:

```python
# Example: "Show me all sales data from last quarter"
# Translates to: SELECT * FROM sales WHERE date >= '2024-01-01' AND date <= '2024-03-31'
```

## 📁 Project Structure

```
fluxpad/
├── api/                    # FastAPI backend
│   ├── main.py            # Application entry point
│   ├── auth.py            # JWT authentication system
│   ├── database.py        # SQLite database models
│   ├── crud.py            # Database operations
│   ├── requirements.txt   # Python dependencies
│   ├── fluxpad.db         # SQLite database (auto-created)
│   └── .jwt_secret        # Auto-generated JWT secret
├── web/                   # Next.js frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   │   ├── login/    # Login page
│   │   │   ├── register/ # Registration page
│   │   │   └── dashboard/# Protected dashboard
│   │   └── lib/          # Utilities (planned)
│   ├── public/           # Static assets
│   └── package.json      # Node.js dependencies
└── README.md
```

## 🚢 Deployment

### Frontend (Vercel)

```bash
cd web
pnpm build

# Deploy to Vercel
npx vercel --prod
```

### Backend (Railway/Fly.io)

**Railway:**
```bash
cd api
railway login
railway init
railway up
```

**Fly.io:**
```bash
cd api
flyctl launch
flyctl deploy
```

### Environment Variables

Ensure all production environment variables are configured in your deployment platform:

- Database connection strings
- JWT secrets
- API keys for external services
- CORS origins for frontend domain

## 🧪 Testing

```bash
# Backend tests
cd api
python -m pytest

# Frontend tests
cd web
pnpm test
```

## 📖 API Documentation

Once the backend is running, visit:
- **Interactive Docs**: `http://localhost:8000/docs`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### 🔐 **Current Authentication Endpoints:**
- `POST /auth/register` - User registration (returns access + refresh tokens)
- `POST /auth/login` - User authentication (returns access + refresh tokens)
- `GET /auth/me` - Get current user info (protected)
- `POST /auth/refresh` - Refresh access token using refresh token
- `GET /ping` - Health check endpoint

### 🚧 **Planned Data Endpoints:**
- `POST /data/upload` - File upload and processing
- `GET /data/query` - Natural language querying
- `POST /data/transform` - Data transformation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all new frontend code
- Write tests for new features
- Update documentation as needed

## 📋 Roadmap

- [ ] **Enhanced AI Models**: Integration with larger language models
- [ ] **Real-time Collaboration**: Multi-user editing and annotations
- [ ] **API Integrations**: Connect with external data sources
- [ ] **Advanced Visualizations**: Interactive charts and dashboards
- [ ] **Enterprise Features**: Role-based access control, audit logs
- [ ] **Mobile App**: React Native companion application

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/fluxpad/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/fluxpad/discussions)
- **Email**: your.email@example.com

## 🌟 Acknowledgments

- [Supabase](https://supabase.com) for managed PostgreSQL
- [Vercel](https://vercel.com) for frontend hosting
- [HuggingFace](https://huggingface.co) for transformer models
- [FastAPI](https://fastapi.tiangolo.com) for the excellent Python framework

---

**Built with ❤️ for the data community**