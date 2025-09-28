<template>
  <div class="markdown-renderer">
    <div 
      v-if="htmlContent" 
      class="markdown-content" 
      v-html="htmlContent"
    ></div>
    <div v-else class="no-content">
      <el-empty description="暂无内容" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, nextTick, watch } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const props = defineProps({
  content: {
    type: String,
    default: ''
  }
})

// 配置marked
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

// 渲染Markdown为HTML
const htmlContent = computed(() => {
  if (!props.content) return ''
  
  try {
    return marked(props.content)
  } catch (error) {
    console.error('Markdown渲染错误:', error)
    return props.content
  }
})

// 动态应用标题样式
const applyTitleStyles = () => {
  nextTick(() => {
    const container = document.querySelector('.markdown-content')
    if (!container) return

    const headings = container.querySelectorAll('h2')
    headings.forEach(heading => {
      const text = heading.textContent.toLowerCase()
      
      // 移除现有的特殊样式类
      heading.classList.remove('match-score', 'strengths', 'weaknesses', 'skills', 'experience', 'education', 'potential', 'interview', 'summary')
      
      // 根据内容添加相应的样式类
      if (text.includes('匹配度') || text.includes('评分') || text.includes('评估')) {
        heading.classList.add('match-score')
      } else if (text.includes('优势') || text.includes('优点') || text.includes('亮点')) {
        heading.classList.add('strengths')
      } else if (text.includes('不足') || text.includes('劣势') || text.includes('风险') || text.includes('问题')) {
        heading.classList.add('weaknesses')
      } else if (text.includes('技能') || text.includes('能力') || text.includes('技术')) {
        heading.classList.add('skills')
      } else if (text.includes('经验') || text.includes('工作') || text.includes('履历')) {
        heading.classList.add('experience')
      } else if (text.includes('教育') || text.includes('学历') || text.includes('背景')) {
        heading.classList.add('education')
      } else if (text.includes('潜力') || text.includes('发展') || text.includes('未来')) {
        heading.classList.add('potential')
      } else if (text.includes('面试') || text.includes('建议') || text.includes('推荐')) {
        heading.classList.add('interview')
      } else if (text.includes('综合') || text.includes('总结') || text.includes('结论')) {
        heading.classList.add('summary')
      }
    })
  })
}

// 监听内容变化
watch(() => props.content, () => {
  applyTitleStyles()
})

onMounted(() => {
  applyTitleStyles()
})
</script>

<style scoped>
.markdown-renderer {
  width: 100%;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.markdown-content {
  line-height: 1.7;
  color: #374151;
  font-size: 15px;
  padding: 32px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  max-width: none;
}

/* H1 - 主标题：深蓝色背景，最高重要程度 */
.markdown-content :deep(h1) {
  font-size: 24px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 24px 0;
  padding: 16px 20px;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(30, 64, 175, 0.2);
}

/* H2 - 重要章节：绿色背景，高重要程度 */
.markdown-content :deep(h2) {
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
  margin: 32px 0 16px 0;
  padding: 12px 16px;
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(5, 150, 105, 0.2);
}

/* H3 - 分析项目：橙色背景，中等重要程度 */
.markdown-content :deep(h3) {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  margin: 24px 0 12px 0;
  padding: 10px 14px;
  background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%);
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(234, 88, 12, 0.2);
}

/* H4 - 子项目：紫色背景，较低重要程度 */
.markdown-content :deep(h4) {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  margin: 20px 0 8px 0;
  padding: 8px 12px;
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(124, 58, 237, 0.2);
}

/* 特殊标题样式 - 根据内容类型区分 */
/* 匹配度评估 - 蓝色系 */
.markdown-content :deep(h2.match-score) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
}

/* 优势/优点 - 绿色系 */
.markdown-content :deep(h2.strengths) {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
}

/* 不足/劣势 - 红色系 */
.markdown-content :deep(h2.weaknesses) {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
}

/* 技能分析 - 青色系 */
.markdown-content :deep(h2.skills) {
  background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%) !important;
}

/* 经验分析 - 橙色系 */
.markdown-content :deep(h2.experience) {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%) !important;
}

