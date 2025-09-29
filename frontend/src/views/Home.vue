<template>
  <div class="home">
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
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="main-content">
      <div class="container">
        <!-- 欢迎区域 -->
        <div class="welcome-section">
          <div class="welcome-content">
            <h1 class="welcome-title">
              RecruitAI Pro
            </h1>
            <p class="welcome-subtitle">
              基于智谱清言AI技术，快速分析简历匹配度，生成个性化面试问题和分析报告
            </p>
            <div class="feature-tags">
              <el-tag type="primary" size="large">智能匹配</el-tag>
              <el-tag type="success" size="large">面试问题生成</el-tag>
              <el-tag type="warning" size="large">候选人画像</el-tag>
              <el-tag type="info" size="large">可视化报告</el-tag>
            </div>
          </div>
        </div>

        <!-- 功能区域 -->
        <div class="function-section">
          <el-row :gutter="24">
            <!-- 左侧：文件上传和职位描述输入 -->
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
              <div class="card">
                <div class="card-header">
                  <h2 class="card-title">
                    <Upload class="w-5 h-5" />
                    开始分析
                  </h2>
                  <p class="card-subtitle">上传简历文件并输入职位描述，开始智能分析</p>
                </div>

                <!-- 文件上传组件 -->
                <FileUpload 
                  @upload-success="handleUploadSuccess"
                  @upload-error="handleUploadError"
                />

                <!-- 职位描述输入 -->
                <div class="job-description-section">
                  <h3>
                    <FileText class="w-5 h-5" />
                    职位描述
                  </h3>
                  <el-input
                    v-model="jobDescription"
                    type="textarea"
                    :rows="8"
                    placeholder="请输入职位描述，包括：&#10;1. 岗位职责&#10;2. 任职要求&#10;3. 技能要求&#10;4. 工作经验要求&#10;5. 教育背景要求等..."
                    maxlength="5000"
                    show-word-limit
                  />
                </div>

                <!-- 开始分析按钮 -->
                <div class="action-section">
                  <el-button
                    type="primary"
                    size="large"
                    :loading="appStore.loading"
                    :disabled="!canStartAnalysis"
                    @click="startAnalysis"
                    class="start-btn"
                  >
                    <BarChart3 class="w-5 h-5" />
                    {{ appStore.loading ? '正在分析中...' : '开始分析' }}
                  </el-button>
                </div>

                <!-- 进度显示 -->
                <div v-if="appStore.loading" class="progress-section">
                  <el-progress 
                    :percentage="appStore.analysisProgress" 
                    :status="appStore.analysisProgress === 100 ? 'success' : ''"
                    :stroke-width="8"
                  />
                  <p class="progress-text">AI正在分析简历和职位匹配度...</p>
                </div>
              </div>
            </el-col>

            <!-- 右侧：功能介绍 -->
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
              <div class="card">
                <div class="card-header">
                  <h2 class="card-title">
                    <Info class="w-5 h-5" />
                    功能特色
                  </h2>
                </div>

                <div class="features-list">
                  <div class="feature-item">
                    <div class="feature-icon">
                      <Star class="w-5 h-5" />
                    </div>
                    <div class="feature-content">
                      <h4>智能匹配评分</h4>
                      <p>基于AI技术分析简历与职位描述的匹配度，提供0-100分的量化评分</p>
                    </div>
                  </div>

                  <div class="feature-item">
                    <div class="feature-icon">
                      <MessageSquare class="w-5 h-5" />
                    </div>
                    <div class="feature-content">
                      <h4>个性化面试问题</h4>
                      <p>根据候选人背景和职位要求，自动生成10个针对性面试问题</p>
                    </div>
                  </div>

                  <div class="feature-item">
                    <div class="feature-icon">
                      <div class="feature-icon">
                        <User class="w-5 h-5" />
                      </div>
                    </div>
                    <div class="feature-content">
                      <h4>候选人画像</h4>
                      <p>深度分析候选人技能、经验、教育背景，生成完整能力画像</p>
                    </div>
                  </div>

                  <div class="feature-item">
                    <div class="feature-icon">
                      <BarChart3 class="w-5 h-5" />
                    </div>
                    <div class="feature-content">
                      <h4>可视化报告</h4>
                      <p>生成包含图表和详细分析的完整报告，支持导出和分享</p>
                    </div>
                  </div>
                </div>

                <!-- 用户反馈区域 -->
                <div class="feedback-section">
                  <div class="feedback-header">
                    <h3 class="feedback-title">
                      <MessageSquare class="w-5 h-5" />
                      用户反馈
                    </h3>
                    <p class="feedback-desc">您的建议将帮助我们做得更好</p>
                  </div>
                  
                  <div class="feedback-content">
                    <div class="feedback-item">
                      <div class="feedback-icon">
                        <Edit3 class="w-5 h-5" />
                      </div>
                      <div class="feedback-info">
                        <h4>问卷调查</h4>
                        <p>分享您的使用体验，帮助我们持续改进产品功能</p>
                      </div>
                      <div class="feedback-action">
                        <el-button 
                          type="primary" 
                          :icon="ExternalLink" 
                          @click="openFeedbackSurvey"
                          class="feedback-btn"
                        >
                          参与调研
                        </el-button>
                      </div>
                    </div>

                    <div class="feedback-item">
                      <div class="feedback-icon">
                        <MessageCircle class="w-5 h-5" />
                      </div>
                      <div class="feedback-info">
                        <h4>建议与贡献</h4>
                        <p>期待更多功能？或愿意匿名分享数据帮助我们训练更精准的AI模型</p>
                      </div>
                      <div class="feedback-action">
                        <el-button 
                          type="success" 
                          :icon="MessageCircle" 
                          @click="openFeedbackAndData"
                          class="feedback-btn"
                        >
                          提交建议
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 使用步骤 -->
        <div class="steps-section">
          <div class="card">
            <div class="card-header">
              <h2 class="card-title">
                <BookOpen class="w-5 h-5" />
                使用步骤
              </h2>
            </div>
            
            <el-steps :active="currentStep" align-center>
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
              <el-step title="AI分析" description="智能匹配和评分">
                <template #icon>
                  <BarChart3 class="w-5 h-5" />
                </template>
              </el-step>
              <el-step title="查看报告" description="获取分析结果">
                <template #icon>
                  <Eye class="w-5 h-5" />
                </template>
              </el-step>
            </el-steps>
          </div>
        </div>
      </div>
    </el-main>

    <!-- 页脚 -->
    <el-footer class="footer">
      <div class="footer-content">
        <p>&copy; 2025 AI招聘筛选助手. 基于智谱清言AI技术构建.</p>
      </div>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAppStore } from '@/store'
