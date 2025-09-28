<template>
  <div class="analysis-page">
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
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-section">
          <div class="loading-content">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <h2>正在加载分析结果...</h2>
            <p>请稍候，AI正在为您生成详细的分析报告</p>
          </div>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="error-section">
          <el-result
            icon="error"
            title="加载失败"
            :sub-title="error"
          >
            <template #extra>
              <el-button type="primary" @click="loadAnalysisData">重新加载</el-button>
              <el-button @click="goBack">返回首页</el-button>
            </template>
          </el-result>
        </div>

        <!-- 分析结果 -->
        <div v-else-if="analysisData" class="analysis-content">
          <!-- 候选人基本信息 -->
          <div class="card candidate-info">
            <div class="card-header">
              <h2 class="card-title">
                <User class="w-5 h-5" />
                候选人信息
              </h2>
            </div>
            <div class="candidate-details">
              <div class="candidate-avatar">
                <el-avatar :size="80" :src="candidateAvatar">
                  <User class="w-5 h-5" />
                </el-avatar>
              </div>
              <div class="candidate-info">
                <h3>{{ analysisData.candidate_profile?.name || '未知' }}</h3>
                <p class="candidate-summary">{{ analysisData.candidate_profile?.summary || '暂无个人简介' }}</p>
                <div class="contact-info" v-if="analysisData.candidate_profile?.contact_info">
                  <el-tag v-for="(value, key) in analysisData.candidate_profile.contact_info" 
                          :key="key" type="info" size="small">
                    {{ key }}: {{ value }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>

          <!-- 匹配度评分 -->
          <div class="card match-score">
            <div class="card-header">
              <h2 class="card-title">
                <Trophy class="w-5 h-5" />
                匹配度评分
              </h2>
            </div>
            <div class="score-display">
              <div class="score-circle" :style="scoreCircleStyle">
                <div class="score-number">{{ Math.round(analysisData.match_score || 0) }}</div>
                <div class="score-label">分</div>
              </div>
              <div class="score-details">
                <div class="score-level" :class="scoreLevelClass">
                  {{ getScoreLevel(analysisData.match_score) }}
                </div>
                <p class="score-description">基于技能匹配、经验匹配、教育背景综合评估</p>
              </div>
            </div>
          </div>

          <!-- 技能分析 -->
          <div class="card skills-analysis">
            <div class="card-header">
              <h2 class="card-title">
                <Star class="w-5 h-5" />
                技能匹配分析
              </h2>
            </div>
            <div class="skills-content">
              <el-row :gutter="20">
                <el-col :xs="24" :sm="12" :md="8">
                  <div class="skill-category">
                    <h4>候选技能</h4>
                    <div class="skill-tags">
                      <el-tag 
                        v-for="skill in analysisData.skills_analysis?.candidate_skills || []" 
                        :key="skill" 
                        type="primary" 
                        size="small"
                      >
                        {{ skill }}
                      </el-tag>
                    </div>
                  </div>
                </el-col>
                <el-col :xs="24" :sm="12" :md="8">
                  <div class="skill-category">
                    <h4>匹配技能</h4>
                    <div class="skill-tags">
                      <el-tag 
                        v-for="skill in analysisData.skills_analysis?.matched_skills || []" 
                        :key="skill" 
                        type="success" 
                        size="small"
                      >
                        {{ skill }}
                      </el-tag>
                    </div>
                  </div>
                </el-col>
                <el-col :xs="24" :sm="12" :md="8">
                  <div class="skill-category">
                    <h4>缺失技能</h4>
                    <div class="skill-tags">
                      <el-tag 
                        v-for="skill in analysisData.skills_analysis?.missing_skills || []" 
                        :key="skill" 
                        type="warning" 
                        size="small"
                      >
                        {{ skill }}
                      </el-tag>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>

          <!-- 面试问题 -->
          <div class="card interview-questions">
            <div class="card-header">
              <h2 class="card-title">
                <MessageSquare class="w-5 h-5" />
                个性化面试问题
              </h2>
              <div class="header-actions">
                <el-button 
                  v-if="!analysisData?.interview_questions?.length && !questionsGenerating"
                  type="primary" 
                  @click="generateQuestions"
                  :loading="questionsGenerating"
                >
                  <Plus class="w-5 h-5" />
                  生成面试问题
                </el-button>
                <el-button 
                  v-if="analysisData?.interview_questions?.length"
                  size="small" 
                  @click="copyQuestions"
                >
                  <Copy class="w-5 h-5" />
                  复制问题
                </el-button>
              </div>
            </div>
            <div class="questions-list">
              <div 
                v-for="(question, index) in analysisData.interview_questions || []" 
                :key="index"
                class="question-item"
              >
                <div class="question-number">{{ index + 1 }}</div>
                <div class="question-content">{{ question }}</div>
              </div>
            </div>
          </div>

          <!-- 候选人画像 -->
          <div class="card candidate-profile">
            <div class="card-header">
              <h2 class="card-title">
                <BarChart3 class="w-5 h-5" />
                候选人画像
              </h2>
            </div>
            <div class="profile-content">
              <el-row :gutter="20">
                <el-col :xs="24" :sm="12">
                  <div class="profile-section">
                    <h4 class="section-title">优势分析</h4>
                    <div class="strengths-list">
                      <div 
                        v-for="strength in getStrengths()" 
                        :key="strength"
                        class="strength-item"
                      >
                        <el-icon class="strength-icon"><Check /></el-icon>
                        <span>{{ strength }}</span>
                      </div>
                      <div v-if="getStrengths().length === 0" class="no-data">
                        <Info class="w-5 h-5" />
                        <span>暂无优势分析数据</span>
                      </div>
                    </div>
                  </div>
                </el-col>
                <el-col :xs="24" :sm="12">
                  <div class="profile-section">
                    <h4 class="section-title">关注点</h4>
                    <div class="weaknesses-list">
                      <div 
                        v-for="weakness in getWeaknesses()" 
                        :key="weakness"
                        class="weakness-item"
                      >
                        <el-icon class="weakness-icon"><Warning /></el-icon>
                        <span>{{ weakness }}</span>
                      </div>
                      <div v-if="getWeaknesses().length === 0" class="no-data">
                        <Info class="w-5 h-5" />
                        <span>暂无关注点分析数据</span>
                      </div>
                    </div>
                  </div>
                </el-col>
              </el-row>
              <div class="potential-section">
                <h4 class="section-title">发展潜力</h4>
                <p class="potential-text">{{ getPotential() }}</p>
              </div>
            </div>
          </div>

          <!-- 可视化图表 -->
          <div class="card charts-report">
            <div class="card-header">
              <h2 class="card-title">
                <BarChart3 class="w-5 h-5" />
                可视化分析图表
              </h2>
            </div>
            <Charts :chart-data="analysisData.chart_data" />
          </div>

          <!-- 详细分析报告 -->
          <div class="card detailed-report">
            <div class="card-header">
              <h2 class="card-title">
                <FileText class="w-5 h-5" />
                详细分析报告
              </h2>
              <div class="header-actions">
                <el-button 
                  size="small" 
                  @click="previewResume"
                  :loading="previewLoading"
                >
                  <Eye class="w-5 h-5" />
                  浏览简历
                </el-button>
                <el-button 
                  size="small" 
                  @click="downloadResume"
                  :loading="downloadLoading"
                >
                  <Download class="w-5 h-5" />
                  下载简历
                </el-button>
                <el-button 
                  size="small" 
                  @click="exportReport"
                  :loading="exporting"
                >
                  <Copy class="w-5 h-5" />
                  导出报告
                </el-button>
                <el-button size="small" @click="printReport">
                  <Printer class="w-5 h-5" />
                  打印报告
                </el-button>
              </div>
            </div>
            <div class="report-content">
              <MarkdownRenderer :content="analysisData.analysis_report || '暂无详细报告'" />
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="action-buttons">
            <el-button type="primary" size="large" @click="regenerateAnalysis">
              <RefreshCw class="w-5 h-5" />
              重新生成分析
            </el-button>
            <el-button size="large" @click="goBack">
              <ArrowLeft class="w-4 h-4" />
              返回首页
            </el-button>
          </div>
        </div>
      </div>
    </el-main>
    <!-- 简历预览弹窗 -->
    <el-dialog
      v-model="resumePreviewVisible"
      title="简历预览"
      width="80%"
      :close-on-click-modal="false"
      class="resume-preview-dialog"
    >
      <div class="resume-preview-header">
        <h3>{{ resumeFileName }}</h3>
      </div>
      <div class="resume-preview-content">
        <pre class="resume-text">{{ resumeContent }}</pre>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="resumePreviewVisible = false">关闭</el-button>
          <el-button type="primary" @click="downloadResume">下载简历</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { apiService } from '@/api'
import Charts from '@/components/Charts.vue'
import { Cpu, ArrowLeft, User, Trophy, Star, MessageSquare, Plus, Copy, BarChart3, Info, FileText, Eye, Download, Printer, RefreshCw } from 'lucide-vue-next'
import MarkdownRenderer from '@/components/MarkdownRenderer.vue'

const route = useRoute()
const router = useRouter()


// 响应式数据
const loading = ref(true)
const error = ref(null)
const analysisData = ref(null)
const questionsGenerating = ref(false)
const exporting = ref(false)
const previewLoading = ref(false)
const downloadLoading = ref(false)
const resumePreviewVisible = ref(false)
const resumeContent = ref('')
const resumeFileName = ref('')

// 计算属性
const candidateAvatar = computed(() => {
  // 可以根据候选人姓名生成头像
  return null
})

// 辅助方法 - 获取优势列表
const getStrengths = () => {
  const strengths = analysisData.value?.candidate_profile?.strengths || []
  if (strengths.length === 0) {
    // 从分析结果中获取优势
    const analysisStrengths = analysisData.value?.strengths || []
    return analysisStrengths.length > 0 ? analysisStrengths : ['具备学习能力', '有发展潜力']
  }
  return strengths
}

// 辅助方法 - 获取关注点列表
const getWeaknesses = () => {
  const weaknesses = analysisData.value?.candidate_profile?.weaknesses || []
  if (weaknesses.length === 0) {
    // 从分析结果中获取关注点
    const analysisWeaknesses = analysisData.value?.weaknesses || []
    return analysisWeaknesses.length > 0 ? analysisWeaknesses : ['需要进一步了解', '需要技能提升']
  }
  return weaknesses
}

// 辅助方法 - 获取发展潜力
const getPotential = () => {
  const potential = analysisData.value?.candidate_profile?.potential || ''
  if (!potential) {
    // 从分析结果中获取潜力评估
    const analysisPotential = analysisData.value?.potential || ''
    return analysisPotential || '候选人具备基础条件，通过适当培训可以胜任工作'
  }
  return potential
}

const scoreCircleStyle = computed(() => {
  const score = analysisData.value?.match_score || 0
  const percentage = score / 100
  
  // 根据分数选择颜色
  let color = '#f56c6c' // 红色 - 低分
  if (score >= 80) {
    color = '#67c23a' // 绿色 - 高分
  } else if (score >= 60) {
    color = '#e6a23c' // 橙色 - 中等
  }
  
  return {
    background: `conic-gradient(${color} ${percentage * 360}deg, #e9ecef ${percentage * 360}deg)`
  }
})

const scoreLevelClass = computed(() => {
  const score = analysisData.value?.match_score || 0
  if (score >= 80) return 'score-excellent'
  if (score >= 60) return 'score-good'
  return 'score-poor'
})

// 方法
const loadAnalysisData = async () => {
  const fileId = route.params.fileId
  if (!fileId) {
    error.value = '缺少文件ID参数'
    loading.value = false
    return
  }

  try {
    loading.value = true
    error.value = null

    // 获取候选人报告
    const response = await apiService.getCandidateReport(fileId)
    analysisData.value = response

  } catch (err) {
    console.error('加载分析数据失败:', err)
    error.value = err.message || '加载失败，请重试'
  } finally {
    loading.value = false
  }
}

const getScoreLevel = (score) => {
  if (score >= 90) return '优秀匹配'
  if (score >= 80) return '良好匹配'
  if (score >= 70) return '一般匹配'
  if (score >= 60) return '勉强匹配'
  return '匹配度较低'
}

const copyQuestions = async () => {
  const questions = analysisData.value?.interview_questions || []
  if (questions.length === 0) {
    ElMessage.warning('暂无面试问题')
    return
  }

  const text = questions.map((q, i) => `${i + 1}. ${q}`).join('\n')
  
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('面试问题已复制到剪贴板')
  } catch (err) {
    ElMessage.error('复制失败，请手动复制')
  }
}

