# RecruitAI Pro 🚀

> Professional AI‑powered recruitment screening assistant

## 📋 Project Overview

RecruitAI Pro is a comprehensive AI recruitment assistant that analyzes resume–JD fit, generates personalized interview questions, and produces visual, decision‑ready reports. It is built with a Vue 3 frontend, a FastAPI backend, ECharts visualizations, and integrates Zhipu AI for text analysis. The app supports Chinese/English UI and is production‑ready with Docker and Nginx.

## ✨ Highlights

- Smart Resume Analysis**: Parse PDF/DOCX resumes and evaluate against JD
- Match Scoring**: Quantified candidate–JD match with robust fallback logic
- Personalized Questions**: Tailored interview prompts from the analysis
- Rich Visuals**: Skill radar, comparisons, distributions, and more with ECharts
- Resilient UX**: Default content and error handling even for low/invalid JSON
- Responsive UI**: Modern layouts, dark mode, and optimized print styles
- Feedback Loop**: Built‑in survey entry and one‑click contact

## 🛠️ Tech Stack

### Frontend
- **Vue 3 + Vite - Progressive JavaScript framework
- **Element Plus (components) - Vue 3 component library
- **Lucide Vue (icons) - Beautiful icons
- **ECharts (visualizations) - Data visualization
- **Pinia (state) - State management

### Backend
- Python 3.11 + FastAPI
- SQLAlchemy + SQLite (default)
- Zhipu AI API (analysis)
- Uvicorn (ASGI)

## 🚀 Quick Start
### DevOps
- Docker & Docker Compose
- Nginx (static serving / reverse proxy)
- Compose Watch for live rebuild/sync in dev

## 🚀 Run with Docker (Recommended)

> One‑command production build with Nginx + API.

1) Ensure Docker is installed:
   - Docker Desktop: https://www.docker.com/products/docker-desktop/
   - Docker Compose v2: https://docs.docker.com/compose/

2) Set your Zhipu API key (optional here if you configure later):
```bash
export ZHIPU_API_KEY="your_zhipu_api_key_here"
```

3) Build images and start the stack:
```bash
docker compose build --no-cache
docker compose up -d
```

4) Access:
- Frontend (via Nginx): http://localhost
- Frontend (direct): http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs

5) Stop:
```bash
docker compose down
```

### Live Dev with Compose Watch (Hot sync/rebuild)

We provide a dev‑friendly workflow using Compose Watch. It will auto‑sync backend code and rebuild the frontend image when `src` changes.

Start watching:
```bash
docker compose watch
```

Notes:
- Backend syncs `./backend` → container `/app` and supports quick reloads.
- Frontend rebuilds when `frontend/src`, `public`, or build config changes.

## 🧩 Manual Local Development (Alternative)

Prerequisites:
- Node.js 16+ and npm
- Python 3.8+

Backend:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # add your ZHIPU_API_KEY
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Configuration

Create a `.env` from the provided template at repo root:
```bash
cp env.txt .env
```

