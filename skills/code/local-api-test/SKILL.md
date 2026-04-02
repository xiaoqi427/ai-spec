---
name: local-api-test
description: 本地启动 Spring Boot 服务后，用 curl 测试后端 API 接口。Bug 修复后、代码提交前，先本地验证接口正确性。当用户需要在本地环境用 curl 测试后端接口时使用。
allowed-tools: Bash(curl:*, mvn:*, java:*), AskUser
---
# Local API Test (本地接口测试)
@author: sevenxiao

## 概述

代码修复后、提交前，**本地启动服务** + **curl 测试接口**，验证修复有效。

**流程**: 编译 → 本地启动服务 → curl 登录获取 Cookie → curl 调用目标接口 → 验证响应

## 外部依赖

无外部依赖，仅使用 curl 命令行。

---

## 使用方式

```bash
# 测试 config 服务的某个接口
/skill local-api-test config "/accountteam/getList"

# 测试 claim-base 服务
/skill local-api-test claim-base "/T001/loadClaim?claimId=123"

# 自动根据修改文件推断服务和接口
/skill local-api-test auto
```

---

## 服务端口映射表

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

> **注意**: 本地测试不走网关，直接访问目标服务端口。

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

### Cookie-based Token 认证

系统使用 Cookie 传递认证信息，流程如下：

```
1. POST /sys/login → 返回 Set-Cookie (Authorization, auth_userId, auth_userName, ...)
2. 后续请求带上这些 Cookie → 服务端从 Cookie 提取 Token → Redis 校验
```

### Cookie 名称

| Cookie | 说明 |
|--------|------|
| `Authorization` | 认证令牌 (UUID) |
| `auth_userId` | 用户 ID |
| `auth_userName` | 用户名 |
| `auth_groupId` | 用户组 ID |
| `auth_operatingSystem` | 操作系统标识 |

---

## 测试流程（4 步）

### Step 1: 本地编译

```bash
# 编译目标模块
cd /Users/xiaoqi/Documents/work/yili/<服务目录>
mvn compile -pl <web模块> -am -q
```

**编译失败** → 停止，先修复编译问题。

---

### Step 2: 本地启动服务

**方式一**: Maven 启动（推荐，后台运行）

```bash
# config 服务示例
cd /Users/xiaoqi/Documents/work/yili/fssc-config-service
mvn spring-boot:run -pl fssc-config-web -Dspring-boot.run.profiles=local &

# claim-base 服务示例
cd /Users/xiaoqi/Documents/work/yili/fssc-claim-service
mvn spring-boot:run -pl claim-base/claim-base-web -Dspring-boot.run.profiles=local &
```

**方式二**: 如果用户已经在 IDE 中启动，跳过此步骤，直接询问用户

```
⚠️ 请确认服务是否已在本地启动？
- 如果已在 IntelliJ IDEA 中启动，请告知端口号
- 如果未启动，我将通过 Maven 启动
```

**健康检查**:
```bash
# 检查服务是否已启动
curl -s http://127.0.0.1:<端口>/actuator/health 2>/dev/null || echo "服务未启动"
```

---

### Step 3: 登录获取 Cookie

```bash
# 登录接口在 config 服务（端口 8080）
# 保存 Cookie 到文件，后续请求复用
curl -v -X POST http://127.0.0.1:8080/sys/login \
  -H "Content-Type: application/json" \
  -d '{"usernum":"fsscadmin","password":"2"}' \
  -c /tmp/fssc-cookies.txt \
  2>&1

# 验证 Cookie 是否获取成功
cat /tmp/fssc-cookies.txt
```

**登录账号配置**: 读取 `config/local-test-auth.yaml`（见下方配置文件说明）

**登录失败排查**:
- 检查 config 服务是否启动在 8080
- 检查 Redis 是否连通（Token 缓存依赖 Redis）
- 检查账号密码是否正确

---

### Step 4: curl 测试目标接口

```bash
# GET 请求示例
curl -s -X GET "http://127.0.0.1:<端口>/<path>?<params>" \
  -b /tmp/fssc-cookies.txt \
  -H "Content-Type: application/json" \
  | python3 -m json.tool

# POST 请求示例
curl -s -X POST "http://127.0.0.1:<端口>/<path>" \
  -b /tmp/fssc-cookies.txt \
  -H "Content-Type: application/json" \
  -d '<request-body>' \
  | python3 -m json.tool
```

