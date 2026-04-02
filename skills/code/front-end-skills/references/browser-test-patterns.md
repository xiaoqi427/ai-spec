# 浏览器测试模式

说明：

- 浏览器联调统一优先 `Playwright`
- `agent-browser` 作为 fallback，不再与 Playwright 平行混用
- 如果用户要求仓库内可复跑测试脚本，应继续走 Playwright

## open-page

目标：确认页面能否被真实打开，而不是只靠代码猜测。

### 输入

- 目标仓库
- 页面组件路径，或路由模块，或页面名称
- 本地服务地址，例如 `http://localhost:8080`

### 步骤

1. 从 `src/config/route/index.js` 找模块入口
2. 从模块路由文件推出完整路径
3. 若页面依赖 query，先确认最小参数
4. 用 `agent-browser` 打开页面
5. 看当前 URL、页面标题、页面主体是否符合预期

如果是 `fssc-web`，优先先跑路由解析脚本：

```bash
python3 scripts/route-open.py src/page/accountingDoc/autoArchiveCheckPool/index.vue
python3 scripts/route-open.py autoArchiveCheckPool --open
```

### 示例

```bash
agent-browser open http://localhost:8080/accountingDoc/autoArchiveCheckPool
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser screenshot --full
agent-browser get url
```

### 成功标准

- 页面不是白屏
- 不是 404
- 不是登录拦截页
- 目标页面关键区域可见

## smoke-test

目标：做一轮低成本、高收益的基础页面验收。

### 最小检查项

- 页面主标题或主容器出现
- 查询区出现
- 表格、表单或核心内容区出现
- 至少一个关键按钮可见
- 执行一次关键入口动作后，页面反馈合理

### 示例

```bash
agent-browser open http://localhost:8080/accountingDoc/autoArchiveCheckPool
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser get url
```

### 常见失败类型

- 路由未注册
- URL 推导错误
- 页面依赖 query，但未传参数
- 接口报错导致白屏或空页
- 权限或登录态拦截
- 改动后关键按钮不再可见

## 结果输出模板

- 页面：`<页面名>`
- URL：`<实际访问地址>`
- 动作：`open-page` 或 `smoke-test`
- 结果：通过 / 失败
- 现象：一句话说明实际看到的页面状态
- 原因：若失败，给出最可能原因
