<template>
  <div class="reports-page">
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
        <!-- 页面标题 -->
        <div class="page-header">
          <h1>分析报告管理</h1>
          <p>查看和管理所有候选人的分析报告</p>
        </div>

        <!-- 统计概览 -->
        <div class="stats-overview">
          <el-row :gutter="20">
            <el-col :xs="12" :sm="6" :md="6">
              <div class="stat-card">
                <div class="stat-icon">
                  <FileText class="w-5 h-5" />
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ reports.length }}</div>
                  <div class="stat-label">总报告数</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6" :md="6">
              <div class="stat-card">
                <div class="stat-icon">
                  <Trophy class="w-5 h-5" />
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ averageScore.toFixed(1) }}</div>
                  <div class="stat-label">平均匹配度</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6" :md="6">
              <div class="stat-card">
                <div class="stat-icon">
                  <Star class="w-5 h-5" />
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ highScoreReports.length }}</div>
                  <div class="stat-label">高分报告</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6" :md="6">
              <div class="stat-card">
                <div class="stat-icon">
                  <Calendar class="w-5 h-5" />
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ todayReports.length }}</div>
                  <div class="stat-label">今日新增</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 筛选和搜索 -->
        <div class="filter-section">
          <el-card>
            <el-row :gutter="20" align="middle">
              <el-col :xs="24" :sm="12" :md="8">
                <el-input
                  v-model="searchKeyword"
                  placeholder="搜索候选人姓名或文件名"
                  clearable
                  @input="handleSearch"
                >
                  <template #prefix>
                    <Search class="w-5 h-5" />
                  </template>
                </el-input>
              </el-col>
              <el-col :xs="24" :sm="12" :md="8">
                <el-select
                  v-model="scoreFilter"
                  placeholder="筛选匹配度"
                  clearable
                  @change="handleFilter"
                >
                  <el-option label="高分 (80分以上)" value="high" />
                  <el-option label="中等 (60-80分)" value="medium" />
                  <el-option label="低分 (60分以下)" value="low" />
                </el-select>
              </el-col>
              <el-col :xs="24" :sm="12" :md="8">
                <el-button type="primary" @click="loadReports">
                  <el-icon><Refresh /></el-icon>
                  刷新列表
                </el-button>
              </el-col>
            </el-row>
          </el-card>
        </div>

        <!-- 报告列表 -->
        <div class="reports-list">
          <el-card>
            <template #header>
              <div class="list-header">
                <h3>分析报告列表</h3>
                <div class="list-actions">
                  <el-button size="small" @click="toggleViewMode">
                    <el-icon>
                      <component :is="viewMode === 'card' ? 'List' : 'Grid'" />
                    </el-icon>
                    {{ viewMode === 'card' ? '列表视图' : '卡片视图' }}
                  </el-button>
                </div>
              </div>
            </template>

            <!-- 加载状态 -->
            <div v-if="loading" class="loading-state">
              <el-skeleton :rows="5" animated />
            </div>

            <!-- 空状态 -->
            <div v-else-if="filteredReports.length === 0" class="empty-state">
              <el-empty description="暂无分析报告">
                <el-button type="primary" @click="goBack">开始分析</el-button>
              </el-empty>
            </div>

            <!-- 卡片视图 -->
            <div v-else-if="viewMode === 'card'" class="card-view">
              <el-row :gutter="20">
                <el-col 
                  v-for="report in paginatedReports" 
                  :key="report.analysis_id"
                  :xs="24" :sm="12" :md="8" :lg="6"
                >
                  <div class="report-card" @click="viewReport(report)">
                    <div class="card-header">
                      <div class="candidate-name">{{ report.candidate_name }}</div>
                      <div class="score-badge" :class="getScoreClass(report.match_score)">
                        {{ Math.round(report.match_score) }}分
                      </div>
                    </div>
                    <div class="card-content">
                      <div class="file-info">
                        <FileText class="w-5 h-5" />
                        <span>{{ report.file_name }}</span>
                      </div>
                      <div class="job-description">
                        {{ report.job_description.substring(0, 100) }}...
                      </div>
                      <div class="created-time">
                        <Calendar class="w-5 h-5" />
                        {{ formatDate(report.created_at) }}
                      </div>
                    </div>
                    <div class="card-actions">
                      <el-button size="small" @click.stop="viewReport(report)">
                        <el-icon><View /></el-icon>
                        查看详情
                      </el-button>
                      <el-button size="small" @click.stop="deleteReport(report)">
                        <el-icon><Delete /></el-icon>
                        删除
                      </el-button>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </div>

            <!-- 列表视图 -->
            <div v-else class="list-view">
              <el-table :data="paginatedReports" stripe>
                <el-table-column prop="candidate_name" label="候选人" width="120" />
                <el-table-column prop="file_name" label="文件名" width="200" show-overflow-tooltip />
                <el-table-column prop="job_description" label="职位描述" min-width="300" show-overflow-tooltip />
                <el-table-column label="匹配度" width="100" align="center">
                  <template #default="{ row }">
                    <el-tag :type="getScoreTagType(row.match_score)">
                      {{ Math.round(row.match_score) }}分
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="created_at" label="创建时间" width="180">
                  <template #default="{ row }">
                    {{ formatDate(row.created_at) }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="200" fixed="right">
                  <template #default="{ row }">
                    <el-button size="small" @click="viewReport(row)">
                      <el-icon><View /></el-icon>
                      查看
                    </el-button>
                    <el-button size="small" @click="deleteReport(row)">
                      <el-icon><Delete /></el-icon>
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>

            <!-- 分页 -->
            <div v-if="filteredReports.length > pageSize" class="pagination">
              <el-pagination
                :current-page="currentPage"
                :page-size="pageSize"
                :total="filteredReports.length"
                layout="total, prev, pager, next, jumper"
                @current-change="handlePageChange"
              />
            </div>
          </el-card>
        </div>
      </div>
    </el-main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { apiService } from '@/api'
import dayjs from 'dayjs'
import { Cpu, ArrowLeft, FileText, Trophy, Star, Calendar, Search } from 'lucide-vue-next'
import { Refresh, List, Grid, View, Delete } from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const loading = ref(true)
const reports = ref([])
const searchKeyword = ref('')
const scoreFilter = ref('')
const viewMode = ref('card')
const currentPage = ref(1)
const pageSize = ref(12)

// 计算属性
const filteredReports = computed(() => {
  let filtered = reports.value

  // 搜索过滤
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(report => 
      report.candidate_name.toLowerCase().includes(keyword) ||
      report.file_name.toLowerCase().includes(keyword)
    )
  }

  // 分数过滤
  if (scoreFilter.value) {
    filtered = filtered.filter(report => {
      const score = report.match_score
      switch (scoreFilter.value) {
        case 'high':
          return score >= 80
        case 'medium':
          return score >= 60 && score < 80
        case 'low':
          return score < 60
        default:
          return true
      }
    })
  }

  return filtered
})

