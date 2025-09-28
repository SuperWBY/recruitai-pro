<template>
  <div class="about-page">
    <!-- 头部导航 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo">
          <Cpu class="w-6 h-6" />
          <span>RecruitAI Pro</span>
        </div>
        <div class="nav-menu">
          <el-menu mode="horizontal" :default-active="$route.path" router>
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/reports">分析报告</el-menu-item>
            <el-menu-item index="/about">关于</el-menu-item>
          </el-menu>
        </div>
        <div class="header-actions">
          <el-button @click="goBack">
            <ArrowLeft class="w-4 h-4" />
            返回首页
          </el-button>
        </div>
      </div>
    </el-header>

    <!-- 主要内容 -->
    <el-main class="main-content">
      <div class="container">
        <!-- 产品介绍 -->
        <div class="hero-section">
          <div class="hero-content">
            <h1 class="hero-title">
              <Trophy class="w-6 h-6" />
              AI招聘筛选助手
            </h1>
            <p class="hero-subtitle">
              基于智谱清言AI技术的智能招聘筛选系统，让招聘更高效、更精准
            </p>
            <div class="hero-stats">
              <div class="stat-item">
                <div class="stat-number">100%</div>
                <div class="stat-label">AI驱动</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">10+</div>
                <div class="stat-label">分析维度</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">秒级</div>
                <div class="stat-label">分析速度</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 功能特色 -->
        <div class="features-section">
          <h2 class="section-title">
            <Star class="w-6 h-6" />
            核心功能
          </h2>
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="8">
              <div class="feature-card">
                <div class="feature-icon">
                  <BarChart3 class="w-5 h-5" />
                </div>
                <h3>智能匹配分析</h3>
                <p>基于先进的AI算法，深度分析简历与职位描述的匹配度，提供0-100分的量化评分</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <div class="feature-card">
                <div class="feature-icon">
                  <MessageSquare class="w-5 h-5" />
                </div>
                <h3>个性化面试问题</h3>
                <p>根据候选人背景和职位要求，自动生成10个针对性面试问题，提升面试效率</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <div class="feature-card">
                <div class="feature-icon">
                  <User class="w-5 h-5" />
                </div>
                <h3>候选人画像</h3>
                <p>深度分析候选人技能、经验、教育背景，生成完整的能力画像和发展潜力评估</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <div class="feature-card">
                <div class="feature-icon">
                  <BarChart3 class="w-5 h-5" />
                </div>
                <h3>可视化报告</h3>
                <p>生成包含图表和详细分析的完整报告，支持导出和分享，便于HR决策参考</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <div class="feature-card">
                <div class="feature-icon">
                  <FileText class="w-5 h-5" />
                </div>
                <h3>多格式支持</h3>
                <p>支持PDF、DOCX、DOC等多种简历格式，智能解析和提取关键信息</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <div class="feature-card">
                <div class="feature-icon">
                  <Clock class="w-5 h-5" />
                </div>
                <h3>快速响应</h3>
                <p>秒级完成简历分析，大幅提升招聘效率，让HR专注于更重要的工作</p>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 技术架构 -->
        <div class="tech-section">
          <h2 class="section-title">
            <Settings class="w-6 h-6" />
            技术架构
          </h2>
          <div class="tech-stack">
            <el-row :gutter="24">
              <el-col :xs="24" :sm="12" :md="6">
                <div class="tech-card">
                  <div class="tech-icon frontend">
                    <Monitor class="w-5 h-5" />
                  </div>
                  <h4>前端技术</h4>
                  <ul>
                    <li>Vue 3</li>
                    <li>Vite</li>
                    <li>Element Plus</li>
                    <li>ECharts</li>
                    <li>Pinia</li>
                  </ul>
                </div>
              </el-col>
              <el-col :xs="24" :sm="12" :md="6">
                <div class="tech-card">
                  <div class="tech-icon backend">
                    <Monitor class="w-5 h-5" />
                  </div>
                  <h4>后端技术</h4>
                  <ul>
                    <li>Python</li>
                    <li>FastAPI</li>
                    <li>SQLAlchemy</li>
                    <li>SQLite</li>
                    <li>Uvicorn</li>
                  </ul>
                </div>
              </el-col>
              <el-col :xs="24" :sm="12" :md="6">
                <div class="tech-card">
                  <div class="tech-icon ai">
                    <Cpu class="w-6 h-6" />
                  </div>
                  <h4>AI技术</h4>
                  <ul>
                    <li>智谱清言API</li>
                    <li>GLM-4模型</li>
                    <li>自然语言处理</li>
                    <li>文档解析</li>
                    <li>智能分析</li>
                  </ul>
                </div>
              </el-col>
              <el-col :xs="24" :sm="12" :md="6">
                <div class="tech-card">
                  <div class="tech-icon deploy">
                    <Package class="w-5 h-5" />
                  </div>
                  <h4>部署运维</h4>
                  <ul>
                    <li>Docker</li>
                    <li>Docker Compose</li>
                    <li>Nginx</li>
                    <li>Linux</li>
                    <li>CI/CD</li>
                  </ul>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 使用流程 -->
        <div class="workflow-section">
          <h2 class="section-title">
            <BookOpen class="w-6 h-6" />
            使用流程
          </h2>
          <div class="workflow-steps">
            <el-steps direction="horizontal" :active="4" align-center>
              <el-step title="上传简历" description="支持PDF、DOCX格式">
                <template #icon>
                  <Upload class="w-5 h-5" />
                </template>
              </el-step>
              <el-step title="输入职位描述" description="详细描述岗位要求">
                <template #icon>
                  <Edit class="w-5 h-5" />
                </template>
              </el-step>
              <el-step title="AI智能分析" description="自动匹配和评分">
                <template #icon>
                  <BarChart3 class="w-5 h-5" />
                </template>
              </el-step>
              <el-step title="获取分析报告" description="查看详细结果">
                <template #icon>
                  <FileText class="w-5 h-5" />
                </template>
              </el-step>
            </el-steps>
          </div>
        </div>

        <!-- 产品优势 -->
        <div class="advantages-section">
          <h2 class="section-title">
            <Trophy class="w-6 h-6" />
            产品优势
          </h2>
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="8">
              <div class="advantage-item">
                <div class="advantage-icon">
                  <Zap class="w-5 h-5" />
                </div>
                <h4>高效便捷</h4>
                <p>秒级完成简历分析，大幅提升HR工作效率，减少人工筛选时间</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <div class="advantage-item">
                <div class="advantage-icon">
                  <CheckCircle class="w-5 h-5" />
                </div>
                <h4>精准匹配</h4>
                <p>基于AI深度学习，提供更准确的匹配度评分和候选人评估</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="8">
              <div class="advantage-item">
                <div class="advantage-icon">
                  <TrendCharts class="w-5 h-5" />
                </div>
                <h4>数据驱动</h4>
                <p>提供详细的分析报告和可视化图表，支持数据驱动的招聘决策</p>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 联系我们 -->
        <div class="contact-section">
          <div class="contact-card">
            <h2 class="section-title">
              <MessageCircle class="w-5 h-5" />
              联系我们
            </h2>
            <p class="contact-description">
              如果您对我们的产品有任何疑问或建议，欢迎随时联系我们
            </p>
            <div class="contact-info">
              <div class="contact-item">
                <MessageCircle class="w-5 h-5" />
                <span>技术支持：support@example.com</span>
              </div>
              <div class="contact-item">
                <Phone class="w-5 h-5" />
                <span>客服热线：400-123-4567</span>
              </div>
              <div class="contact-item">
                <MapPin class="w-5 h-5" />
                <span>公司地址：北京市朝阳区xxx大厦</span>
              </div>
            </div>
            <div class="contact-actions">
              <el-button type="primary" size="large">
                <MessageCircle class="w-5 h-5" />
                在线咨询
              </el-button>
              <el-button size="large">
                <Download class="w-5 h-5" />
                下载文档
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-main>

    <!-- 页脚 -->
    <el-footer class="footer">
      <div class="footer-content">
        <div class="footer-info">
          <p>&copy; 2024 AI招聘筛选助手. 基于智谱清言AI技术构建.</p>
          <p>让招聘更智能，让人才更精准</p>
        </div>
        <div class="footer-links">
          <a href="#" class="footer-link">隐私政策</a>
          <a href="#" class="footer-link">服务条款</a>
          <a href="#" class="footer-link">帮助中心</a>
        </div>
      </div>
    </el-footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { 
  BarChart3, Monitor, Cpu, Trophy, Star, MessageSquare, User, TrendingUp, Edit, Eye,
  ArrowLeft, FileText, Clock, Settings, Package, BookOpen, Upload, Zap, CheckCircle, 
  TrendingUp as TrendCharts, MessageCircle, Phone, MapPin, Download
} from 'lucide-vue-next'

