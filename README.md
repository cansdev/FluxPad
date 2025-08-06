# FluxPad 📊

> A lightweight, full-stack web application for intelligent data interaction through LLM-powered agents

FluxPad enables users to upload, visualize, and transform structured datasets (CSV, Excel) with an intuitive interface backed by AI-driven querying and analysis capabilities.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-15.4.5-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)
![Python](https://img.shields.io/badge/Python-3.12+-3776ab)

## ✨ Key Features

- **📤 Data Upload & Management**: Seamlessly import CSV and Excel files with automatic schema detection
- **🔍 Intelligent Querying**: Natural language queries powered by local LLM integration
- **🗃️ Structured Storage**: PostgreSQL backend with optimized data modeling via Supabase
- **🎨 Modern UI**: Responsive dashboard built with Next.js and Tailwind CSS
- **🔐 Secure Authentication**: JWT-based authentication system
- **🤖 AI-Powered Insights**: Automated metadata generation and column mapping suggestions
- **🔄 Data Transformation**: Advanced filtering and transformation through prompt-to-SQL interface
- **📈 Extensible Architecture**: Designed for enterprise workflows and API integrations

## 🛠️ Tech Stack

### Frontend
- **Next.js 15.4.5** - React framework with App Router
- **React 19** - UI library with latest features
- **Tailwind CSS 4** - Utility-first CSS framework
- **TypeScript 5** - Type-safe development
- **Supabase JS SDK** - Database client and authentication

### Backend
- **FastAPI 0.104.1** - High-performance Python web framework
- **Uvicorn** - ASGI server with WebSocket support
- **Custom JWT Authentication** - Secure token-based auth
- **SQLAlchemy/Async ORM** - Database abstraction layer
- **Python 3.12+** - Modern Python runtime

### Database & Infrastructure
- **Supabase Cloud** - Managed PostgreSQL with real-time capabilities
- **PostgreSQL** - Robust relational database
- **Custom database schema** - No Supabase Auth or Edge Functions

### AI/ML Integration
- **HuggingFace Transformers** - Local LLM hosting
- **Prompt-to-SQL Engine** - Natural language to database queries
- **OpenAI API** (optional) - Enhanced language model capabilities

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** and **pnpm**
- **Python 3.12+** and **pip**
- **Supabase account** for database hosting

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fluxpad.git
cd fluxpad
```

### 2. Environment Setup

Create environment files for both frontend and backend:

**Frontend (`web/.env.local`):**
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

**Backend (`api/.env`):**
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
JWT_SECRET=your_jwt_secret_key
DATABASE_URL=your_postgresql_connection_string
OPENAI_API_KEY=your_openai_key_optional
HUGGINGFACE_API_KEY=your_hf_key_optional
```

### 3. Database Setup

1. Create a new Supabase project
2. Run the database migrations:
```sql
-- Create tables for user data, file uploads, and metadata
-- (Database schema will be provided in /docs/schema.sql)
```

### 4. Backend Setup

```bash
cd api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 5. Frontend Setup

```bash
cd web

# Install dependencies
pnpm install

# Run development server
pnpm dev
```

The application will be available at `http://localhost:3000`

## 🔧 Configuration

### Supabase Integration

FluxPad uses Supabase as a managed PostgreSQL provider with the following approach:

- **Database Only**: No Supabase Auth or Edge Functions
- **Custom JWT**: Self-managed authentication system
- **Direct SQL**: Raw PostgreSQL queries for optimal performance
- **Real-time Updates**: Optional Supabase real-time subscriptions

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
│   ├── supabase_client.py # Database client
│   ├── requirements.txt   # Python dependencies
│   └── ...
├── web/                   # Next.js frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   └── lib/          # Utilities and clients
│   ├── public/           # Static assets
│   ├── package.json      # Node.js dependencies
│   └── ...
├── docs/                 # Documentation (planned)
├── tests/                # Test suites (planned)
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

Key endpoints:
- `POST /auth/login` - User authentication
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