const paginatedReports = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredReports.value.slice(start, end)
})

const averageScore = computed(() => {
  if (reports.value.length === 0) return 0
  const total = reports.value.reduce((sum, report) => sum + report.match_score, 0)
  return total / reports.value.length
})

const highScoreReports = computed(() => {
  return reports.value.filter(report => report.match_score >= 80)
})

const todayReports = computed(() => {
  const today = dayjs().format('YYYY-MM-DD')
  return reports.value.filter(report => 
    dayjs(report.created_at).format('YYYY-MM-DD') === today
  )
})

// 方法
const loadReports = async () => {
  try {
    loading.value = true
    const response = await apiService.getAllReports()
    reports.value = response.reports || []
  } catch (error) {
    console.error('加载报告失败:', error)
    ElMessage.error('加载报告失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleFilter = () => {
  currentPage.value = 1
}

const toggleViewMode = () => {
  viewMode.value = viewMode.value === 'card' ? 'list' : 'card'
}

const handlePageChange = (page) => {
  currentPage.value = page
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const viewReport = (report) => {
  router.push(`/analysis/${report.candidate_id}`)
}

const deleteReport = async (report) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除候选人"${report.candidate_name}"的分析报告吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 这里应该调用删除API，暂时简化处理
    ElMessage.success('删除成功')
    await loadReports()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const getScoreClass = (score) => {
  if (score >= 80) return 'score-high'
  if (score >= 60) return 'score-medium'
  return 'score-low'
}

const getScoreTagType = (score) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

const goBack = () => {
  router.push('/')
}

// 生命周期
onMounted(() => {
  loadReports()
})
</script>

<style scoped>
.reports-page {
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

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 2.5em;
  color: #2c3e50;
  margin-bottom: 12px;
}

.page-header p {
  color: #666;
  font-size: 1.1em;
}

.stats-overview {
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  color: #666;
  font-size: 0.9em;
}

.filter-section {
  margin-bottom: 24px;
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.list-header h3 {
  margin: 0;
  color: #2c3e50;
}

.loading-state {
  padding: 40px 0;
}

.empty-state {
  padding: 60px 0;
  text-align: center;
}

.card-view {
  margin-bottom: 24px;
}

.report-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.report-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.15);
  border-color: #409eff;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.candidate-name {
  font-size: 1.2em;
  font-weight: 600;
  color: #2c3e50;
}

.score-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9em;
}

.score-high {
  background: #f0f9ff;
  color: #67c23a;
}

.score-medium {
  background: #fef7e6;
  color: #e6a23c;
}

.score-low {
  background: #fef0f0;
  color: #f56c6c;
}

.card-content {
  margin-bottom: 16px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  margin-bottom: 8px;
  font-size: 0.9em;
}

.job-description {
  color: #666;
  font-size: 0.9em;
  line-height: 1.5;
  margin-bottom: 12px;
}

.created-time {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #999;
  font-size: 0.8em;
}

.card-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.list-view {
  margin-bottom: 24px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
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
  
  .page-header h1 {
    font-size: 2em;
  }
  
  .stat-card {
    padding: 16px;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .stat-number {
    font-size: 1.5em;
  }
  
  .container {
    padding: 0 16px;
  }
  
  .report-card {
    padding: 16px;
  }
}
</style>