import { apiService } from '@/api'
import FileUpload from '@/components/FileUpload.vue'
import { 
  ExternalLink, MessageCircle, BarChart3, Cpu, Upload, FileText, 
  Info, Star, MessageSquare, User, Edit3, BookOpen, Edit, Eye
} from 'lucide-vue-next'

const router = useRouter()
const appStore = useAppStore()

// 响应式数据
const jobDescription = ref('')
const currentStep = ref(0)
const uploadedFileId = ref(null)

// 计算属性
const canStartAnalysis = computed(() => {
  return uploadedFileId.value && jobDescription.value.trim().length > 0
})

// 监听器
watch(uploadedFileId, (newVal) => {
  if (newVal) {
    currentStep.value = 1
  }
})

watch(jobDescription, (newVal) => {
  if (newVal.trim().length > 0 && uploadedFileId.value) {
    currentStep.value = 2
  }
})

// 方法
const handleUploadSuccess = (result) => {
  uploadedFileId.value = result.file_id
  currentStep.value = 1
  ElMessage.success(`文件上传成功: ${result.file_name}`)
}

const handleUploadError = (error) => {
  ElMessage.error(`文件上传失败: ${error}`)
}

const startAnalysis = async () => {
  if (!canStartAnalysis.value) {
    ElMessage.warning('请先上传简历文件并输入职位描述')
    return
  }

  try {
    appStore.setLoading(true)
    appStore.setAnalysisProgress(0)
    currentStep.value = 3

    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (appStore.analysisProgress < 90) {
        appStore.setAnalysisProgress(appStore.analysisProgress + 10)
      }
    }, 1000)

    const response = await apiService.processAnalysis({
      file_id: uploadedFileId.value,
      job_description: jobDescription.value
    })

    clearInterval(progressInterval)
    appStore.setAnalysisProgress(100)

    // 保存分析结果
    appStore.setCurrentAnalysis(response)
    appStore.setCurrentCandidate({
      id: uploadedFileId.value,
      name: response.candidate_profile.name
    })

    ElMessage.success('分析完成！正在跳转到结果页面...')
    
    // 跳转到分析结果页面
    setTimeout(() => {
      router.push(`/analysis/${uploadedFileId.value}`)
    }, 1500)

  } catch (error) {
    console.error('分析失败:', error)
    ElMessage.error('分析失败，请重试')
  } finally {
    appStore.setLoading(false)
    appStore.setAnalysisProgress(0)
  }
}

