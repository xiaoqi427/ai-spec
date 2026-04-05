---
name: local-api-test
description: 本地启动 Spring Boot 服务后，自动读取前端 page/service、后端 Controller、DTO schema 和 mock 信息，推导接口并直接用 curl 执行本地接口测试。适用于 Bug 修复后、提交前、本地联调时做真实接口验证。
allowed-tools: Bash(curl:*, mvn:*, java:*, python3:*, rg:*, sed:*, cat:*, jq:*, find:*, ls:*, lsof:*, ps:*), AskUser
---
# Local API Test (本地接口测试)
@author: sevenxiao

## 概述

这个 skill 不再只是“告诉用户怎么 curl”。

默认目标是:

1. 自动定位目标接口
2. 自动确认本地服务和端口
3. 自动登录拿 Cookie
4. 自动构造安全请求体
5. 自动执行 curl
6. 输出可复用的请求和结果

核心新增能力:

- 支持从 `fssc-web` 的 `index.vue / service.js` 反推接口
- 支持从 `Setaria.getHttp().<domain>` 自动映射到本地服务
- 支持向后追到后端 `Controller`
- 支持读取前端 `json-schema` 生成最小请求体
- 参数不够时，支持继续参考 `mock` 或浏览器真实请求

---

## 自动执行原则

使用此 skill 时，**默认自己执行**，不要只停在命令建议。

除以下场景外，必须直接跑完整流程:

- 目标接口只有写操作，且会改真实本地数据
- 关键参数完全无法从代码、schema、mock、页面入口推断
- 本地服务启动方式存在歧义，必须让用户确认

执行优先级:

1. **安全查询接口优先**
2. **能自动推断就自动推断**
3. **能自动执行就自动执行**
4. **只在必要时才询问用户**

---

## 可集成能力

### 1. `front-end-skills`

用途:

- 定位页面入口
- 定位 `index.vue / service.js / route`
- 必要时用路由脚本确认页面 URL

复用文件:

- `ai-spec/skills/code/front-end-skills/SKILL.md`
- `ai-spec/skills/code/front-end-skills/scripts/route-open.py`

### 2. `sit-smoke-test`

用途:

- 当代码里推不出完整参数时，用浏览器真实打开页面
- 观察页面行为和真实请求
- 作为“抓真实请求再回放为 curl”的兜底策略

复用文件:

- `ai-spec/skills/code/sit-smoke-test/SKILL.md`

> `local-api-test` 仍以本地接口为主。只有代码推断不够时，才借用浏览器能力。

---

## 使用方式

```bash
# 直接测后端接口
/skill local-api-test config "/accountteam/getList"
/skill local-api-test claim-base "/myReimbursement/AllClaimSavedList"

# 从前端页面反推主接口并执行
/skill local-api-test from-frontend fssc-web/src/page/myInfo/myDraft/index.vue

# 从 service.js 反推指定导出函数并执行
/skill local-api-test from-service fssc-web/src/page/myInfo/myDraft/service.js --api apiTableData

# 自动根据修改文件判断
/skill local-api-test auto

# 代码推不出完整参数时，进入抓包回放模式
/skill local-api-test capture-and-replay fssc-web/src/page/claim/fund/T044/index.vue
```

---

## 内置脚本

### `scripts/infer_frontend_api.py`

路径:

```bash
ai-spec/skills/code/local-api-test/scripts/infer_frontend_api.py
```

作用:

- 读取页面或 `service.js`
- 提取 `export const apiXxx`
- 识别 `Setaria.getHttp().<domain>`
- 映射前端 baseURL
- 追溯本地后端 `Controller`
- 提取请求 DTO 类型
- 在 `fssc-web/src/json-schema/*.json` 中定位 schema
- 输出最小请求体、参数示例和 curl 模板

示例:

```bash
python3 ai-spec/skills/code/local-api-test/scripts/infer_frontend_api.py \
  fssc-web/src/page/myInfo/myDraft/index.vue --primary-only

python3 ai-spec/skills/code/local-api-test/scripts/infer_frontend_api.py \
  fssc-web/src/page/myInfo/myDraft/service.js --api-name apiTableData
```

---

## 智能推导顺序

当用户给页面、模块、路由或“修这个前端对应接口”这类请求时，按下面顺序推导:

1. **页面真实调用优先**
   - 先看 `index.vue`
   - 找 `request / load / save / submit / export` 方法里调用了哪个 API

2. **`service.js` 定义优先**
   - 找 `export const apiXxx = (...) => request.post(...)`
   - 找 `Setaria.getHttp().<domain>`

3. **后端 Controller 确认**
   - 找 `@RequestMapping`
   - 找 `@PostMapping / @GetMapping`
   - 找 `@RequestBody` 参数类型

4. **DTO schema 补齐**
   - 在 `fssc-web/src/json-schema/*.json` 中找对应 DTO
   - 对分页接口自动构造 `pageNum/pageSize/params`