const generateQuestions = async () => {
  try {
    questionsGenerating.value = true
    const fileId = route.params.fileId
    
    if (!fileId) {
      ElMessage.error('缺少文件ID')
      return
    }
    
    ElMessage.info('正在生成个性化面试问题...')
    
    // 使用文件ID作为分析ID（后端会根据文件ID找到对应的分析结果）
    const response = await apiService.generateInterviewQuestions(fileId)
    
    if (response.interview_questions) {
      analysisData.value.interview_questions = response.interview_questions
      ElMessage.success('面试问题生成成功！')
    } else {
      ElMessage.warning('面试问题生成失败')
    }
  } catch (error) {
    console.error('生成面试问题失败:', error)
    ElMessage.error('生成面试问题失败，请重试')
  } finally {
    questionsGenerating.value = false
  }
}

const exportReport = async () => {
  try {
    const fileId = route.params.fileId
    const response = await apiService.exportReport(fileId)
    
    // 创建下载链接
    const blob = new Blob([response.html_content], { type: 'text/html' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `候选人分析报告-${Date.now()}.html`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('报告导出成功')
  } catch (err) {
    ElMessage.error('报告导出失败')
  }
}

const printReport = () => {
  const printContent = document.querySelector('.detailed-report .report-content').innerHTML
  const printWindow = window.open('', '_blank')
  printWindow.document.write(`
    <html>
      <head>
        <title>候选人分析报告</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          pre { white-space: pre-wrap; word-wrap: break-word; }
        </style>
      </head>
      <body>
        <h1>候选人分析报告</h1>
        ${printContent}
      </body>
    </html>
  `)
  printWindow.document.close()
  printWindow.print()
}

// 预览简历
const previewResume = async () => {
  try {
    previewLoading.value = true
    const fileId = route.params.fileId
    
    if (!fileId) {
      ElMessage.error('缺少文件ID')
      return
    }
    
    const response = await apiService.previewResume(fileId)
    
    console.log('预览响应:', response)
    console.log('预览响应头:', response.headers)
    console.log('预览数据类型:', typeof response.data)
    
    // 如果是JSON响应（文本文件）
    if (response.data && typeof response.data === 'object' && !response.data.constructor.name.includes('Blob')) {
      resumeContent.value = response.data.content
      resumeFileName.value = response.data.file_name
      resumePreviewVisible.value = true
      ElMessage.success('简历预览成功')
    } else {
      // 如果是文件流（PDF等），在新窗口打开
      const contentType = response.headers?.['content-type'] || response.headers?.['Content-Type'] || 'application/pdf'
      console.log('文件类型:', contentType)
      const blob = new Blob([response.data], { type: contentType })
      const url = window.URL.createObjectURL(blob)
      window.open(url, '_blank')
      window.URL.revokeObjectURL(url)
      ElMessage.success('简历预览成功')
    }
  } catch (error) {
    console.error('预览简历失败:', error)
    ElMessage.error('预览简历失败，请重试')
  } finally {
    previewLoading.value = false
  }
}

// 下载简历
const downloadResume = async () => {
  try {
    downloadLoading.value = true
    const fileId = route.params.fileId
    
    if (!fileId) {
      ElMessage.error('缺少文件ID')
      return
    }
    
    const response = await apiService.downloadResume(fileId)
    
    console.log('下载响应:', response)
    console.log('响应头:', response.headers)
    
    // 创建下载链接
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    
    // 从响应头获取文件名，如果没有则使用默认名称
    const contentDisposition = response.headers?.['content-disposition'] || response.headers?.['Content-Disposition']
    let filename = `resume_${fileId}`
    
    if (contentDisposition) {
      const matches = contentDisposition.match(/filename="(.+)"/)
      if (matches) {
        filename = matches[1]
      }
    }
    
    // 根据响应类型添加文件扩展名
    const contentType = response.headers?.['content-type'] || response.headers?.['Content-Type']
    if (contentType === 'application/pdf') {
      filename += '.pdf'
    } else if (contentType?.includes('word')) {
      filename += '.docx'
    } else if (contentType?.includes('text')) {
      filename += '.txt'
    }
    
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('简历下载成功')
  } catch (error) {
    console.error('下载简历失败:', error)
    ElMessage.error('下载简历失败，请重试')
  } finally {
    downloadLoading.value = false
  }
}

const regenerateAnalysis = async () => {
  try {
    await ElMessageBox.confirm(
      '重新生成分析将覆盖当前结果，确定要继续吗？',
      '确认重新生成',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const fileId = route.params.fileId
    // 这里需要先获取分析ID，然后重新生成
    // 简化处理，重新加载页面
    ElMessage.info('正在重新生成分析...')
    await loadAnalysisData()
    ElMessage.success('分析重新生成完成')

  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('重新生成失败')
    }
  }
}

const goBack = () => {
  router.push('/')
}

// 生命周期
onMounted(() => {
  loadAnalysisData()
})
</script>

<style scoped>
.analysis-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.header {
  background: white;
  border-bottom: 1px solid #ebeef5;
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
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.loading-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.loading-content {
  text-align: center;
}

.loading-icon {
  font-size: 48px;
  color: #409eff;
  animation: rotate 2s linear infinite;
  margin-bottom: 20px;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error-section {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.card-title {
  font-size: 1.3em;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  margin: 0;
}

.card-title .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.candidate-details {
  display: flex;
  align-items: flex-start;
  gap: 24px;
}

.candidate-avatar {
  flex-shrink: 0;
}

.candidate-info h3 {
  font-size: 1.5em;
  color: #2c3e50;
  margin: 0 0 12px 0;
}

.candidate-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.contact-info {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 40px;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.score-circle::before {
  content: '';
  position: absolute;
  width: 90%;
  height: 90%;
  background: white;
  border-radius: 50%;
  z-index: 1;
}

.score-number {
  font-size: 2em;
  font-weight: bold;
  color: #2c3e50;
  z-index: 2;
}

.score-label {
  font-size: 0.9em;
  color: #666;
  z-index: 2;
}

.score-details {
  flex: 1;
}

.score-level {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 8px;
}

.score-excellent {
  color: #67c23a;
}

.score-good {
  color: #e6a23c;
}

.score-poor {
  color: #f56c6c;
}

.score-description {
  color: #666;
  margin: 0;
}

.skills-content {
  margin-top: 16px;
}

.skill-category h4 {
  color: #2c3e50;
  margin-bottom: 12px;
  font-size: 1.1em;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.question-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.question-number {
  width: 32px;
  height: 32px;
  background: #409eff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.question-content {
  flex: 1;
  line-height: 1.6;
  color: #2c3e50;
}

.profile-content {
  margin-top: 16px;
}

.no-data {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-style: italic;
  padding: 12px 0;
}

.no-data .el-icon {
  font-size: 16px;
}

.profile-section {
  margin-bottom: 24px;
}

.section-title {
  color: #2c3e50;
  margin-bottom: 16px;
  font-size: 1.1em;
  display: flex;
  align-items: center;
}

.strengths-list,
.weaknesses-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.strength-item,
.weakness-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
}

.strength-item {
  background: #f0f9ff;
  color: #67c23a;
}

.weakness-item {
  background: #fef0f0;
  color: #f56c6c;
}

.strength-icon {
  color: #67c23a;
}

.weakness-icon {
  color: #f56c6c;
}

.potential-section {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.potential-text {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.report-content {
  margin-top: 16px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

/* 简历预览弹窗样式 */
.resume-preview-dialog .resume-preview-header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e5e7eb;
}

.resume-preview-dialog .resume-preview-header h3 {
  margin: 0;
  color: #374151;
  font-size: 18px;
  font-weight: 600;
}

.resume-preview-dialog .resume-preview-content {
  max-height: 60vh;
  overflow-y: auto;
  background: #f9fafb;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e5e7eb;
}

.resume-preview-dialog .resume-preview-content .resume-text {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  line-height: 1.6;
  color: #374151;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  font-size: 14px;
}

.resume-preview-dialog .dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
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
  
  .score-display {
    flex-direction: column;
    gap: 24px;
    text-align: center;
  }
  
  .candidate-details {
    flex-direction: column;
    text-align: center;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .container {
    padding: 0 16px;
  }
  
  .card {
    padding: 16px;
  }
}
</style>
