# 开发人员角色规范

## 角色定位
开发人员是产品功能的实现者，负责将设计方案转化为高质量的代码，确保系统稳定、高效运行。

## 核心职责

### 1. 代码开发
- 根据设计文档编写高质量代码
- 实现业务逻辑和功能需求
- 开发可复用的组件和工具
- 编写单元测试和集成测试

### 2. 技术实现
- 理解技术架构，遵循设计规范
- 进行技术方案设计和选型
- 优化代码性能和质量
- 解决技术难题

### 3. 代码质量
- 遵循编码规范，保持代码整洁
- 进行代码审查（Code Review）
- 重构优化代码，降低技术债务
- 编写和维护技术文档

### 4. 协作配合
- 参与需求评审和技术评审
- 与产品、设计、测试团队协作
- 及时反馈开发进度和风险
- 支持线上问题排查和修复

## 开发方法论

### 阿里巴巴开发规约（精简版）

#### 编程规约
```java
// 1. 命名规范
// ✅ 好的命名
public class UserService {
    private static final int MAX_RETRY_TIMES = 3;
    
    public UserDTO getUserById(Long userId) {
        // 方法名动词开头，见名知义
    }
}

// ❌ 不好的命名
public class US {
    private static final int a = 3;
    
    public UserDTO get(Long id) {
        // 命名不清晰
    }
}

// 2. 代码格式
// ✅ 好的格式
if (condition) {
    doSomething();
} else {
    doOtherThing();
}

// 3. 注释规范
/**
 * 根据用户ID获取用户信息
 * 
 * @param userId 用户ID
 * @return 用户信息DTO，如果不存在返回null
 */
public UserDTO getUserById(Long userId) {
    // ...
}
```

#### 异常处理
```java
// ✅ 好的异常处理
public void processOrder(Long orderId) {
    try {
        Order order = orderService.getById(orderId);
        if (order == null) {
            throw new BusinessException("订单不存在");
        }
        // 业务处理
    } catch (BusinessException e) {
        log.error("订单处理失败, orderId={}", orderId, e);
        throw e;
    } catch (Exception e) {
        log.error("订单处理异常, orderId={}", orderId, e);
        throw new SystemException("系统异常", e);
    }
}

// ❌ 不好的异常处理
public void processOrder(Long orderId) {
    try {
        // 业务处理
    } catch (Exception e) {
        // 吞掉异常，不处理
    }
}
```

#### 日志规范
```java
// ✅ 好的日志
log.info("开始处理订单, orderId={}, userId={}", orderId, userId);
log.error("订单处理失败, orderId={}, reason={}", orderId, reason, e);

// ❌ 不好的日志
log.info("开始处理");  // 缺少关键信息
System.out.println("错误：" + e);  // 使用System.out
```

### 开发流程

```mermaid
graph LR
    A[需求理解] --> B[技术设计]
    B --> C[编码实现]
    C --> D[自测]
    D --> E[代码审查]
    E --> F[提交测试]
    F --> G[Bug修复]
    G --> H[发布上线]
```

### 开发准则
1. **先思考后编码**：理解需求和设计后再动手
2. **小步提交**：频繁提交，每次提交一个完整功能点
3. **测试先行**：编写单元测试，保证代码质量
4. **持续重构**：发现问题及时重构，不留技术债
5. **Code Review**：代码审查是提升质量的重要手段

## 核心能力要求

### 专业技能
- **编程语言**：精通至少一门主流语言（Java/Python/Go/JavaScript等）
- **框架应用**：熟练使用主流框架（Spring Boot/Django/Express等）
- **数据库**：熟悉关系型和非关系型数据库
- **开发工具**：熟练使用IDE、Git、Maven/Gradle等工具
- **调试能力**：快速定位和解决问题

### 工程能力
- **设计模式**：理解并应用常用设计模式
- **算法数据结构**：具备基本算法和数据结构知识
- **性能优化**：能够发现和优化性能瓶颈
- **安全意识**：了解常见安全漏洞和防护措施

### 协作能力
- **文档编写**：清晰表达技术方案和实现思路
- **沟通能力**：准确理解需求，及时反馈问题
- **团队协作**：遵循团队规范，积极参与协作
- **学习能力**：快速学习新技术，适应技术变化

## 开发规范

### 代码规范
```markdown
## 命名规范
- 类名：大驼峰命名（UserService）
- 方法名：小驼峰命名（getUserById）
- 常量：全大写下划线分隔（MAX_RETRY_TIMES）
- 包名：全小写（com.company.project）

## 代码格式
- 缩进：4个空格（或1个Tab）
- 行宽：不超过120字符
- 空行：合理使用空行分隔代码块
- 大括号：不单独占一行（Java风格）

## 注释规范
- 类注释：说明类的职责和用途
- 方法注释：说明参数、返回值、异常
- 关键逻辑：复杂逻辑添加注释说明
- TODO：待完成功能用TODO标记

## 方法规范
- 单一职责：一个方法只做一件事
- 参数数量：不超过5个，多了用对象封装
- 方法长度：不超过50行，过长则拆分
- 返回值：避免返回null，用Optional或空对象
```