5. **mock 和页面默认值兜底**
   - 找 `fssc-web/mock/**`
   - 找页面 `conditionData`、`created`、默认参数组装逻辑

6. **浏览器抓真实请求兜底**
   - 代码仍然不够时，再联动 `sit-smoke-test`

### 推导冲突时的优先级

如果页面字段和 DTO 字段不一致，优先级如下:

1. 页面实际组参逻辑
2. service.js 调用方式
3. 后端 Controller/DTO
4. json-schema
5. mock

不要只拿 schema 硬猜参数。

---

## 服务映射

### 本地服务端口映射

| 模块 | 启动类 | 端口 | context-path |
|------|--------|------|-------------|
| `config` | `FsscConfigWebApp` | 8080 | / |
| `claim-base` | `FsscClaimBaseWebApp` | 8081 | / |
| `claim-eer` | `FsscClaimEerWebApp` | 7001 | /eer |
| `claim-ptp` | `FsscClaimPtpWebApp` | 7002 | /ptp |
| `claim-rtr` | `FsscClaimRtrWebApp` | 7003 | /rtr |
| `claim-tr` | `FsscClaimTrWebApp` | 7006 | /tr |
| `claim-otc` | `FsscClaimOtcWebApp` | 7003 | /otc |
| `claim-fa` | `FsscClaimFaWebApp` | 7002 | /fa |
| `integration` | `FsscIntegrationWebApp` | 8083 | / |
| `fund` | `FsscFundWebApp` | 8082 | / |
| `invoice` | `FsscInvoiceWebApp` | 8082 | / |
| `bpm` | `FsscBpmWebApp` | 8085 | / |
| `image` | `ImageWebApp` | - | / |
| `aam` | `FsscAamWebApp` | 7788 | / |
| `rule` | `ReApplication` | 9013 | / |
| `gateway` | `GatewayApplication` | 80 | / |

### 前端 domain 到本地模块映射

| 前端 domain | baseURL | 本地模块 |
|------------|---------|---------|
| `config` | `/api/config` | `config` |
| `claimBase` | `/api/claim-base` | `claim-base` |
| `claim` | `/api/claim` | `claim-base` |
| `tr` | `/api/claim/tr` | `claim-tr` |
| `ptp` | `/api/claim/ptp` | `claim-ptp` |
| `rtr` | `/api/claim/rtr` | `claim-rtr` |
| `otc` | `/api/claim/otc` | `claim-otc` |
| `eer` | `/api/claim/eer` | `claim-eer` |
| `fa` | `/api/claim/fa` | `claim-fa` |
| `fund` | `/api/fund` | `fund` |
| `invoice` | `/api/invoice` | `invoice` |
| `image` | `/api/image` | `image` |
| `aam` | `/api/aam` | `aam` |
| `bpm` | `/api/bpm` | `bpm` |
| `re` | `/api/re` | `rule` |

> `pi / cac / bi / voucher / base` 这几类如果脚本没法映射到本地模块，要在结果里明确标记“需人工确认”。

---

## 启动类路径

| 模块 | 启动类路径 |
|------|-----------|
| `config` | `fssc-config-service/fssc-config-web/src/main/java/com/yili/config/web/FsscConfigWebApp.java` |
| `claim-base` | `fssc-claim-service/claim-base/claim-base-web/src/main/java/com/yili/claim/base/web/FsscClaimBaseWebApp.java` |
| `claim-eer` | `fssc-claim-service/claim-eer/claim-eer-web/src/main/java/com/yili/claim/eer/web/FsscClaimEerWebApp.java` |
| `claim-ptp` | `fssc-claim-service/claim-ptp/claim-ptp-web/src/main/java/com/yili/claim/ptp/web/FsscClaimPtpWebApp.java` |
| `claim-rtr` | `fssc-claim-service/claim-rtr/claim-rtr-web/src/main/java/com/yili/claim/rtr/web/FsscClaimRtrWebApp.java` |
| `claim-tr` | `fssc-claim-service/claim-tr/claim-tr-web/src/main/java/com/yili/claim/tr/web/FsscClaimTrWebApp.java` |
| `claim-otc` | `fssc-claim-service/claim-otc/claim-otc-web/src/main/java/com/yili/claim/otc/web/FsscClaimOtcWebApp.java` |
| `claim-fa` | `fssc-claim-service/claim-fa/claim-fa-web/src/main/java/com/yili/claim/fa/web/FsscClaimFaWebApp.java` |

---

## 认证机制

系统使用 Cookie 传递认证信息，流程如下:

1. `POST /sys/login`
2. 保存返回 Cookie 到文件
3. 后续接口全部复用同一个 Cookie 文件

Cookie 关键字段:

- `Authorization`
- `auth_userId`
- `auth_userName`
- `auth_groupId`
- `auth_operatingSystem`

---

## 标准执行流程

### Step 1: 定位目标接口

按输入模式处理:

- **直接模块 + path**: 直接用给定接口
- **`from-frontend`**: 跑 `infer_frontend_api.py`，默认选页面主查询接口
- **`from-service`**: 跑 `infer_frontend_api.py --api-name <api>`
- **`auto`**: 先找最近修改的前端或后端文件，再推导接口
- **`capture-and-replay`**: 先代码推导，不够再抓真实请求

### Step 2: 本地编译

**前置条件**: JDK 21（`java -version` 输出必须包含 `21`，否则编译必定失败）

```bash
cd /Users/xiaoqi/Documents/work/yili/<服务目录>
mvn compile -pl <web模块> -am -q -Dmaven.repo.local=/Users/xiaoqi/.m2/yili-repository
```

编译失败就停止，先修复。

### Step 3: 本地启动服务

优先复用用户已经启动的服务。未启动时自动启动。

```bash
# config 服务
cd /Users/xiaoqi/Documents/work/yili/fssc-config-service
mvn spring-boot:run -pl fssc-config-web -Dspring-boot.run.profiles=local -Dmaven.repo.local=/Users/xiaoqi/.m2/yili-repository &

# claim-base 服务
cd /Users/xiaoqi/Documents/work/yili/fssc-claim-service
mvn spring-boot:run -pl claim-base/claim-base-web -Dspring-boot.run.profiles=local -Dmaven.repo.local=/Users/xiaoqi/.m2/yili-repository &
```

健康检查:

```bash
curl -s http://127.0.0.1:<端口>/actuator/health 2>/dev/null || echo "服务未启动"
```

### Step 4: 登录获取 Cookie

```bash
curl -s -X POST http://127.0.0.1:8080/sys/login \
  -H "Content-Type: application/json" \
  -d '{"usernum":"fsscadmin","password":"2"}' \
  -c /tmp/fssc-cookies.txt | python3 -m json.tool
```

### Step 5: 生成请求体

规则:

- `GET` 接口: 不带 body
- `PageParam<ReqDto, XxxDto>`: 默认

```json
{
  "pageNum": 1,
  "pageSize": 10,
  "params": {}
}
```

- 有 DTO schema: 输出 `params_example` 或对象示例
- 有页面默认入参: 优先用页面真实入参
- 有 route/query 依赖: 尽量从代码里取 `claimId / itemId / archiveId`

### Step 6: 执行 curl

```bash
curl -s -X POST "http://127.0.0.1:<端口>/<path>" \
  -b /tmp/fssc-cookies.txt \
  -H "Content-Type: application/json" \
  -d '<request-body>' \
  | python3 -m json.tool
```

### Step 7: 校验结果

至少检查:

1. HTTP 状态码
2. 认证是否通过
3. `code / success / message`
4. 关键业务字段

---

## `capture-and-replay` 模式

当以下场景出现时进入该模式:

- 接口只有动态 query/body，代码里拿不到实参
- 页面会在提交前做复杂数据转换
- 需要完全仿造前端真实请求

执行方式:

1. 用 `front-end-skills` 找页面入口
2. 本地前端能跑就先开本地前端
3. 参考 `sit-smoke-test` 的浏览器执行策略
4. 打开页面，触发真实请求
5. 记录 method、URL、payload、headers
6. 再回放为本地 curl

> 这个模式的目标不是“测前端”，而是“抓真实请求模板，服务于本地接口测试”。

---

## 输出格式

测试完成后统一输出:

```markdown
## 本地接口测试结果

- 服务: claim-base (端口 8081)
- 推导来源: myDraft/index.vue -> myDraft/service.js -> MyReimbursementController
- 接口: POST /myReimbursement/AllClaimSavedList
- 登录状态: 成功
- 请求体: {"pageNum":1,"pageSize":10,"params":{}}
- curl: curl -s -X POST ...
- 响应状态: 200
- 响应摘要: code=0 success=true
- 验证结果: 成功
```

如果是从前端推导出的接口，必须额外输出:

- 页面文件
- service 文件
- 选中的 API 导出函数
- 对应 Controller
- DTO/schema 来源

---

## 配置文件

### `config/local-test-auth.yaml`

```yaml
workspace_root: "/Users/xiaoqi/Documents/work/yili"
login_url: "http://127.0.0.1:8080/sys/login"
username: "fsscadmin"
password: "2"
cookie_file: "/tmp/fssc-cookies.txt"
default_page_num: 1
default_page_size: 10
prefer_safe_read_api: true
```

---

## 强制约束

1. **JDK 21 强制**: 编译和启动服务前必须确认 JDK 版本为 21
2. **先定位再执行**: 不要猜接口，先确认来源
3. **先健康检查再调用**: 服务没起来不能直接打业务接口
4. **必须登录**: 除健康检查外，业务接口一律带 Cookie
5. **优先跑读接口**: 查询、加载、列表优先
6. **写接口先告知风险**: 会改数据时要明确说明
7. **结果必须可复用**: 输出最终 curl 和最小请求体
8. **不要只给建议**: 除非遇到阻塞，否则必须自己执行
