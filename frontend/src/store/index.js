import { createPinia, defineStore } from 'pinia'

export default createPinia()

// 创建应用状态管理store
export const useAppStore = defineStore('app', {
  state: () => ({
    // 当前分析的候选人信息
    currentCandidate: null,
    
    // 当前分析结果
    currentAnalysis: null,
    
    // 加载状态
    loading: false,
    
    // 错误信息
    error: null,
    
    // 文件上传状态
    uploadProgress: 0,
    
    // 分析进度
    analysisProgress: 0,
    
    // 主题设置
    theme: 'light'
  }),
  
  getters: {
    // 是否有当前候选人
    hasCurrentCandidate: (state) => !!state.currentCandidate,
    
    // 是否有分析结果
    hasAnalysisResult: (state) => !!state.currentAnalysis,
    
    // 匹配度评分
    matchScore: (state) => state.currentAnalysis?.match_score || 0,
    
    // 面试问题
    interviewQuestions: (state) => state.currentAnalysis?.interview_questions || [],
    
    // 候选人画像
    candidateProfile: (state) => state.currentAnalysis?.candidate_profile || null,
    
    // 图表数据
    chartData: (state) => state.currentAnalysis?.chart_data || null
  },
  
  actions: {
    // 设置当前候选人
    setCurrentCandidate(candidate) {
      this.currentCandidate = candidate
    },
    
    // 设置分析结果
    setCurrentAnalysis(analysis) {
      this.currentAnalysis = analysis
    },
    
    // 设置加载状态
    setLoading(loading) {
      this.loading = loading
    },
    
    // 设置错误信息
    setError(error) {
      this.error = error
    },
    
    // 清除错误
    clearError() {
      this.error = null
    },
    
    // 设置上传进度
    setUploadProgress(progress) {
      this.uploadProgress = progress
    },
    
    // 设置分析进度
    setAnalysisProgress(progress) {
      this.analysisProgress = progress
    },
    
    // 切换主题
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light'
    },
    
    // 重置状态
    reset() {
      this.currentCandidate = null
      this.currentAnalysis = null
      this.loading = false
      this.error = null
      this.uploadProgress = 0
      this.analysisProgress = 0
    }
  }
})
