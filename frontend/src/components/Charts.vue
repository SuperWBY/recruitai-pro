<template>
  <div class="charts-container">
    <!-- 匹配度圆形进度图 -->
    <div class="chart-section">
      <h3 class="chart-title">
        <Trophy class="w-5 h-5" />
        匹配度评分
      </h3>
      <div class="match-score-chart">
        <v-chart 
          class="chart" 
          :option="matchScoreOption" 
          autoresize
        />
      </div>
    </div>

    <!-- 技能匹配雷达图 -->
    <div class="chart-section">
      <h3 class="chart-title">
        <Star class="w-5 h-5" />
        技能匹配分析
      </h3>
      <div class="skill-radar-chart">
        <v-chart 
          class="chart" 
          :option="skillRadarOption" 
          autoresize
        />
      </div>
    </div>

    <!-- 经验分析柱状图 -->
    <div class="chart-section">
      <h3 class="chart-title">
        <TrendingUp class="w-5 h-5" />
        工作经验分析
      </h3>
      <div class="experience-bar-chart">
        <v-chart 
          class="chart" 
          :option="experienceBarOption" 
          autoresize
        />
      </div>
    </div>

    <!-- 教育背景饼图 -->
    <div class="chart-section">
      <h3 class="chart-title">
        <GraduationCap class="w-5 h-5" />
        教育背景分析
      </h3>
      <div class="education-pie-chart">
        <v-chart 
          class="chart" 
          :option="educationPieOption" 
          autoresize
        />
      </div>
    </div>

    <!-- 技能对比柱状图 -->
    <div class="chart-section">
      <h3 class="chart-title">
        <DataBoard class="w-5 h-5" />
        技能对比分析
      </h3>
      <div class="skill-comparison-chart">
        <v-chart 
          class="chart" 
          :option="skillComparisonOption" 
          autoresize
        />
      </div>
    </div>

    <!-- 综合能力雷达图 -->
    <div class="chart-section">
      <h3 class="chart-title">
        <PieChart class="w-5 h-5" />
        综合能力评估
      </h3>
      <div class="comprehensive-radar-chart">
        <v-chart 
          class="chart" 
          :option="comprehensiveRadarOption" 
          autoresize
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import * as echarts from 'echarts'
import VChart from 'vue-echarts'
import { Trophy, Star, TrendingUp, GraduationCap, TrendingUp as DataBoard, PieChart } from 'lucide-vue-next'

// 使用完整的ECharts，不需要手动注册组件

// 定义props
const props = defineProps({
  chartData: {
    type: Object,
    default: () => ({
      match_score: 0,
      skill_radar: {
        categories: [],
        values: []
      },
      experience_bar: {
        categories: [],
        values: []
      },
      education_pie: []
    })
  }
})

// 匹配度评分图表配置
const matchScoreOption = computed(() => {
  const score = props.chartData.match_score || 0
  
  // 根据分数选择颜色
  let color = '#f56c6c' // 红色 - 低分
  if (score >= 80) {
    color = '#67c23a' // 绿色 - 高分
  } else if (score >= 60) {
    color = '#e6a23c' // 橙色 - 中等
  }

  return {
    series: [
      {
        name: '匹配度',
        type: 'gauge',
        center: ['50%', '60%'],
        radius: '90%',
        min: 0,
        max: 100,
        splitNumber: 10,
        axisLine: {
          lineStyle: {
            width: 8,
            color: [
              [0.3, '#f56c6c'],
              [0.7, '#e6a23c'],
              [1, '#67c23a']
            ]
          }
        },
        pointer: {
          itemStyle: {
            color: color
          }
        },
        axisTick: {
          distance: -8,
          length: 8,
          lineStyle: {
            color: '#fff',
            width: 2
          }
        },
        splitLine: {
          distance: -12,
          length: 12,
          lineStyle: {
            color: '#fff',
            width: 4
          }
        },
        axisLabel: {
          color: '#666',
          fontSize: 12,
          distance: -20
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}分',
          color: color,
          fontSize: 20,
          fontWeight: 'bold',
          offsetCenter: [0, '70%']
        },
        data: [
          {
            value: score,
            name: '匹配度'
          }
        ]
      }
    ]
  }
})

