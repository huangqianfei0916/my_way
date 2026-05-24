<!--
 * Copyright (c) 2026 by huangqianfei@tju.edu.cn All Rights Reserved. 
 * @Author: huangqianfei@tju.edu.cn
 * @Date: 2026-05-20 21:42:38
 * @Description: 
-->
# MyPath – Streamlit MVP

## 快速启动

### 1. 安装依赖
```bash
pip install streamlit
```

### 2. 运行
```bash
streamlit run app.py
```

浏览器打开 http://localhost:8501 即可。

---

## 功能说明

| 功能 | 状态 | 说明 |
|------|------|------|
| 首页仪表盘 | ✅ | 当前目标卡片、所有目标列表、数据概览统计 |
| 快速记录 | ✅ | 关联目标、选择标签，实时保存 |
| 时间线 | ✅ | 按标签筛选，每条记录可删除 |
| 目标管理 | ✅ | 最多 5 个目标，创建 / 删除，删除后自动激活下一个 |
| 数据持久化 | ✅ | 本地 JSON 文件（mypath_data.json）|
| 回顾 / 存档 | 🚧 | 开发中 |

## 数据存储
数据保存在 `mypath_data.json`，首次运行无预设数据，创建目标后自动写入文件。

## 升级建议（Post-MVP）
- 替换 JSON → SQLite / Supabase
- 添加用户登录（streamlit-authenticator）
- 部署到 Streamlit Cloud