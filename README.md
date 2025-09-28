# RecruitAI Pro 🚀

> Professional AI-powered recruitment screening assistant

## 📋 Project Overview

RecruitAI Pro is a comprehensive AI-powered recruitment screening system that automatically analyzes resume match scores, generates personalized interview questions, and provides detailed analysis reports. Built with modern technologies and powered by Zhipu AI.

## ✨ Features

### 🎯 Core Functionality
- **Smart Resume Analysis**: Automatically parse and analyze candidate resumes
- **Intelligent Matching**: Calculate match scores between candidates and job requirements
- **Personalized Questions**: Generate tailored interview questions based on analysis
- **Comprehensive Reports**: Detailed candidate profiles with strengths, weaknesses, and potential
- **Visual Analytics**: Interactive charts and graphs for better insights

### 🔧 Technical Features
- **File Upload Support**: PDF and DOCX resume upload
- **Real-time Processing**: Fast AI-powered analysis
- **Interactive Dashboard**: Modern, responsive user interface
- **Export Capabilities**: PDF report generation and download
- **Multi-language Support**: Chinese and English interface

## 🛠️ Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Fast build tool
- **Element Plus** - Vue 3 component library
- **Lucide Vue** - Beautiful icons
- **ECharts** - Data visualization
- **Pinia** - State management

### Backend
- **Python 3.8+** - Programming language
- **FastAPI** - Modern web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database
- **Zhipu AI API** - AI analysis engine
- **Uvicorn** - ASGI server

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Zhipu AI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/recruitai-pro.git
   cd recruitai-pro
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Zhipu AI API key
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
recruitai-pro/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   └── main.py            # Application entry point
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/         # Page components
│   │   ├── router/        # Vue Router
│   │   └── api/           # API services
│   └── package.json
├── docker-compose.yml      # Docker configuration
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Zhipu AI Configuration
ZHIPU_API_KEY=your_zhipu_api_key_here
ZHIPU_MODEL=glm-4

# Database Configuration
DATABASE_URL=sqlite:///./recruit_assistant.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## 📊 Usage

1. **Upload Resume**: Upload candidate resume (PDF/DOCX)
2. **Enter Job Description**: Provide detailed job requirements
3. **AI Analysis**: System automatically analyzes match score
4. **Generate Questions**: Create personalized interview questions
5. **View Reports**: Access comprehensive analysis reports
6. **Export Results**: Download PDF reports for sharing

## 🎨 Screenshots

![Home Page](docs/screenshots/home.png)
![Analysis Results](docs/screenshots/analysis.png)
![Reports Dashboard](docs/screenshots/reports.png)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Zhipu AI](https://www.zhipuai.cn/) for providing the AI analysis capabilities
- [Element Plus](https://element-plus.org/) for the beautiful UI components
- [Vue.js](https://vuejs.org/) for the amazing frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance backend

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact us at support@recruitai-pro.com
- Check our [documentation](docs/)

---

**RecruitAI Pro** - Making recruitment smarter, faster, and more accurate! 🎯