// 技能匹配雷达图配置
const skillRadarOption = computed(() => {
  const { categories, values } = props.chartData.skill_radar || { categories: [], values: [] }
  
  if (categories.length === 0) {
    return {
      title: {
        text: '暂无技能数据',
        left: 'center',
        top: 'middle',
        textStyle: {
          color: '#999',
          fontSize: 16
        }
      }
    }
  }

  return {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    radar: {
      indicator: categories.map(category => ({
        name: category,
        max: 100
      })),
      center: ['60%', '50%'],
      radius: '70%',
      name: {
        textStyle: {
          color: '#666',
          fontSize: 12
        }
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(64, 158, 255, 0.1)', 'rgba(64, 158, 255, 0.2)']
        }
      },
      splitLine: {
        lineStyle: {
          color: '#409eff'
        }
      }
    },
    series: [
      {
        name: '技能匹配度',
        type: 'radar',
        data: [
          {
            value: values,
            name: '候选技能',
            areaStyle: {
              color: 'rgba(64, 158, 255, 0.3)'
            },
            lineStyle: {
              color: '#409eff',
              width: 2
            },
            itemStyle: {
              color: '#409eff'
            }
          }
        ]
      }
    ]
  }
})

// 经验分析柱状图配置
const experienceBarOption = computed(() => {
  const { categories, values } = props.chartData.experience_bar || { categories: [], values: [] }
  
  if (categories.length === 0) {
    return {
      title: {
        text: '暂无经验数据',
        left: 'center',
        top: 'middle',
        textStyle: {
          color: '#999',
          fontSize: 16
        }
      }
    }
  }

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: categories,
        axisTick: {
          alignWithLabel: true
        },
        axisLabel: {
          color: '#666'
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        axisLabel: {
          color: '#666',
          formatter: '{value}年'
        }
      }
    ],
    series: [
      {
        name: '工作经验',
        type: 'bar',
        barWidth: '60%',
        data: values,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#409eff' },
            { offset: 1, color: '#67c23a' }
          ])
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}年'
        }
      }
    ]
  }
})

// 教育背景饼图配置
const educationPieOption = computed(() => {
  const data = props.chartData.education_pie || []
  
  if (data.length === 0) {
    return {
      title: {
        text: '暂无教育数据',
        left: 'center',
        top: 'middle',
        textStyle: {
          color: '#999',
          fontSize: 16
        }
      }
    }
  }

  return {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c}% ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '教育匹配',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '20',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data,
        color: ['#67c23a', '#e6a23c', '#f56c6c', '#409eff']
      }
    ]
  }
})

// 技能对比柱状图配置
const skillComparisonOption = computed(() => {
  const { categories, values } = props.chartData.skill_comparison || { categories: [], values: [] }
  
  if (categories.length === 0) {
    return {
      title: {
        text: '暂无技能对比数据',
        left: 'center',
        top: 'middle',
        textStyle: {
          color: '#999',
          fontSize: 16
        }
      }
    }
  }

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['技能数量'],
      top: '5%'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisTick: {
        alignWithLabel: true
      },
      axisLabel: {
        color: '#666',
        fontSize: 12,
        interval: 0,
        rotate: 0
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#666',
        fontSize: 12
      }
    },
    series: [
      {
        name: '技能数量',
        type: 'bar',
        data: values,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#2378f7' },
              { offset: 0.7, color: '#2378f7' },
              { offset: 1, color: '#83bff6' }
            ])
          }
        },
        animationDelay: function (idx) {
          return idx * 10
        }
      }
    ],
    animationEasing: 'elasticOut',
    animationDelayUpdate: function (idx) {
      return idx * 5
    }
  }
})