const router = useRouter()

const goBack = () => {
  router.push('/')
}
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  height: 60px;
  line-height: 60px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.logo .el-icon {
  margin-right: 8px;
  font-size: 24px;
}

.main-content {
  padding: 40px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero-section {
  text-align: center;
  margin-bottom: 60px;
}

.hero-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 60px 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.hero-title {
  font-size: 3em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-title .el-icon {
  margin-right: 16px;
  color: #409eff;
}

.hero-subtitle {
  font-size: 1.2em;
  color: #666;
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5em;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  color: #666;
  font-size: 1em;
}

.section-title {
  font-size: 2em;
  font-weight: bold;
  color: #2c3e50;
  text-align: center;
  margin-bottom: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.section-title .el-icon {
  margin-right: 12px;
  color: #409eff;
}

.features-section,
.tech-section,
.workflow-section,
.advantages-section {
  margin-bottom: 60px;
}

.feature-card,
.tech-card,
.advantage-item {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  margin-bottom: 24px;
}

.feature-card:hover,
.tech-card:hover,
.advantage-item:hover {
  transform: translateY(-5px);
}

.feature-icon,
.advantage-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  font-size: 32px;
}

.tech-icon {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: white;
  font-size: 24px;
}

.tech-icon.frontend {
  background: linear-gradient(135deg, #4fc08d, #44a08d);
}

.tech-icon.backend {
  background: linear-gradient(135deg, #ff6b6b, #ee5a52);
}

.tech-icon.ai {
  background: linear-gradient(135deg, #a8edea, #fed6e3);
  color: #333;
}

.tech-icon.deploy {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.feature-card h3,
.tech-card h4,
.advantage-item h4 {
  font-size: 1.3em;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
}

.feature-card p,
.advantage-item p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.tech-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-card li {
  padding: 4px 0;
  color: #666;
}

.workflow-steps {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.contact-section {
  margin-bottom: 60px;
}

.contact-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 50px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.contact-description {
  font-size: 1.1em;
  color: #666;
  margin-bottom: 30px;
}

.contact-info {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
}

.contact-item .el-icon {
  color: #409eff;
}

.contact-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding: 40px 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.footer-info p {
  color: #666;
  margin: 4px 0;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-link {
  color: #666;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-content {
    padding: 40px 20px;
  }
  
  .hero-title {
    font-size: 2em;
  }
  
  .hero-stats {
    gap: 20px;
  }
  
  .stat-number {
    font-size: 2em;
  }
  
  .feature-card,
  .tech-card,
  .advantage-item {
    padding: 20px;
  }
  
  .workflow-steps {
    padding: 20px;
  }
  
  .contact-card {
    padding: 30px 20px;
  }
  
  .contact-info {
    flex-direction: column;
    gap: 16px;
  }
  
  .contact-actions {
    flex-direction: column;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 16px;
  }
  
  .logo {
    margin-bottom: 16px;
  }
  
  .nav-menu {
    margin-bottom: 16px;
  }
  
  .container {
    padding: 0 16px;
  }
}
</style>