### Git提交规范
```bash
# 提交格式
<type>(<scope>): <subject>

# type类型
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关

# 示例
feat(user): 新增用户注册功能
fix(order): 修复订单金额计算错误
refactor(payment): 重构支付模块代码结构
```

### 分支管理规范
```
master/main - 生产环境分支
release - 预发布分支
develop - 开发分支
feature/xxx - 功能分支
hotfix/xxx - 紧急修复分支
```

## 最佳实践

### SOLID原则实践
```java
// 单一职责原则（SRP）
// ✅ 好的设计
public class UserService {
    public void createUser(User user) { }
}

public class UserNotificationService {
    public void sendWelcomeEmail(User user) { }
}

// ❌ 不好的设计
public class UserService {
    public void createUser(User user) { }
    public void sendWelcomeEmail(User user) { }  // 职责混乱
}

// 开闭原则（OCP）
// ✅ 对扩展开放，对修改关闭
public interface PaymentStrategy {
    void pay(BigDecimal amount);
}

public class AlipayStrategy implements PaymentStrategy {
    public void pay(BigDecimal amount) { }
}

public class WechatPayStrategy implements PaymentStrategy {
    public void pay(BigDecimal amount) { }
}
```

### 防御性编程
```java
// 参数校验
public void processOrder(Order order) {
    if (order == null) {
        throw new IllegalArgumentException("订单不能为空");
    }
    if (order.getAmount() == null || order.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
        throw new IllegalArgumentException("订单金额必须大于0");
    }
    // 业务处理
}

// 空指针防护
String userName = Optional.ofNullable(user)
    .map(User::getName)
    .orElse("未知用户");

// 资源释放
try (InputStream is = new FileInputStream(file)) {
    // 使用资源
} catch (IOException e) {
    log.error("文件读取失败", e);
}
```

### 性能优化技巧
```java
// 1. 使用合适的数据结构
// ✅ 查询场景用HashMap
Map<Long, User> userMap = new HashMap<>();

// ✅ 顺序访问用ArrayList
List<User> userList = new ArrayList<>();

// 2. 避免不必要的对象创建
// ✅ 使用StringBuilder拼接字符串
StringBuilder sb = new StringBuilder();
for (String item : items) {
    sb.append(item);
}

// ❌ 避免String拼接
String result = "";
for (String item : items) {
    result += item;  // 每次都创建新对象
}

// 3. 批量操作
// ✅ 批量插入
batchInsert(userList);

// ❌ 逐条插入
for (User user : userList) {
    insert(user);
}
```

### 单元测试
```java
@Test
public void testGetUserById_Success() {
    // Given
    Long userId = 1L;
    User expectedUser = new User(userId, "张三");
    when(userRepository.findById(userId)).thenReturn(Optional.of(expectedUser));
    
    // When
    User actualUser = userService.getUserById(userId);
    
    // Then
    assertNotNull(actualUser);
    assertEquals(expectedUser.getName(), actualUser.getName());
}

@Test
public void testGetUserById_NotFound() {
    // Given
    Long userId = 999L;
    when(userRepository.findById(userId)).thenReturn(Optional.empty());
    
    // When & Then
    assertThrows(NotFoundException.class, () -> {
        userService.getUserById(userId);
    });
}
```

## 日常工作流程

### 开发流程
1. **领取任务**：从项目管理工具领取任务
2. **需求理解**：仔细阅读需求和设计文档，有疑问及时沟通
3. **技术设计**：设计技术方案，必要时评审
4. **创建分支**：从develop创建feature分支
5. **编码实现**：按照规范编写代码
6. **单元测试**：编写单元测试，保证覆盖率
7. **自测**：本地自测功能和边界场景
8. **代码审查**：提交Code Review
9. **合并代码**：审查通过后合并到develop
10. **提测**：部署测试环境，提交测试

### 每日工作节奏
- **晨会（10分钟）**：同步昨日进展、今日计划、遇到的问题
- **专注开发（上午）**：核心开发时间，避免打扰
- **Code Review（午后）**：审查团队代码
- **问题解决（下午）**：处理测试反馈、线上问题
- **总结规划（傍晚）**：总结当日工作，规划明日任务

## Vibe Engineering实践

### 快速交付
- 采用敏捷开发，小步快跑
- 持续集成，频繁提交代码
- 自动化测试，快速反馈

### 质量第一
- 代码规范检查自动化
- 强制Code Review
- 单元测试覆盖率要求
- 性能测试和压测

### 持续改进
- 定期复盘，总结经验教训
- 技术分享，共同成长
- 重构优化，降低技术债务
- 学习新技术，保持竞争力

## 成长路径
1. **初级开发**：完成基础功能开发，代码质量合格
2. **中级开发**：独立负责模块开发，代码质量优秀
3. **高级开发**：技术攻坚，架构设计，技术引领
4. **技术专家**：领域专家，技术创新，影响力建设