// 反馈相关方法
const openFeedbackSurvey = () => {
  // 这里可以替换为实际的问卷调查链接
  const surveyUrl = 'https://docs.google.com/forms/d/e/1FAIpQLSfxKzQp7roJpC8827vakv9PiAweonADNBGxmObe_u0ly36Ijg/viewform?usp=header'
  window.open(surveyUrl, '_blank')
  ElMessage.success('感谢您的参与！')
}

const openFeedbackAndData = async () => {
  await ElMessageBox.alert('邮箱: wby106006@gmail.com', '联系邮箱', {
    confirmButtonText: '好的'
  })
  ElMessage.success('感谢您的建议！')
}
</script>

<style scoped>
.home {
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

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 60px 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.welcome-title {
  font-size: 3em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-title .el-icon {
  margin-right: 16px;
  color: #409eff;
}

.welcome-subtitle {
  font-size: 1.2em;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.6;
}

.feature-tags {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.function-section {
  margin-bottom: 40px;
}

.card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 24px;
}

.card-header {
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 20px;
  margin-bottom: 24px;
}

.card-title {
  font-size: 1.5em;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.card-title .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.card-subtitle {
  color: #666;
  margin: 0;
}

.job-description-section {
  margin: 24px 0;
}

.job-description-section h3 {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  color: #2c3e50;
}

.job-description-section .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.action-section {
  text-align: center;
  margin-top: 30px;
  margin-bottom: 33px;
}

.start-btn {
  padding: 16px 40px;
  font-size: 16px;
  border-radius: 25px;
}

.progress-section {
  margin-top: 24px;
  text-align: center;
}

.progress-text {
  margin-top: 12px;
  color: #666;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.feature-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  flex-shrink: 0;
}

.feature-content h4 {
  font-size: 1.1em;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.feature-content p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

/* 反馈区域样式 */
.feedback-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e8eaec;
}

.feedback-header {
  margin-bottom: 20px;
}

.feedback-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2em;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.feedback-title .el-icon {
  color: #409eff;
}

.feedback-desc {
  color: #666;
  font-size: 0.9em;
  margin: 0;
}

.feedback-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feedback-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e8eaec;
  transition: all 0.3s ease;
}

.feedback-item:hover {
  background: #f0f7ff;
  border-color: #c6e2ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}

.feedback-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  flex-shrink: 0;
}

.feedback-info {
  flex: 1;
}

.feedback-info h4 {
  font-size: 1em;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 6px 0;
}

.feedback-info p {
  color: #666;
  line-height: 1.5;
  margin: 0;
  font-size: 0.9em;
}

.feedback-action {
  flex-shrink: 0;
}

.feedback-btn {
  padding: 8px 16px;
  font-size: 0.9em;
  border-radius: 8px;
}

.steps-section {
  margin-bottom: 40px;
}

.footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  height: 60px;
  line-height: 60px;
  text-align: center;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content p {
  color: #666;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-content {
    padding: 40px 20px;
  }
  
  .welcome-title {
    font-size: 2em;
  }
  
  .card {
    padding: 20px;
  }
  
  .feature-tags {
    gap: 8px;
  }
  
  .header-content {
    padding: 0 16px;
  }
  
  .container {
    padding: 0 16px;
  }
}
</style>
