# 🚀 快速启动指南 - 公司API版

## ✅ 测试结果

公司API测试成功！✅

```
状态码: 200
响应: {"code": 0, "data": 1283, "msg": ""}
```

---

## 🎯 立即开始（3步）

### 1️⃣ 安装依赖
```bash
pip install flask flask-cors pandas requests qrcode pillow
```

### 2️⃣ 启动服务
```bash
python app_flask.py
```

服务地址: http://localhost:5000

### 3️⃣ 访问页面
- 电脑: http://localhost:5000/h5/index.html
- 手机: 运行 `python generate_qrcode.py` 生成二维码扫码访问

---

## 📱 使用演示

1. **打开H5页面** → 看到爆文清单
2. **点击"🚀 发布到内容库"** → 确认发布
3. **自动调用公司API** → 创建笔记
4. **显示发布结果** → ✅ 成功

---

## 🎉 核心功能

### 自动数据处理
- ✅ 从CSV读取爆文
- ✅ 自动提取标签（#标签）
- ✅ 清理内容格式
- ✅ 调用公司API发布

### API集成
- ✅ 支持公司API
- ✅ 错误处理
- ✅ 超时控制
- ✅ 详细日志

---

## 📝 API说明

**当前配置:**
```
URL: http://contenthub-test.applesay.cn/app-api/hotword/note-review/create
```

**请求格式:**
```json
{
  "title": "标题",
  "content": "正文",
  "tags": "标签1,标签2",
  "noteImage": "图片URL"
}
```

**响应格式:**
```json
{
  "code": 0,
  "data": 1283,
  "msg": ""
}
```

---

## 🔧 自定义配置

### 修改API地址

编辑 `app_flask.py` 第32行:
```python
'COMPANY_API_URL': 'your-api-url-here',
```

### 修改默认标签

编辑 `app_flask.py` 第333行:
```python
tags = ','.join(hashtags) if hashtags else '你的标签1,你的标签2'
```

---

## 📂 文件清单

| 文件 | 说明 | 状态 |
|------|------|------|
| app_flask.py | 后端API服务 | ✅ 已更新 |
| h5/index.html | 前端H5页面 | ✅ 已更新 |
| test_company_api.py | API测试工具 | ✅ 测试通过 |
| .env.company | 配置示例 | ✅ 已创建 |
| 公司API版本使用指南.md | 详细文档 | ✅ 已创建 |

---

## 💡 提示

1. **测试API** - 运行 `python test_company_api.py`
2. **查看日志** - 后端控制台显示详细日志
3. **调试模式** - Flask Debug模式已启用

---

## 🎊 完成！

系统已就绪，可以开始使用了！

**下一步:**
1. 运行 `python app_flask.py`
2. 打开 http://localhost:5000/h5/index.html
3. 点击"发布到内容库"测试

---

**祝使用愉快！** 🔥
