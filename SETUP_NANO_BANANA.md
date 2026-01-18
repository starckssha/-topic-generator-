# Google Nano Banana (Gemini) 图片生成配置指南

## 📋 什么是 Nano Banana？

**Nano Banana** 是 Google 基于 Gemini 2.5 Flash 的AI图片生成模型，可以生成高质量的教育类配图。

## 🚀 快速配置步骤

### 1. 获取 Google API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登录你的 Google 账号
3. 点击 "Create API Key" 创建新的 API Key
4. 复制你的 API Key（格式类似：`AIzaSy...`）

### 2. 配置环境变量

**Windows (命令提示符):**
```cmd
set GOOGLE_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

**永久设置（Windows）:**
```cmd
setx GOOGLE_API_KEY "your_api_key_here"
```

### 3. 测试配置

运行测试脚本：
```bash
cd D:\Projects\ClaudeCode\topicgenerater
python nano_banana_generator.py
```

如果成功，你会看到：
```
✅ 图片生成完成！
🔗 URL: http://192.168.31.8:5000/static/generated_images/xxxxx.png
```

### 4. 重启服务

配置完成后，重启 Flask 服务：
```bash
python app_flask.py
```

## 💰 费用说明

- **免费额度**: Google Gemini API 提供免费额度
- **收费**: 超出免费额度后，按使用量计费
- **价格**: 约 $0.001-0.002/张（取决于分辨率）
- **估算**: 每月生成1000张图片约 $1-2

## 🔧 工作原理

1. 用户访问移动端页面
2. 页面自动调用 `/api/generate-image` API
3. 后端使用 Google Gemini API 生成图片
4. 图片保存到本地服务器
5. 返回图片URL给前端显示

## 📸 图片特点

- **分辨率**: 高清，适合移动端
- **风格**: 教育科技感，渐变紫蓝色调
- **元素**: 包含教育图标、标题文字
- **格式**: PNG，透明背景支持

## ❓ 常见问题

### Q: 没有配置 API Key 会怎样？
A: 系统会自动使用占位图服务（placehold.co），功能正常可用

### Q: 如何确认使用了 Nano Banana？
A: 查看图片URL，如果包含 `nano_banana` 字样说明使用了真实AI生成

### Q: 生成失败怎么办？
A: 系统会自动降级到占位图，不影响使用

### Q: 可以批量生成吗？
A: 可以，但注意不要超过 API 速率限制（建议每分钟不超过60张）

## 📚 相关链接

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API 文档](https://ai.google.dev/gemini-api/docs/image-generation)
- [API Key 管理](https://aistudio.google.com/app/apikey)
- [Nano Banana 介绍](https://blog.google/innovation-and-ai/products/nano-banana-pro/)

## 🎯 优化建议

1. **提示词优化**: 根据内容类型调整提示词
2. **批量预生成**: 可以预先为所有爆文生成配图
3. **缓存机制**: 避免重复生成相同标题的图片
4. **风格统一**: 保持品牌色彩和风格一致性

---

**Sources:**
- [Introducing Nano Banana Pro](https://blog.google/innovation-and-ai/products/nano-banana-pro/)
- [Nano Banana image generation | Gemini API](https://ai.google.dev/gemini-api/docs/image-generation)
- [Gemini 2.5 Flash Image (Nano Banana)](https://aistudio.google.com/models/gemini-2-5-flash-image)
- [Nano Banana Pro Image Generation - API易文档中心](https://docs.apiyi.com/en/api-capabilities/nano-banana-image)
