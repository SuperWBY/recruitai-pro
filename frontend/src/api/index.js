import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 创建长时间超时的axios实例用于AI分析
const longTimeoutApi = axios.create({
  baseURL: '/api',
  timeout: 300000, // 5分钟超时
  headers: {
    'Content-Type': 'application/json'
  }
})

// 为长时间请求添加相同的拦截器
longTimeoutApi.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    return config
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 2xx 范围内的状态码都会触发该函数
    return response.data
  },
  error => {
    // 超出 2xx 范围的状态码都会触发该函数
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// API接口定义
export const apiService = {
  // 文件上传
  uploadFile: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取文件信息
  getFileInfo: (fileId) => {
    return api.get(`/file/${fileId}`)
  },

  // 删除文件
  deleteFile: (fileId) => {
    return api.delete(`/file/${fileId}`)
  },

  // 获取文件列表
  getFileList: () => {
    return api.get('/files')
  },

  // 处理分析
  processAnalysis: (data) => {
    return longTimeoutApi.post('/process', data)
  },

  // 获取分析历史
  getAnalysisHistory: (fileId) => {
    return api.get(`/process/${fileId}/history`)
  },

  // 获取分析结果
  getAnalysisResult: (analysisId) => {
    return api.get(`/process/${analysisId}`)
  },

  // 重新生成分析
  regenerateAnalysis: (analysisId) => {
    return api.post(`/process/${analysisId}/regenerate`)
  },

  // 获取候选人报告
  getCandidateReport: (fileId) => {
    return api.get(`/report/${fileId}`)
  },

  // 获取报告摘要
  getReportSummary: (fileId) => {
    return api.get(`/report/${fileId}/summary`)
  },

  // 获取图表数据
  getChartData: (fileId) => {
    return api.get(`/report/${fileId}/charts`)
  },

  // 获取面试问题
  getInterviewQuestions: (fileId) => {
    return api.get(`/report/${fileId}/questions`)
  },

  // 生成面试问题
  generateInterviewQuestions: (analysisId) => {
    return longTimeoutApi.post(`/process/${analysisId}/generate-questions`)
  },

  // 获取所有报告
  getAllReports: () => {
    return api.get('/reports')
  },

  // 导出报告
  exportReport: (fileId) => {
    return api.post(`/report/${fileId}/export`)
  },

  // 下载简历文件
  downloadResume: (fileId) => {
    return api.get(`/file/${fileId}/download`, {
      responseType: 'blob'
    })
  },

  // 预览简历文件
  previewResume: (fileId) => {
    return api.get(`/file/${fileId}/preview`)
  },

  // 获取简历内容
  getResumeContent: (fileId) => {
    return api.get(`/file/${fileId}/content`)
  }
}

export default api