**验证结果**:
1. HTTP 状态码: 200 → 成功，401 → 未认证，500 → 服务端错误
2. 响应体: 检查 `code`/`success` 字段
3. 业务数据: 检查关键字段值是否符合预期

---

## 常用测试场景模板

### 查询列表类接口

```bash
# 分页查询
curl -s -X POST "http://127.0.0.1:<端口>/<path>/list" \
  -b /tmp/fssc-cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"pageNum":1,"pageSize":10}' \
  | python3 -m json.tool
```

### 保存/更新类接口

```bash
# 先查询获取数据
curl -s -X GET "http://127.0.0.1:<端口>/<path>/get?id=<id>" \
  -b /tmp/fssc-cookies.txt \
  | python3 -m json.tool

# 修改后保存
curl -s -X POST "http://127.0.0.1:<端口>/<path>/save" \
  -b /tmp/fssc-cookies.txt \
  -H "Content-Type: application/json" \
  -d '<modified-data>' \
  | python3 -m json.tool

# 再次查询验证
curl -s -X GET "http://127.0.0.1:<端口>/<path>/get?id=<id>" \
  -b /tmp/fssc-cookies.txt \
  | python3 -m json.tool
```

### Bug 修复验证模板

```bash
# 1. 查询修改前状态（记录关键字段值）
curl -s ... | python3 -m json.tool > /tmp/before.json

# 2. 执行触发修复逻辑的操作
curl -s -X POST ...

# 3. 查询修改后状态（对比关键字段值）
curl -s ... | python3 -m json.tool > /tmp/after.json

# 4. 对比前后差异
diff /tmp/before.json /tmp/after.json
```

---

## 根据修改文件推断测试接口

当使用 `auto` 模式时，按以下规则推断：

1. **找到修改的 Service/Business 类**
2. **向上追溯 Controller**，找到对应的 API 路径
3. **确定端口和请求方式**
4. **构造测试请求**

```
修改文件 → 所在模块 → Controller 路径 → API URL → curl 命令
```

示例：
```
TProcAccountantteamUserServiceImpl.java
  → fssc-config-service (端口 8080)
  → AccountantTeamController
  → POST /accountteam/updateTprocAccountantteamUser
  → curl -s -X POST http://127.0.0.1:8080/accountteam/updateTprocAccountantteamUser ...
```

---

## Swagger 文档地址

每个服务启动后可查看 Swagger UI 获取接口文档：

```
http://127.0.0.1:<端口>/swagger-ui/index.html
http://127.0.0.1:<端口>/v3/api-docs
```

> 先打开 Swagger 了解接口参数格式，再构造 curl 请求。

---

## 配置文件

### `config/local-test-auth.yaml`

```yaml
# 本地测试登录账号（本地开发环境）
login_url: "http://127.0.0.1:8080/sys/login"
username: "fsscadmin"
password: "2"

# Cookie 存储路径
cookie_file: "/tmp/fssc-cookies.txt"
```

---

## 输出格式

测试完成后输出：

```markdown
## 本地接口测试结果

- **服务**: fssc-config-service (端口 8080)
- **接口**: POST /accountteam/updateTprocAccountantteamUser
- **登录状态**: ✅ 成功
- **请求**:
  ```bash
  curl -s -X POST http://127.0.0.1:8080/accountteam/updateTprocAccountantteamUser ...
  ```
- **响应状态**: 200 OK
- **响应体**:
  ```json
  { "code": 0, "success": true, "data": ... }
  ```
- **验证结果**: ✅ 修改时间和修改人已正确更新
```

---

## 强制约束

1. **先启动再测试**: 确认服务已启动且健康，再发 curl 请求
2. **必须登录**: 除了健康检查，所有业务接口都需要带 Cookie
3. **保存 Cookie**: 登录后 Cookie 保存到文件，后续请求复用，不重复登录
4. **结果可读**: curl 响应用 `python3 -m json.tool` 格式化输出
5. **不修改数据**: 测试优先用查询接口，如需修改操作要告知用户
6. **清理资源**: 测试完成后提醒用户关闭本地服务（如果是 Maven 启动的）