// 综合能力雷达图配置
const comprehensiveRadarOption = computed(() => {
  const { categories, values } = props.chartData.comprehensive_radar || { categories: [], values: [] }
  
  if (categories.length === 0) {
    return {
      title: {
        text: '暂无综合能力数据',
        left: 'center',
        top: 'middle',
        textStyle: {
          color: '#999',
          fontSize: 16
        }
      }
    }
  }

  return {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['综合能力']
    },
    radar: {
      indicator: categories.map(category => ({
        name: category,
        max: 100
      })),
      center: ['60%', '50%'],
      radius: '70%',
      name: {
        textStyle: {
          color: '#666',
          fontSize: 12
        }
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(250, 250, 250, 0.3)', 'rgba(200, 200, 200, 0.3)']
        }
      },
      splitLine: {
        lineStyle: {
          color: '#999'
        }
      }
    },
    series: [
      {
        name: '综合能力评估',
        type: 'radar',
        data: [
          {
            value: values,
            name: '能力评估',
            areaStyle: {
              color: 'rgba(64, 158, 255, 0.2)'
            },
            lineStyle: {
              color: '#409eff',
              width: 3
            },
            itemStyle: {
              color: '#409eff'
            }
          }
        ]
      }
    ]
  }
})
</script>

<style scoped>
.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 20px;
  padding: 16px 0;
  max-width: 1400px;
  margin: 0 auto;
}

/* 图表区域样式优化 */
.chart-section {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.chart-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.chart-section:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.chart-section:hover::before {
  opacity: 1;
}

/* 图表标题样式优化 */
.chart-title {
  font-size: 1.1em;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e5e7eb;
  position: relative;
}

.chart-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 30px;
  height: 2px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 1px;
}

.chart-title .el-icon {
  color: #667eea;
  font-size: 1.2em;
}

/* 图表容器样式 */
.chart {
  width: 100%;
  height: 280px;
  border-radius: 8px;
  background: #ffffff;
  position: relative;
  border: 1px solid #f0f0f0;
}

/* 特殊图表高度调整 */
.match-score-chart .chart {
  height: 320px;
}

.skill-comparison-chart .chart,
.comprehensive-radar-chart .chart {
  height: 300px;
}

.skill-radar-chart .chart,
.education-pie-chart .chart {
  height: 280px;
}

/* 响应式设计优化 */
@media (max-width: 1200px) {
  .charts-container {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 18px;
    padding: 14px 0;
  }
}

@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 16px 12px;
    max-width: 100%;
  }
  
  .chart-section {
    padding: 18px;
    border-radius: 12px;
  }
  
  .chart {
    height: 260px;
  }
  
  .match-score-chart .chart {
    height: 300px;
  }
  
  .skill-comparison-chart .chart,
  .comprehensive-radar-chart .chart {
    height: 280px;
  }
}

@media (max-width: 480px) {
  .charts-container {
    padding: 12px 8px;
    gap: 14px;
  }
  
  .chart-section {
    padding: 16px;
    border-radius: 10px;
  }
  
  .chart-title {
    font-size: 1em;
    margin-bottom: 14px;
    gap: 8px;
  }
  
  .chart-title .el-icon {
    font-size: 1.1em;
  }
  
  .chart {
    height: 220px;
  }
  
  .match-score-chart .chart {
    height: 260px;
  }
  
  .skill-comparison-chart .chart,
  .comprehensive-radar-chart .chart {
    height: 240px;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .chart-section {
    background: #ffffff;
    border-color: rgba(226, 232, 240, 0.8);
    color: #2c3e50;
  }
  
  .chart-title {
    color: #2c3e50;
    border-bottom-color: #e5e7eb;
  }
  
  .chart {
    background: #ffffff;
    border-color: #f0f0f0;
  }
}

/* 打印样式 */
@media print {
  .charts-container {
    display: block;
    padding: 0;
  }
  
  .chart-section {
    break-inside: avoid;
    margin-bottom: 20px;
    box-shadow: none;
    border: 1px solid #ddd;
  }
  
  .chart {
    height: 250px;
  }
}
</style>