/* 教育背景 - 紫色系 */
.markdown-content :deep(h2.education) {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
}

/* 发展潜力 - 金色系 */
.markdown-content :deep(h2.potential) {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
}

/* 面试建议 - 粉色系 */
.markdown-content :deep(h2.interview) {
  background: linear-gradient(135deg, #db2777 0%, #be185d 100%) !important;
}

/* 综合评价 - 灰色系 */
.markdown-content :deep(h2.summary) {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%) !important;
}

.markdown-content :deep(p) {
  margin: 12px 0;
  line-height: 1.8;
}

.markdown-content :deep(ul) {
  margin: 16px 0;
  padding-left: 24px;
  list-style: none;
}

.markdown-content :deep(ol) {
  margin: 16px 0;
  padding-left: 24px;
}

.markdown-content :deep(li) {
  margin: 8px 0;
  line-height: 1.6;
  position: relative;
}

.markdown-content :deep(ul > li::before) {
  content: "•";
  color: #6b7280;
  font-weight: bold;
  position: absolute;
  left: -16px;
}

.markdown-content :deep(ol > li::before) {
  content: counter(item) ".";
  counter-increment: item;
  color: #6b7280;
  font-weight: 500;
  position: absolute;
  left: -24px;
  min-width: 16px;
}

.markdown-content :deep(blockquote) {
  margin: 20px 0;
  padding: 16px 20px;
  background: #f9fafb;
  border-left: 4px solid #6b7280;
  border-radius: 0 4px 4px 0;
  font-style: italic;
  color: #4b5563;
  position: relative;
}

.markdown-content :deep(code) {
  background: #f1f5f9;
  color: #e11d48;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
}

.markdown-content :deep(pre) {
  background: #f8fafc;
  color: #374151;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 16px 0;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  border: 1px solid #e5e7eb;
}

.markdown-content :deep(pre code) {
  background: transparent;
  color: inherit;
  padding: 0;
}

.markdown-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 14px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.markdown-content :deep(th) {
  background: #f9fafb;
  color: #374151;
  font-weight: 600;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
}

.markdown-content :deep(td) {
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  vertical-align: top;
  background: #ffffff;
}

.markdown-content :deep(tr:nth-child(even) td) {
  background: #f9fafb;
}

.markdown-content :deep(tr:hover td) {
  background: #f3f4f6;
}

.markdown-content :deep(strong) {
  font-weight: 600;
  color: #111827;
}

.markdown-content :deep(em) {
  font-style: italic;
  color: #6b7280;
}

.markdown-content :deep(hr) {
  border: none;
  height: 1px;
  background: #e5e7eb;
  margin: 32px 0;
}

.markdown-content :deep(a) {
  color: #2563eb;
  text-decoration: underline;
  text-decoration-color: #dbeafe;
  transition: all 0.2s ease;
}

.markdown-content :deep(a:hover) {
  color: #1d4ed8;
  text-decoration-color: #1d4ed8;
}

.no-content {
  padding: 40px 0;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .markdown-content {
    font-size: 14px;
    padding: 24px;
  }
  
  .markdown-content :deep(h1) {
    font-size: 20px;
    margin: 0 0 20px 0;
  }
  
  .markdown-content :deep(h2) {
    font-size: 18px;
    margin: 28px 0 14px 0;
  }
  
  .markdown-content :deep(h3) {
    font-size: 16px;
    margin: 20px 0 10px 0;
  }
  
  .markdown-content :deep(h4) {
    font-size: 15px;
    margin: 16px 0 8px 0;
  }
  
  .markdown-content :deep(pre) {
    padding: 12px;
    font-size: 13px;
  }
  
  .markdown-content :deep(table) {
    font-size: 13px;
  }
  
  .markdown-content :deep(th),
  .markdown-content :deep(td) {
    padding: 10px 12px;
  }
  
  .markdown-content :deep(ul),
  .markdown-content :deep(ol) {
    padding-left: 20px;
  }
  
  .markdown-content :deep(blockquote) {
    padding: 12px 16px;
    margin: 16px 0;
  }
}
</style>
