<template>
  <div class="file-upload">
    <h3>
      <FileText class="w-5 h-5" />
      简历文件上传
    </h3>
    
    <el-upload
      ref="uploadRef"
      class="upload-demo"
      drag
      :auto-upload="false"
      :on-change="handleFileChange"
      :before-upload="beforeUpload"
      accept=".pdf,.docx,.doc"
      :limit="1"
      :file-list="fileList"
      :on-exceed="handleExceed"
    >
      <div class="upload-area">
        <el-icon class="upload-icon"><UploadFilled /></el-icon>
        <div class="upload-text">
          <p>将文件拖拽到此处，或<em>点击上传</em></p>
          <p class="upload-hint">支持 PDF、DOCX、DOC 格式，文件大小不超过 10MB</p>
        </div>
      </div>
    </el-upload>

    <!-- 文件信息显示 -->
    <div v-if="fileInfo" class="file-info">
      <div class="file-info-content">
        <div class="file-icon">
          <el-icon v-if="fileInfo.type === 'pdf'" color="#f56c6c"><Document /></el-icon>
          <el-icon v-else color="#409eff"><Document /></el-icon>
        </div>
        <div class="file-details">
          <div class="file-name">{{ fileInfo.name }}</div>
          <div class="file-size">{{ formatFileSize(fileInfo.size) }}</div>
        </div>
        <div class="file-actions">
          <el-button 
            type="primary" 
            size="small" 
            :loading="uploading"
            @click="uploadFile"
          >
            <el-icon><Upload /></el-icon>
            {{ uploading ? '上传中...' : '确认上传' }}
          </el-button>
          <el-button 
            size="small" 
            @click="removeFile"
          >
            <el-icon><Delete /></el-icon>
            移除
          </el-button>
        </div>
      </div>
      
      <!-- 上传进度 -->
      <div v-if="uploading" class="upload-progress">
        <el-progress 
          :percentage="uploadProgress" 
          :status="uploadProgress === 100 ? 'success' : ''"
          :stroke-width="6"
        />
      </div>
    </div>

    <!-- 上传状态提示 -->
    <div v-if="uploadStatus" class="upload-status">
      <el-alert
        :title="uploadStatus.message"
        :type="uploadStatus.type"
        :closable="false"
        show-icon
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { apiService } from '@/api'
import { FileText } from 'lucide-vue-next'
import { Upload, Delete } from '@element-plus/icons-vue'

// 定义事件
const emit = defineEmits(['upload-success', 'upload-error'])

// 响应式数据
const uploadRef = ref()
const fileList = ref([])
const fileInfo = ref(null)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref(null)

// 方法
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const beforeUpload = (file) => {
  // 检查文件类型
  const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']
  const isAllowedType = allowedTypes.includes(file.type) || 
    file.name.toLowerCase().endsWith('.pdf') ||
    file.name.toLowerCase().endsWith('.docx') ||
    file.name.toLowerCase().endsWith('.doc')
  
  if (!isAllowedType) {
    ElMessage.error('只支持 PDF、DOCX、DOC 格式的文件！')
    return false
  }

  // 检查文件大小（10MB）
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB！')
    return false
  }

  return false // 阻止自动上传
}

const handleFileChange = (file, fileListParam) => {
  fileList.value = fileListParam
  if (file.status === 'ready') {
    fileInfo.value = {
      name: file.name,
      size: file.size,
      type: file.name.toLowerCase().endsWith('.pdf') ? 'pdf' : 'doc'
    }
    uploadStatus.value = null
  }
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件，请先移除现有文件')
}

const removeFile = () => {
  fileList.value = []
  fileInfo.value = null
  uploadStatus.value = null
  uploadProgress.value = 0
  uploadRef.value?.clearFiles()
}

const uploadFile = async () => {
  if (!fileInfo.value || fileList.value.length === 0) {
    ElMessage.warning('请先选择文件')
    return
  }

  const file = fileList.value[0].raw
  if (!file) {
    ElMessage.error('文件信息异常，请重新选择')
    return
  }

  try {
    uploading.value = true
    uploadProgress.value = 0
    uploadStatus.value = null

    // 模拟上传进度
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += Math.random() * 20
      }
    }, 200)

    const response = await apiService.uploadFile(file)
    
    clearInterval(progressInterval)
    uploadProgress.value = 100

    uploadStatus.value = {
      type: 'success',
      message: `文件上传成功！文件名：${response.file_name}`
    }

    // 延迟一下再触发成功事件，让用户看到进度完成
    setTimeout(() => {
      emit('upload-success', response)
    }, 500)

  } catch (error) {
    console.error('文件上传失败:', error)
    uploadStatus.value = {
      type: 'error',
      message: `文件上传失败：${error.message || '未知错误'}`
    }
    emit('upload-error', error.message || '上传失败')
  } finally {
    uploading.value = false
    setTimeout(() => {
      uploadProgress.value = 0
    }, 1000)
  }
}
</script>

<style scoped>
.file-upload {
  margin-bottom: 24px;
}

.file-upload h3 {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  color: #2c3e50;
  font-size: 1.1em;
}

.file-upload h3 .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.upload-demo {
  width: 100%;
}

.upload-area {
  padding: 40px 20px;
  text-align: center;
  background: #fafafa;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #409eff;
  background: #f0f9ff;
}

.upload-icon {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 16px;
}

.upload-text {
  color: #606266;
}

.upload-text em {
  color: #409eff;
  font-style: normal;
  text-decoration: underline;
  cursor: pointer;
}

.upload-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.file-info {
  margin-top: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.file-info-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-icon {
  font-size: 24px;
}

.file-details {
  flex: 1;
}

.file-name {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.file-size {
  font-size: 12px;
  color: #666;
}

.file-actions {
  display: flex;
  gap: 8px;
}

.upload-progress {
  margin-top: 16px;
}

.upload-status {
  margin-top: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .file-info-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .file-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .upload-area {
    padding: 30px 15px;
  }
  
  .upload-icon {
    font-size: 36px;
  }
}
</style>