Or create a `.env` in `backend/` manually:
```env
# Zhipu AI Configuration
ZHIPU_API_KEY=your_zhipu_api_key_here
ZHIPU_MODEL=glm-4

# Database Configuration
DATABASE_URL=sqlite:///./recruitment_assistant.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

Docker Compose maps `./backend/uploads` and the SQLite DB file for persistence.

### Get a Zhipu AI API Key

1) Visit the Zhipu AI Open Platform: https://open.bigmodel.cn/
2) Sign up or sign in with your account.
3) Create a new API key in the Console (Keys/Access Tokens).
4) Copy the key and set it in your `.env` as `ZHIPU_API_KEY`.
5) Optional: adjust `ZHIPU_MODEL` (e.g., `glm-4.5`).


## 📁 Project Structure

```
recruitment-assistant/
├── backend/                      # FastAPI backend
│   ├── ai_client.py              # AI analysis and chart data generation
│   ├── main.py                   # FastAPI entry
│   ├── requirements.txt          # Backend deps
│   └── ...
├── frontend/                     # Vue 3 frontend
│   ├── src/
│   │   ├── components/           # Reusable components (e.g., FileUpload)
│   │   ├── views/                # Pages (Home, Analysis, Reports, About)
│   │   ├── store/                # Pinia store
│   │   └── api/                  # API service
│   ├── Dockerfile                # Frontend builder + Nginx static
│   └── ...
├── nginx/nginx.conf              # Nginx config
├── docker-compose.yml            # Backend + Frontend + Nginx
└── README.md
```

## 📊 Key Features in Detail

- Robust JSON parsing with multiple extraction strategies; safe fallbacks
- Default analysis and charts even with malformed AI responses
- Expanded, categorized skill keyword extraction across many roles/industries
- New chart types: skill comparison, comprehensive radar, and more
- UI/UX optimizations: clean white backgrounds, responsive, dark mode, print styles
- Icon strategy: Lucide for general UI, Element Plus icons retained for specific buttons

## 🧪 API Quick Peek

Open Swagger at http://localhost:8000/docs to inspect and try endpoints.

Typical flow:
1. Upload resume (PDF/DOCX)
2. Submit JD text
3. Receive analysis JSON and render charts on the frontend

## 🙋 Feedback & Survey

- Survey (Google Forms): https://docs.google.com/forms/d/e/1FAIpQLSfxKzQp7roJpC8827vakv9PiAweonADNBGxmObe_u0ly36Ijg/viewform?usp=header
- Suggestions: wby106006@gmail.com

We warmly welcome professional advice from HR/recruiting practitioners. Your domain expertise (e.g., competencies, evaluation criteria, interview frameworks, industry‑specific skill taxonomies) is invaluable to help us improve model prompts, scoring logic, and chart insights. If you are open to sharing best practices or sample redacted data, please contact us — it will greatly accelerate the product’s accuracy and usefulness in real hiring workflows.

## 📌 Current Limitations & Roadmap

| Area | Current Status | Impact | Near‑Term Plan | Longer‑Term Plan |
| --- | --- | --- | --- | --- |
| Analysis speed | ~2–3 minutes per analysis; user needs to wait patiently during resume analysis | Slower feedback loop | Optimize prompts and streaming; reduce payload size; cache static steps | Introduce multi‑model strategy (fast model for coarse pass, strong model for final synthesis); parallelize subtasks |
| Feature completeness | Some features not yet implemented (resume browsing in app, resume download/export, richer report actions) | Usability gaps | Add resume file preview, download/export buttons, and report quick actions | Full file management (versioning, annotations), batch processing, candidate comparison |
| Accuracy & depth | Good baseline but room for more professional, role‑aware insights | Decision quality | Expand domain taxonomies and rules; refine scoring weights | Use specialized models per domain; add evaluator models; human‑in‑the‑loop calibration |
| Skill extraction | Broad library, may miss niche/industry‑specific terms | Partial coverage | Extend keyword library by industry; add synonym/alias mapping | Embed‑based extraction + adaptive dictionaries learned from data |
| Charts & insights | Solid set of charts; some advanced visuals pending | Insight density | Add heatmaps, correlation, Sankey, timelines, sensitivity analysis | Auto‑insight generation and recommendations based on patterns |
| Reliability | Fallbacks exist for malformed AI output; rare render issues historically | Occasional manual refresh | Harden parsers; more unit tests; stricter schemas | Telemetry‑driven robustness; canary checks before render |

Notes:
- While analysis is running, please allow 2–3 minutes for completion.
- We’re actively working to shorten latency and enhance accuracy with multi‑model pipelines.

## 🧰 Troubleshooting

- Vite “Outdated Optimize Dep” during dev: stop dev server, clear `node_modules/.vite`, then reinstall.
- ECharts registration errors: we use full `echarts` import for compatibility.
- If changes don’t show in Docker:
  - Rebuild the affected service: `docker compose build frontend && docker compose up -d frontend`
  - Or use dev mode: `docker compose watch`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/awesome`)
3. Commit (`git commit -m "feat: add awesome"`)
4. Push (`git push origin feature/awesome`)
5. Open a Pull Request

## 📄 License

MIT License — see [LICENSE](LICENSE).

## 🙏 Acknowledgments

- [Zhipu AI](https://www.zhipuai.cn/)
- [Element Plus](https://element-plus.org/)
- [Vue.js](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

## 📞 Support

- Open a GitHub issue
- Email: wby106006@gmail.com

---

**RecruitAI Pro** — Make recruitment smarter, faster, and more accurate. 🎯
