"""
智谱清言API客户端
"""
import requests
import json
from typing import Dict, List, Any, Optional
from config import ZHIPU_API_KEY, ZHIPU_API_URL

class ZhipuClient:
    """智谱清言API客户端"""
    
    def __init__(self):
        self.api_key = ZHIPU_API_KEY
        self.base_url = ZHIPU_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _call_api(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """调用智谱清言API"""
        data = {
            "model": "glm-4.5",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data,
                timeout=120  # 增加超时时间到120秒
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            raise Exception(f"API调用失败: {str(e)}")
    
    def parse_resume(self, resume_content: str) -> Dict[str, Any]:
        """解析简历内容"""
        prompt = f"""
        请解析以下简历内容，提取关键信息并以JSON格式返回：
        
        简历内容：
        {resume_content}
        
        请返回以下格式的JSON：
        {{
            "name": "候选人姓名",
            "contact_info": {{
                "phone": "电话号码",
                "email": "邮箱",
                "location": "所在地"
            }},
            "summary": "个人简介",
            "skills": ["技能1", "技能2", "技能3"],
            "experience": [
                {{
                    "company": "公司名称",
                    "position": "职位",
                    "duration": "工作时间",
                    "description": "工作描述"
                }}
            ],
            "education": [
                {{
                    "degree": "学位",
                    "major": "专业",
                    "school": "学校",
                    "year": "毕业年份"
                }}
            ],
            "projects": ["项目1", "项目2"],
            "certifications": ["证书1", "证书2"]
        }}
        
        请确保返回有效的JSON格式。
        """
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages)
        
        try:
            # 提取JSON部分
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            return json.loads(json_str)
        except:
            # 如果解析失败，返回默认结构
            return {
                "name": "未知",
                "contact_info": {},
                "summary": resume_content[:200] + "...",
                "skills": [],
                "experience": [],
                "education": [],
                "projects": [],
                "certifications": []
            }
    
    def analyze_match(self, resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """分析简历与职位描述的匹配度"""
        prompt = f"""
        请分析以下候选人简历与职位描述的匹配度：
        
        候选人信息：
        {json.dumps(resume_data, ensure_ascii=False, indent=2)}
        
        职位描述：
        {job_description}
        
        请返回以下格式的JSON分析结果：
        {{
            "match_score": 85.5,
            "skills_analysis": {{
                "required_skills": ["Python", "机器学习", "数据分析"],
                "candidate_skills": ["Python", "Java", "数据分析"],
                "matched_skills": ["Python", "数据分析"],
                "missing_skills": ["机器学习"],
                "skill_scores": {{"Python": 90, "数据分析": 85, "机器学习": 0}}
            }},
            "experience_analysis": {{
                "total_experience": 3.5,
                "relevant_experience": 2.0,
                "company_count": 2,
                "position_progression": ["初级开发", "中级开发", "高级开发"],
                "industry_experience": ["互联网", "金融科技"]
            }},
            "education_analysis": {{
                "degree_level": "本科",
                "major": "计算机科学",
                "school": "某大学",
                "graduation_year": 2020,
                "education_score": 80
            }},
            "strengths": ["相关技能匹配", "工作经验丰富"],
            "weaknesses": ["缺少机器学习经验", "教育背景一般"],
            "potential": "候选人具有扎实的技术基础，学习能力强，适合该职位"
        }}
        
        请确保返回有效的JSON格式，match_score为0-100的数值。
        """
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            return json.loads(json_str)
        except:
            # 返回默认分析结果
            return {
                "match_score": 70.0,
                "skills_analysis": {
                    "required_skills": [],
                    "candidate_skills": resume_data.get("skills", []),
                    "matched_skills": [],
                    "missing_skills": [],
                    "skill_scores": {}
                },
                "experience_analysis": {
                    "total_experience": len(resume_data.get("experience", [])),
                    "relevant_experience": len(resume_data.get("experience", [])),
                    "company_count": len(set([exp.get("company", "") for exp in resume_data.get("experience", [])])),
                    "position_progression": [exp.get("position", "") for exp in resume_data.get("experience", [])],
                    "industry_experience": []
                },
                "education_analysis": {
                    "degree_level": "未知",
                    "major": "未知",
                    "school": "未知",
                    "graduation_year": None,
                    "education_score": 60
                },
                "strengths": ["有工作经验"],
                "weaknesses": ["信息不足"],
                "potential": "需要进一步了解"
            }
    
    def generate_interview_questions(self, resume_data: Dict[str, Any], job_description: str, analysis_result: Dict[str, Any]) -> List[str]:
        """生成个性化面试问题"""
        prompt = f"""
        基于以下信息，为候选人生成10个个性化的面试问题：
        
        候选人简历：
        {json.dumps(resume_data, ensure_ascii=False, indent=2)}
        
        职位描述：
        {job_description}
        
        匹配分析结果：
        {json.dumps(analysis_result, ensure_ascii=False, indent=2)}
        
        请生成涵盖以下方面的问题：
        1. 技术能力验证
        2. 项目经验深入
        3. 问题解决能力
        4. 团队合作
        5. 学习能力
        6. 职业规划
        
        请以JSON数组格式返回问题列表：
        ["问题1", "问题2", "问题3", ...]
        """
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages)
        
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            json_str = response[json_start:json_end]
            
            return json.loads(json_str)
        except:
            # 返回默认问题
            return [
                "请介绍一下您最擅长的技术栈？",
                "描述一个您解决过的技术难题？",
                "您在团队项目中通常扮演什么角色？",
                "您如何学习新的技术？",
                "您的职业规划是什么？",
                "描述一个您主导的项目？",
                "您如何处理工作中的压力？",
                "您认为自己的优势是什么？",
                "您希望从这份工作中获得什么？",
                "您还有什么问题要问我们？"
            ]
    
    def generate_analysis_report(self, resume_data: Dict[str, Any], job_description: str, analysis_result: Dict[str, Any], interview_questions: List[str]) -> str:
        """生成完整的分析报告"""
        prompt = f"""
        请基于以下信息生成一份详细的候选人分析报告：
        
        候选人信息：
        {json.dumps(resume_data, ensure_ascii=False, indent=2)}
        
        职位描述：
        {job_description}
        
        匹配分析：
        {json.dumps(analysis_result, ensure_ascii=False, indent=2)}
        
        面试问题：
        {json.dumps(interview_questions, ensure_ascii=False, indent=2)}
        
        请生成一份专业的Markdown格式分析报告，包含以下部分：
        
        # 📊 候选人分析报告
        
        ## 👤 基本信息
        [候选人姓名、联系方式等基本信息]
        
        ## 🎯 匹配度评估
        [总体匹配度评分和简要说明，使用**粗体**强调关键信息]
        
        ## 💼 技能匹配分析
        [技能匹配情况，优势和不足，使用列表格式]
        
        ## 🏢 工作经验分析
        [工作经验评估，相关性和深度]
        
        ## 🎓 教育背景分析
        [教育背景与职位要求的匹配度]
        
        ## ✅ 候选人优势
        [候选人的主要优势和亮点，使用列表和强调]
        
        ## ⚠️ 潜在不足
        [需要关注的问题和风险点]
        
        ## 🚀 发展潜力
        [候选人未来发展的潜力和建议]
        
        ## 💡 面试建议
        [基于分析结果的面试重点和建议]
        
        ## 📝 综合评价
        [整体评价和录用建议，使用引用格式突出重要内容]
        
        > **注意**：请使用丰富的Markdown格式，包括粗体、斜体、列表、引用块等，让报告更加专业和易读。
        
        请确保报告内容详实、客观，便于HR和面试官参考。
        """
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages, temperature=0.8)
        return response
    
    def generate_chart_data(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成图表数据"""
        skills_analysis = analysis_result.get("skills_analysis", {})
        experience_analysis = analysis_result.get("experience_analysis", {})
        education_analysis = analysis_result.get("education_analysis", {})
        
        # 技能匹配雷达图数据 - 增强数据完整性
        skill_scores = skills_analysis.get("skill_scores", {})
        candidate_skills = skills_analysis.get("candidate_skills", [])
        required_skills = skills_analysis.get("required_skills", [])
        
        # 如果没有技能分数，基于技能列表生成默认分数
        if not skill_scores and candidate_skills:
            skill_scores = {skill: min(100, 70 + len(skill) * 3) for skill in candidate_skills[:8]}
        
        # 如果还是没有，生成基于职位要求的默认数据
        if not skill_scores and required_skills:
            skill_scores = {skill: min(100, 60 + len(skill) * 4) for skill in required_skills[:6]}
        
        # 最后的保底方案
        if not skill_scores:
            skill_scores = {
                "技术能力": 70,
                "项目经验": 65,
                "学习能力": 80,
                "沟通能力": 75,
                "问题解决": 70
            }
        
        skill_radar_data = {
            "categories": list(skill_scores.keys())[:8],  # 限制最多8个技能
            "values": list(skill_scores.values())[:8]
        }
        
        # 经验分析柱状图数据 - 增强数据完整性
        total_exp = experience_analysis.get("total_experience", 0)
        relevant_exp = experience_analysis.get("relevant_experience", 0)
        
        # 如果经验数据为0，尝试从其他字段推断
        if total_exp == 0:
            position_count = len(experience_analysis.get("position_progression", []))
            total_exp = position_count * 1.5 if position_count > 0 else 2.0
        
        if relevant_exp == 0:
            relevant_exp = total_exp * 0.8
        
        experience_bar_data = {
            "categories": ["总经验", "相关经验", "公司数量"],
            "values": [
                round(total_exp, 1),
                round(relevant_exp, 1),
                experience_analysis.get("company_count", 1)
            ]
        }
        
        # 教育背景饼图数据 - 增强数据完整性
        education_score = education_analysis.get("education_score", 0)
        if education_score == 0:
            # 基于教育背景推断分数
            degree_level = education_analysis.get("degree_level", "未知")
            if "博士" in degree_level:
                education_score = 95
            elif "硕士" in degree_level:
                education_score = 85
            elif "本科" in degree_level:
                education_score = 75
            elif "专科" in degree_level:
                education_score = 60
            else:
                education_score = 50
        
        education_pie_data = [
            {"name": "教育匹配度", "value": education_score},
            {"name": "其他因素", "value": 100 - education_score}
        ]
        
        # 新增：技能对比柱状图
        skill_comparison_data = {
            "categories": ["候选技能数", "匹配技能数", "缺失技能数"],
            "values": [
                len(candidate_skills),
                len(skills_analysis.get("matched_skills", [])),
                len(skills_analysis.get("missing_skills", []))
            ]
        }
        
        # 新增：综合能力雷达图
        comprehensive_radar_data = {
            "categories": ["技术能力", "工作经验", "教育背景", "学习能力", "沟通能力"],
            "values": [
                min(100, skill_radar_data["values"][0] if skill_radar_data["values"] else 70),
                min(100, (total_exp / 5) * 100),  # 5年经验为满分
                education_score,
                min(100, 75 + (total_exp * 5)),  # 经验越多学习能力越强
                min(100, 70 + (experience_analysis.get("company_count", 1) * 10))  # 公司越多沟通能力越强
            ]
        }
        
        return {
            "skill_radar": skill_radar_data,
            "experience_bar": experience_bar_data,
            "education_pie": education_pie_data,
            "skill_comparison": skill_comparison_data,
            "comprehensive_radar": comprehensive_radar_data,
            "match_score": analysis_result.get("match_score", 0)
        }
    
    def comprehensive_analysis(self, resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """综合分析：一次API调用完成所有分析任务"""
        prompt = f"""
        作为AI招聘专家，请对以下候选人进行全面的招聘分析。

        候选人简历：
        {json.dumps(resume_data, ensure_ascii=False, indent=2)}

        职位描述：
        {job_description}

        请提供以下分析结果，以JSON格式返回：

        1. match_score: 总体匹配度分数 (0-100)
        2. skills_analysis: 技能分析
           - required_skills: 职位要求的技能列表
           - candidate_skills: 候选人具备的技能列表
           - matched_skills: 匹配的技能列表
           - missing_skills: 缺失的技能列表
           - skill_scores: 各技能的评分 (技能名: 分数)
        3. experience_analysis: 经验分析
           - total_experience: 总工作经验年数
           - relevant_experience: 相关工作经验年数
           - company_count: 工作公司数量
           - position_progression: 职位发展路径
           - industry_experience: 行业经验
        4. education_analysis: 教育背景分析
           - degree_level: 学位级别
           - major: 专业
           - school: 学校
           - graduation_year: 毕业年份
           - education_score: 教育匹配度分数
        5. strengths: 候选人优势列表
        6. weaknesses: 候选人不足列表
        7. potential: 发展潜力评估

        请严格按照以下JSON格式返回结果，不要包含任何其他文本或代码块标记：
        
        {{
            "match_score": 85,
            "skills_analysis": {{
                "required_skills": ["技能1", "技能2"],
                "candidate_skills": ["技能1", "技能3"],
                "matched_skills": ["技能1"],
                "missing_skills": ["技能2"],
                "skill_scores": {{"技能1": 90.0, "技能2": 60.0}}
            }},
            "experience_analysis": {{
                "total_experience": 3.0,
                "relevant_experience": 2.5,
                "company_count": 2,
                "position_progression": ["初级", "中级"],
                "industry_experience": ["互联网", "金融"]
            }},
            "education_analysis": {{
                "degree_level": "本科",
                "major": "计算机科学",
                "school": "某大学",
                "graduation_year": 2020,
                "education_score": 85.0
            }},
            "strengths": ["优势1", "优势2"],
            "weaknesses": ["不足1", "不足2"],
            "potential": "潜力评估文本"
        }}
        """
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_api(messages, temperature=0.3)
        
        try:
            # 尝试多种方式提取JSON
            json_str = None
            
            # 方法1：查找完整的JSON对象
            json_start = response.find('{')
            if json_start != -1:
                json_end = response.rfind('}') + 1
                if json_end > json_start:
                    json_str = response[json_start:json_end]
            
            # 方法2：如果方法1失败，尝试查找JSON代码块
            if not json_str:
                import re
                json_pattern = r'```json\s*(\{.*?\})\s*```'
                match = re.search(json_pattern, response, re.DOTALL)
                if match:
                    json_str = match.group(1)
            
            # 方法3：如果还是失败，尝试查找任何看起来像JSON的内容
            if not json_str:
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                match = re.search(json_pattern, response, re.DOTALL)
                if match:
                    json_str = match.group(0)
            
            if not json_str:
                raise ValueError("无法从响应中提取JSON")
            
            result = json.loads(json_str)
            
            # 确保所有必要字段都存在并格式化正确
            if "match_score" not in result:
                result["match_score"] = 0
            if "skills_analysis" not in result:
                result["skills_analysis"] = {}
            if "experience_analysis" not in result:
                result["experience_analysis"] = {}
            if "education_analysis" not in result:
                result["education_analysis"] = {}
            if "strengths" not in result:
                result["strengths"] = []
            if "weaknesses" not in result:
                result["weaknesses"] = []
            if "potential" not in result:
                result["potential"] = "暂无评估"
            
            # 修复experience_analysis格式
            exp_analysis = result.get("experience_analysis", {})
            if isinstance(exp_analysis.get("total_experience"), str):
                # 尝试从字符串中提取数字，如"1-2年" -> 1.5
                exp_str = exp_analysis["total_experience"]
                import re
                numbers = re.findall(r'\d+', exp_str)
                if numbers:
                    result["experience_analysis"]["total_experience"] = float(numbers[0])
                else:
                    result["experience_analysis"]["total_experience"] = 0.0
            
            if isinstance(exp_analysis.get("relevant_experience"), str):
                exp_str = exp_analysis["relevant_experience"]
                import re
                numbers = re.findall(r'\d+', exp_str)
                if numbers:
                    result["experience_analysis"]["relevant_experience"] = float(numbers[0])
                else:
                    result["experience_analysis"]["relevant_experience"] = 0.0
            
            if isinstance(exp_analysis.get("position_progression"), str):
                result["experience_analysis"]["position_progression"] = [exp_analysis["position_progression"]]
            
            if isinstance(exp_analysis.get("industry_experience"), str):
                result["experience_analysis"]["industry_experience"] = [exp_analysis["industry_experience"]]
            
            return result
            
        except Exception as e:
            print(f"综合分析解析失败: {e}")
            print(f"原始响应: {response[:500]}...")  # 打印前500个字符用于调试
            
            # 返回一个完整的默认结构，确保所有字段都有值
            return self._create_default_analysis_result(resume_data, job_description)
    
    def _create_default_analysis_result(self, resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """创建默认的分析结果结构"""
        # 尝试从响应中提取一些基本信息
        try:
            import re
            
            # 尝试提取匹配度分数
            match_score = 50.0  # 默认中等分数
            score_match = re.search(r'(\d+(?:\.\d+)?)[分]', str(resume_data))
            if score_match:
                match_score = min(100.0, max(0.0, float(score_match.group(1))))
            
            # 基于简历数据生成合理的默认值
            skills = resume_data.get("skills", [])
            experiences = resume_data.get("experience", [])
            education = resume_data.get("education", [])
            
            # 生成技能分析
            skills_analysis = {
                "required_skills": self._extract_skills_from_jd(job_description),
                "candidate_skills": skills[:10],  # 限制数量
                "matched_skills": skills[:5],  # 假设前5个是匹配的
                "missing_skills": [],
                "skill_scores": {skill: min(100, 60 + len(skill) * 2) for skill in skills[:5]}
            }
            
            # 生成经验分析
            experience_analysis = {
                "total_experience": len(experiences) * 1.5,  # 估算
                "relevant_experience": len(experiences) * 1.2,
                "company_count": len(set([exp.get("company", "") for exp in experiences if exp.get("company")])),
                "position_progression": [exp.get("position", "未知职位") for exp in experiences[:3]],
                "industry_experience": list(set([exp.get("industry", "未知行业") for exp in experiences if exp.get("industry")]))
            }
            
            # 生成教育分析
            education_analysis = {
                "degree_level": "本科" if education else "未知",
                "major": education[0].get("major", "未知专业") if education else "未知专业",
                "school": education[0].get("school", "未知学校") if education else "未知学校",
                "graduation_year": education[0].get("graduation_year") if education else None,
                "education_score": 70.0
            }
            
            # 生成优势和不足
            strengths = [
                "具备相关工作经验" if experiences else "有学习能力",
                "掌握多种技能" if len(skills) > 3 else "有基础技能",
                "教育背景良好" if education else "有发展潜力"
            ]
            
            weaknesses = [
                "缺少特定技能经验" if len(skills) < 3 else "经验相对有限",
                "需要进一步培训" if not experiences else "技能深度待提升"
            ]
            
            potential = "候选人具备基础条件，通过适当培训可以胜任工作"
            
            return {
                "match_score": match_score,
                "skills_analysis": skills_analysis,
                "experience_analysis": experience_analysis,
                "education_analysis": education_analysis,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "potential": potential
            }
            
        except Exception as e:
            print(f"创建默认分析结果失败: {e}")
            # 最后的保底方案
            return {
                "match_score": 50.0,
                "skills_analysis": {
                    "required_skills": [],
                    "candidate_skills": [],
                    "matched_skills": [],
                    "missing_skills": [],
                    "skill_scores": {}
                },
                "experience_analysis": {
                    "total_experience": 0.0,
                    "relevant_experience": 0.0,
                    "company_count": 0,
                    "position_progression": [],
                    "industry_experience": []
                },
                "education_analysis": {
                    "degree_level": "未知",
                    "major": "未知",
                    "school": "未知",
                    "graduation_year": None,
                    "education_score": 60.0
                },
                "strengths": ["有学习能力"],
                "weaknesses": ["需要进一步了解"],
                "potential": "需要进一步评估"
            }
    
    def _extract_skills_from_jd(self, job_description: str) -> List[str]:
        """从职位描述中提取技能关键词 - 覆盖多个岗位和行业"""
        # 扩展的技能关键词库，按类别组织
        skill_keywords = {
            # 编程语言
            "programming_languages": [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Swift", "Kotlin",
                "PHP", "Ruby", "Scala", "R", "MATLAB", "Perl", "Lua", "Haskell", "Clojure", "Erlang",
                "Shell", "Bash", "PowerShell", "Assembly", "COBOL", "Fortran", "Ada", "Pascal"
            ],
            
            # Web开发框架
            "web_frameworks": [
                "React", "Vue", "Angular", "Svelte", "Next.js", "Nuxt.js", "SvelteKit",
                "Django", "Flask", "FastAPI", "Spring Boot", "Spring MVC", "Spring Security",
                "Express.js", "Koa.js", "Nest.js", "Laravel", "Symfony", "CodeIgniter",
                "Ruby on Rails", "Sinatra", "ASP.NET", "ASP.NET Core", "Blazor", "WebAPI",
                "Gin", "Fiber", "Echo", "Gorilla", "Buffalo"
            ],
            
            # 数据库技术
            "databases": [
                "MySQL", "PostgreSQL", "Oracle", "SQL Server", "SQLite", "MariaDB",
                "MongoDB", "Redis", "Cassandra", "CouchDB", "Neo4j", "Elasticsearch",
                "InfluxDB", "TimescaleDB", "ClickHouse", "BigQuery", "Snowflake",
                "DynamoDB", "Firebase", "Supabase", "PlanetScale", "CockroachDB"
            ],
            
            # 云服务和DevOps
            "cloud_devops": [
                "AWS", "Azure", "GCP", "阿里云", "腾讯云", "华为云", "百度云",
                "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions",
                "Terraform", "Ansible", "Chef", "Puppet", "SaltStack",
                "Prometheus", "Grafana", "ELK Stack", "Splunk", "Datadog",
                "Istio", "Linkerd", "Helm", "ArgoCD", "Tekton"
            ],
            
            # 移动开发
            "mobile_development": [
                "React Native", "Flutter", "Xamarin", "Ionic", "Cordova", "PhoneGap",
                "Android Studio", "Xcode", "Unity", "Unreal Engine", "Godot",
                "iOS开发", "Android开发", "跨平台开发", "原生开发", "混合开发"
            ],
            
            # AI和机器学习
            "ai_ml": [
                "机器学习", "深度学习", "人工智能", "神经网络", "计算机视觉", "自然语言处理",
                "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "OpenCV", "NLTK",
                "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Jupyter",
                "Hugging Face", "Transformers", "BERT", "GPT", "LLM", "大语言模型",
                "数据分析", "数据挖掘", "数据可视化", "统计学习", "强化学习"
            ],
            
            # 大数据技术
            "big_data": [
                "Hadoop", "Spark", "Kafka", "Storm", "Flink", "Hive", "Pig", "HBase",
                "大数据", "数据仓库", "ETL", "数据湖", "实时计算", "批处理",
                "Apache Airflow", "Apache Beam", "Apache NiFi", "DataX", "MaxCompute"
            ],
            
            # 测试和质量保证
            "testing_qa": [
                "单元测试", "集成测试", "端到端测试", "性能测试", "安全测试", "自动化测试",
                "Jest", "Mocha", "Chai", "Cypress", "Selenium", "Playwright", "TestCafe",
                "JUnit", "TestNG", "Mockito", "PowerMock", "Jest", "Enzyme", "Testing Library"
            ],
            
            # 安全技术
            "security": [
                "网络安全", "信息安全", "数据安全", "应用安全", "云安全", "安全审计",
                "渗透测试", "漏洞扫描", "安全编码", "加密算法", "身份认证", "权限管理",
                "OWASP", "NIST", "ISO27001", "SOC2", "PCI DSS", "GDPR", "数据保护"
            ],
            
            # 产品和管理
            "product_management": [
                "产品经理", "项目管理", "敏捷开发", "Scrum", "Kanban", "看板管理",
                "用户研究", "用户体验", "产品设计", "需求分析", "原型设计",
                "Jira", "Confluence", "Trello", "Asana", "Notion", "Figma", "Sketch"
            ],
            
            # 软技能
            "soft_skills": [
                "沟通能力", "团队协作", "领导力", "学习能力", "解决问题", "创新思维",
                "项目管理", "时间管理", "压力管理", "客户服务", "演讲能力", "写作能力",
                "英语", "日语", "韩语", "法语", "德语", "西班牙语", "多语言"
            ],
            
            # 行业特定技能
            "industry_specific": [
                # 金融科技
                "金融科技", "区块链", "数字货币", "支付系统", "风控", "反欺诈",
                "量化交易", "算法交易", "高频交易", "金融建模", "风险管理",
                
                # 电商
                "电商", "零售", "供应链", "库存管理", "订单处理", "支付网关",
                "推荐系统", "搜索引擎", "商品管理", "营销自动化",
                
                # 游戏开发
                "游戏开发", "游戏引擎", "游戏设计", "3D建模", "动画制作", "音效设计",
                "游戏策划", "关卡设计", "用户界面设计", "游戏测试",
                
                # 医疗健康
                "医疗信息化", "健康管理", "医疗数据", "远程医疗", "医疗设备", "药物研发",
                "临床试验", "医疗影像", "电子病历", "健康监测",
                
                # 教育科技
                "在线教育", "教育技术", "学习管理系统", "课程设计", "学习分析", "智能辅导",
                "虚拟现实", "增强现实", "混合现实", "沉浸式学习",
                
                # 汽车科技
                "自动驾驶", "车联网", "智能汽车", "新能源汽车", "汽车电子", "车载系统",
                "ADAS", "V2X", "汽车软件", "车载娱乐系统",
                
                # 物联网
                "物联网", "IoT", "传感器", "嵌入式开发", "边缘计算", "智能硬件",
                "工业4.0", "智能制造", "智慧城市", "智能家居"
            ],
            
            # 设计技能
            "design_skills": [
                "UI设计", "UX设计", "平面设计", "视觉设计", "交互设计", "产品设计",
                "Adobe Photoshop", "Adobe Illustrator", "Adobe XD", "Figma", "Sketch",
                "InVision", "Principle", "Framer", "Protopie", "Origami Studio",
                "用户研究", "可用性测试", "信息架构", "设计系统", "品牌设计"
            ],
            
            # 营销和运营
            "marketing_operations": [
                "数字营销", "社交媒体营销", "内容营销", "搜索引擎优化", "搜索引擎营销",
                "Google Analytics", "Facebook Ads", "Google Ads", "微信营销", "抖音营销",
                "用户增长", "用户运营", "社群运营", "活动策划", "品牌推广",
                "数据分析", "A/B测试", "转化率优化", "用户画像", "精准营销"
            ]
        }
        
        found_skills = []
        jd_lower = job_description.lower()
        
        # 遍历所有技能类别
        for category, skills in skill_keywords.items():
            for skill in skills:
                if skill.lower() in jd_lower:
                    found_skills.append(skill)
        
        # 去重并限制数量
        unique_skills = list(dict.fromkeys(found_skills))  # 保持顺序的去重
        return unique_skills[:15]  # 增加到15个技能
