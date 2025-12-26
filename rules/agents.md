---
trigger: manual
---
# AGENTS.MD – AI 助手项目规则 (Qoder)

## 1. 目的与范围

本文档定义 AI 编码助手 (Qoder) 在 **fssc-config-service** 项目中的工作规范。

目标:

- 尊重现有的**架构**、**代码风格**和**依赖关系**
- 避免引入**不兼容的框架**或**不一致的模式**
- 以**安全**、**渐进**和**便于审查**的方式进行修改
- 严格遵守项目包结构规范和分层调用规则

适用范围:

- `fssc-config-service/` 下的所有模块
- 代码建议、重构、测试和配置变更

---

## 2. 项目概览

- **类型**: Java 21, Spring Boot 3, Maven 多模块项目
- **业务领域**: 财务共享服务中心 – 配置管理服务
- **主要模块**:
  - `fssc-config-do` – 数据实体层，只存放 entity DO 信息
  - `fssc-config-api-param` – 存放 API 需要的 DTO 和 Converter
  - `fssc-config-api` – 存放外部需要用到的 Feign API 接口
  - `fssc-config-service` – 业务逻辑层，包含 business、service、mapper
  - `fssc-config-web` – Web 层，包含 Controller 和配置

当不确定代码应该放在哪里时，**严格遵循下述模块职责和包结构规范**。

---

### 3. 技术栈与依赖规则

### 3.1 核心技术栈

1. **Java 版本**: Java 21 (必须)
2. **构建工具**: Maven 3.9.6
3. **Spring 框架**:
   - Spring Boot 3 + 注解驱动（全面消除 XML 配置）
   - Spring Cloud
4. **数据访问**:
   - MyBatis Plus (主要使用)
   - 单表查询可以使用注解和接口默认实现
   - 多表查询禁止使用注解，只能通过配置 XML
5. **中间件**: Redis, MySQL, RabbitMQ (如需要)
6. **代码规范工具**: Spotless + Google Java Format
7. **静态分析**: SonarLint + Alibaba Java Guidelines
8. **测试框架**: JUnit 5 + Mockito + AssertJ
9. **AST 工具**: Lombok (强制使用)
10. **对象转换**: MapStruct (禁止使用任何反射相关的对象克隆和复制)

### 3.2 依赖管理规则

1. **不要引入新的主要框架** (例如新的 DI 框架、Web 框架或 ORM)，除非用户明确要求
2. **复用现有的 common 模块**:
   - `fssc-common-util`, `fssc-common-db`, `fssc-common-redis`, `fssc-common-mq` 等
3. 如果某个库在本项目中尚未使用，**默认不要添加**。请先向用户提出建议
4. **版本管理**: 所有依赖版本由 `fssc-parent` 统一管理

---

## 4. 架构与分层约定

### 4.1 模块包结构规范

项目采用严格的分层架构，模块结构如下：

```
com.yili.{model}
├── web/              # Web层相关代码 (Controller)
├── service/          # business、service、mapper 存放目录
├── api-param/        # 存放 API 需要的 DTO 和 Converter
├── api/              # 存放外部需要用到本 model 的 Feign API 接口
└── do/               # 只存放 entity DO 信息
```

### 4.2 分层结构与职责

项目严格遵循以下分层结构：

```
HTTP Request → Controller → Business → DO Service → Mapper → Database
```

#### 4.2.1 Controller 层
**位置**: `{model}-web/src/main/java/com/yili/{model}/web/controller`

**职责**:
- 接收和处理 HTTP 请求
- 参数验证和绑定
- 身份认证和权限检查
- 调用 Business 层并返回响应
- 统一异常处理

**严格规则**:
- ✅ Controller 只能调用 Business 层
- ❌ 禁止直接调用 Service 或 Mapper 层
- ❌ 禁止包含业务逻辑
- ❌ 禁止跨层调用
- ❌ 禁止反向调用

#### 4.2.2 Business 层（业务逻辑层）
**位置**: `{model}-service/src/main/java/com/yili/{model}/{功能模块}/business`

**职责**:
- 核心业务逻辑处理
- 业务流程编排和协调
- 复杂的业务规则验证
- 事务边界管理
- 调用多个 DO Service 完成复杂业务场景

**使用条件**:
- 当且仅当只有增删改的简单业务可以不用此层
- 复杂业务逻辑必须在此层实现
- 跨领域业务规则在此层处理

**严格规则**:
- ✅ Business 层可以调用多个 DO Service 层
- ✅ Business 层可以调用平层 Business
- ❌ 禁止跨层调用
- ❌ 禁止反向调用

#### 4.2.3 Service 层（DO Service）
**位置**: `{model}-service/src/main/java/com/yili/{model}/{功能模块}/service`

**命名规范**: `I{Name}DoService` (接口)、`{Name}DoServiceImpl` (实现)

**职责**:
- 与 Mapper 交互
- 数据持久化操作的封装
- 多个带不同参数的操作可以拆分成多个方法

**严格规则** (⚠️ 强制执行):
- ❌ **不允许写任何 business 逻辑**
- ❌ **不允许写任何 SQL**
- ❌ **不允许写任何 if 相关代码**
- ✅ **只写一切与 mapper 相关的交互**
- ✅ **DO Service 层只能调用 Mapper 层**
- ✅ **多个带不同参数的可以拆分成多个方法**
- ✅ **或由 business 来承接复杂逻辑**

#### 4.2.4 Mapper 层（数据访问层）
**位置**: `{model}-service/src/main/java/com/yili/{model}/{功能模块}/mapper`

**职责**:
- 数据库 CRUD 操作
- SQL 实现
- 数据持久化相关操作
- 仅包含数据访问逻辑

**严格规则**:
- ✅ 单表可以用注解接口默认实现
- ❌ 多表不允许直接使用注解，只能通过配置 XML
- ✅ Mapper 层只能操作 DO

#### 4.2.5 DO 层（Entity）
**位置**: `{model}-do/src/main/java/com/yili/{model}/DO`

**职责**:
- 与数据库表映射
- 定义数据结构和约束
- 基本的 MyBatis Plus 注解
- 不包含任何业务逻辑

**命名规范**: `{Name}Do`

#### 4.2.6 DTO 层规范
**位置**: `{model}-api-param/src/main/java/com/yili/{model}/api/param/dto`

**职责**:
- 所有和数据库对象无关的数据传输对象
- 包括和前端交互的对象
- 统一取名 DTO

**Converter 层**:
**位置**: `{model}-api-param/src/main/java/com/yili/{model}/api/param/converter`

**职责**:
- 负责 DO ↔ DTO 转换
- 尽量用 `org.mapstruct.Mapper`
- ❌ 禁止使用任何反射相关的对象克隆和复制

### 4.3 层间调用关系检查清单

**Controller 层检查**:
- [ ] 只调用 Business 层
- [ ] 没有业务逻辑
- [ ] 没有直接调用 Service 或 Mapper

**Business 层检查**:
- [ ] 包含完整的业务流程
- [ ] 处理复杂的业务规则
- [ ] 合理的事务管理
- [ ] 适当的异常处理

**DO Service 层检查** (⚠️ 必须严格执行):
- [ ] 没有 business 逻辑
- [ ] 没有 SQL 语句
- [ ] 没有 if 相关代码
- [ ] 只调用 mapper 方法
- [ ] 方法命名清晰明确

**Mapper 层检查**:
- [ ] 单表查询使用注解（可选）
- [ ] 多表查询使用 XML 配置
- [ ] 只操作 DO 对象

**Converter 层检查**:
- [ ] 使用 MapStruct 而非反射
- [ ] 明确的转换方法定义
- [ ] 支持批量转换

### 4.4 新代码应该放在哪里

- **新的 DO (实体)** → `{model}-do/src/main/java/com/yili/{model}/DO`
- **新的 DTO** → `{model}-api-param/src/main/java/com/yili/{model}/api/param/dto`
- **新的 Converter** → `{model}-api-param/src/main/java/com/yili/{model}/api/param/converter`
- **新的 Feign API 接口** → `{model}-api/src/main/java/com/yili/{model}/api/feign`
- **新的 Mapper** → `{model}-service/src/main/java/com/yili/{model}/{功能模块}/mapper`
- **新的 DO Service** → `{model}-service/src/main/java/com/yili/{model}/{功能模块}/service`
- **新的 Business** → `{model}-service/src/main/java/com/yili/{model}/{功能模块}/business`
- **新的 Controller** → `{model}-web/src/main/java/com/yili/{model}/web/controller`

**功能模块命名示例**: `common`, `item`, `acpt`, `asset`, `project`, `tax` 等业务域

---

## 5. 编码规范 (阿里巴巴 Java 开发手册)

**重要**: 本项目严格遵守《阿里巴巴 Java 开发手册》，所有新增代码必须符合以下规范。

### 5.1 命名规范

#### 5.1.1 命名风格

1. **类名**: 使用 UpperCamelCase 风格，必须遵从驼峰形式
   ```java
   // ✅ 正确
   public class ClaimService {}
   public class UserOrderDTO {}
   
   // ❌ 错误
   public class claimservice {}
   public class user_order_dto {}
   ```

2. **方法名、参数名、成员变量、局部变量**: 使用 lowerCamelCase 风格
   ```java
   // ✅ 正确
   private String userName;
   public void getUserInfo() {}
   
   // ❌ 错误
   private String user_name;
   public void get_user_info() {}
   ```

3. **常量命名**: 全部大写，单词间用下划线隔开
   ```java
   // ✅ 正确
   public static final int MAX_STOCK_COUNT = 50;
   public static final String DEFAULT_ENCODING = "UTF-8";
   
   // ❌ 错误
   public static final int maxStockCount = 50;
   ```

4. **抽象类命名**: 使用 Abstract 或 Base 开头
   ```java
   public abstract class AbstractClaimService {}
   public abstract class BaseController {}
   ```

5. **异常类命名**: 使用 Exception 结尾
   ```java
   public class BusinessException extends RuntimeException {}
   public class DataNotFoundException extends Exception {}
   ```

6. **测试类命名**: 以被测试类的名称开始，以 Test 结尾
   ```java
   public class ClaimServiceTest {}
   ```

#### 5.1.2 项目特定命名约定

**保持与现有代码一致**:
- Service 接口: `I{Name}Service` (例如 `IExportService`)
- Service 实现: `{Name}ServiceImpl`
- DAO 接口: `I{Name}Dao`
- 实体: `T{Name}` (与现有命名保持一致)
- 参数/DTO: `{Name}RequestParam`, `{Name}ResponseParam`

---

### 5.2 常量定义规范

1. **不允许任何魔法值** (即未经预先定义的常量) 直接出现在代码中
   ```java
   // ❌ 错误 - 魔法值
   if (type == 1) {
       // 1 代表什么?
   }
   
   // ✅ 正确 - 使用常量
   public static final int CLAIM_TYPE_EXPENSE = 1;
   if (type == CLAIM_TYPE_EXPENSE) {
       // 清晰明了
   }
   
   // ✅ 更好 - 使用枚举
   public enum ClaimType {
       EXPENSE(1, "费用报销"),
       ASSET(2, "资产采购");
       
       private final int code;
       private final String desc;
       // ...
   }
   ```

2. **long 或 Long 赋值时，数值后使用大写 L**
   ```java
   // ✅ 正确
   Long value = 2L;
   
   // ❌ 错误 - 小写 l 容易与数字 1 混淆
   Long value = 2l;
   ```

---

### 5.3 代码格式规范

1. **大括号使用约定**:
   - 左大括号前不换行，左大括号后换行
   - 右大括号前换行，右大括号后还有 else 等代码则不换行
   ```java
   // ✅ 正确
   if (condition) {
       // code
   } else {
       // code
   }
   
   // ❌ 错误
   if (condition)
   {
       // code
   }
   else {
       // code
   }
   ```

2. **单行字符数限制不超过 120 个**，超出需要换行
   - 运算符与下文一起换行
   - 方法调用的点符号与下文一起换行
   ```java
   // ✅ 正确
   String result = "very long string " + 
                   "continue here";
   
   userService
       .findById(userId)
       .map(User::getName)
       .orElse("Unknown");
   ```

3. **IDE 的 text file encoding 设置为 UTF-8**

4. **IDE 中文件的换行符使用 Unix 格式**，不要使用 Windows 格式

---

### 5.4 OOP 规范

1. **避免通过一个类的对象引用访问此类的静态变量或静态方法**
   ```java
   // ❌ 错误
   ClaimService service = new ClaimService();
   String result = service.staticMethod();
   
   // ✅ 正确
   String result = ClaimService.staticMethod();
   ```

2. **所有覆写方法，必须加 @Override 注解**
   ```java
   @Override
   public String toString() {
       return "ClaimInfo";
   }
   ```

3. **相同参数类型，相同业务含义，才可以使用 Java 的可变参数**
   ```java
   // ✅ 正确
   public void saveUsers(User... users) {}
   
   // ❌ 错误 - 参数含义不同
   public void process(Object... params) {}
   ```

4. **外部正在调用或者二方库依赖的接口，不允许修改方法签名**，避免对接口调用方产生影响

---

### 5.5 集合处理规范

1. **关于 hashCode 和 equals 的处理**:
   - 只要覆写 equals，就必须覆写 hashCode
   - Set 存储的对象、Map 的键对象，必须覆写这两个方法

2. **ArrayList 的 subList 结果不可强转成 ArrayList**
   ```java
   // ❌ 错误
   ArrayList<String> subList = (ArrayList<String>) list.subList(0, 10);
   
   // ✅ 正确
   List<String> subList = list.subList(0, 10);
   ```

3. **使用集合转数组的方法，必须使用集合的 toArray(T[] array)**
   ```java
   // ✅ 正确
   String[] array = list.toArray(new String[0]);
   
   // ❌ 错误
   String[] array = (String[]) list.toArray();
   ```

4. **不要在 foreach 循环里进行元素的 remove/add 操作**
   ```java
   // ❌ 错误 - 会抛出 ConcurrentModificationException
   for (String item : list) {
       if (condition) {
           list.remove(item);
       }
   }
   
   // ✅ 正确 - 使用 Iterator
   Iterator<String> iterator = list.iterator();
   while (iterator.hasNext()) {
       String item = iterator.next();
       if (condition) {
           iterator.remove();
       }
   }
   
   // ✅ 更好 - 使用 removeIf
   list.removeIf(item -> condition);
   ```

5. **集合初始化时，指定集合初始值大小**
   ```java
   // ✅ 正确 - 避免扩容
   Map<String, String> map = new HashMap<>(16);
   List<String> list = new ArrayList<>(10);
   ```

---

### 5.6 并发处理规范

1. **线程资源必须通过线程池提供，不允许在应用中自行显式创建线程**
   ```java
   // ❌ 错误
   new Thread(() -> {
       // task
   }).start();
   
   // ✅ 正确 - 使用线程池
   @Autowired
   private ThreadPoolExecutor executor;
   
   executor.execute(() -> {
       // task
   });
   ```

2. **SimpleDateFormat 是线程不安全的类**，一般不要定义为 static 变量
   ```java
   // ❌ 错误
   private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
   
   // ✅ 正确 - 使用 Java 8 的 DateTimeFormatter
   private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
   
   // ✅ 或使用项目工具类
   import com.au.sa.fssc.common.util.lang.DateUtil;
   String dateStr = DateUtil.format(date, "yyyy-MM-dd");
   ```

3. **必须回收自定义的 ThreadLocal 变量**
   ```java
   try {
       threadLocal.set(value);
       // business logic
   } finally {
       threadLocal.remove();
   }
   ```

---

### 5.7 控制语句规范

1. **在一个 switch 块内，每个 case 要么通过 break/return 等来终止，要么注释说明程序将继续执行到哪一个 case 为止**
   ```java
   switch (status) {
       case PENDING:
           process();
           break;
       case APPROVED:
           approve();
           // fall through
       case COMPLETED:
           complete();
           break;
       default:
           throw new IllegalArgumentException();
   }
   ```

2. **在 if/else/for/while/do 语句中必须使用大括号**
   ```java
   // ❌ 错误
   if (condition)
       doSomething();
   
   // ✅ 正确
   if (condition) {
       doSomething();
   }
   ```

3. **表达异常的分支时，少用 if-else 方式**，使用卫语句（guard clauses）
   ```java
   // ❌ 不推荐
   public void process(String data) {
       if (data != null) {
           if (data.length() > 0) {
               // 业务逻辑
           }
       }
   }
   
   // ✅ 推荐 - 使用卫语句
   public void process(String data) {
       if (data == null) {
           return;
       }
       if (data.length() == 0) {
           return;
       }
       // 业务逻辑
   }
   ```

4. **除常用方法（如 getXxx/isXxx）等外，不要在条件判断中执行其他复杂的语句**
   ```java
   // ❌ 错误
   if (calculateComplexValue() > 10) {}
   
   // ✅ 正确
   int value = calculateComplexValue();
   if (value > 10) {}
   ```

---

### 5.8 注释规范

1. **类、类属性、类方法的注释必须使用 Javadoc 规范**
   ```java
   /**
    * 报账单服务实现
    *
    * @author zhangsan
    * @since 2025-12-11
    */
   @Service
   public class ClaimServiceImpl implements IClaimService {
       
       /**
        * 根据报账单号查询报账单信息
        *
        * @param claimNo 报账单号
        * @return 报账单信息
        * @throws BusinessException 当报账单不存在时
        */
       @Override
       public Claim findByClaimNo(String claimNo) {
           // implementation
       }
   }
   ```

2. **所有的抽象方法（包括接口中的方法）必须用 Javadoc 注释**

3. **方法内部单行注释，在被注释语句上方另起一行，使用 // 注释**

4. **所有的枚举类型字段必须要有注释，说明每个数据项的用途**
   ```java
   public enum ClaimStatus {
       /** 草稿 */
       DRAFT(0),
       /** 待审批 */
       PENDING(1),
       /** 已通过 */
       APPROVED(2);
   }
   ```

5. **代码修改的同时，注释也要进行相应的修改**，特别是参数、返回值、异常、核心逻辑等

---

### 5.9 其他规范

1. **在使用正则表达式时，利用好其预编译功能**
   ```java
   // ✅ 正确 - 预编译
   private static final Pattern PATTERN = Pattern.compile("[a-zA-Z0-9]+");
   
   public boolean validate(String input) {
       return PATTERN.matcher(input).matches();
   }
   ```

2. **velocity 调用 POJO 类的属性时，直接使用属性名取值即可**

3. **后台输送给页面的变量必须加 $!{var}**，中间的感叹号

4. **注意 Math.random() 返回的是 double 类型**，范围 0 ≤ x < 1

5. **获取当前毫秒数使用 System.currentTimeMillis()**，而不是 new Date().getTime()

---

### 5.10 异常处理规范

1. **Java 类库中定义的可以通过预检查方式规避的 RuntimeException 异常不应该通过 catch 的方式来处理**
   ```java
   // ❌ 错误
   try {
       obj.method();
   } catch (NullPointerException e) {}
   
   // ✅ 正确
   if (obj != null) {
       obj.method();
   }
   ```

2. **异常不要用来做流程控制，条件控制**

3. **catch 时请分清稳定代码和非稳定代码**，稳定代码指的是无论如何不会出错的代码

4. **捕获异常是为了处理它，不要捕获了却什么都不处理而抛弃之**
   ```java
   // ❌ 错误 - 吞掉异常
   try {
       process();
   } catch (Exception e) {
       // 什么也不做
   }
   
   // ✅ 正确 - 记录日志并处理
   try {
       process();
   } catch (Exception e) {
       log.error("处理失败", e);
       throw new BusinessException("处理失败", e);
   }
   ```

5. **有 try 块放到了事务代码中，catch 异常后，如果需要回滚事务，一定要注意手动回滚事务**

6. **finally 块必须对资源对象、流对象进行关闭**，或使用 try-with-resources

7. **不要在 finally 块中使用 return**

---

### 5.11 MySQL 数据库规范

1. **表达是与否概念的字段，必须使用 is_xxx 的方式命名**，数据类型是 unsigned tinyint (1 表示是，0 表示否)

2. **表名、字段名必须使用小写字母或数字**，禁止出现数字开头，禁止两个下划线中间只出现数字

3. **表名不使用复数名词**

4. **禁用保留字**，如 desc、range、match、delayed 等

5. **小数类型为 decimal，禁止使用 float 和 double**
   - float 和 double 存在精度损失问题
   - decimal(M,D) 中 M 表示总位数，D 表示小数位数

6. **如果存储的字符串长度几乎相等，使用 char 定长字符串类型**

7. **varchar 是可变长字符串，不预先分配存储空间**，长度不要超过 5000

8. **表必备三字段: id, create_time, update_time**
   - id: 主键，类型为 bigint unsigned，单表时自增
   - create_time: 创建时间，类型为 datetime
   - update_time: 更新时间，类型为 datetime

---

### 5.12 Spring 与注解

1. **注解**:
   - 使用 Spring 标准注解: `@RestController`, `@Controller`, `@Service`, `@Repository`, `@Component`
   - 依赖注入使用 `@Autowired` 或 `@Resource`，与周围代码保持一致
   
2. **Lombok**:
   - 如果目标包中已经使用 Lombok，允许建议使用 Lombok 注解 (`@Data`, `@Slf4j` 等)
   - 不要在尚未使用 Lombok 的包/模块中引入 Lombok，除非获得明确批准
   
3. **@Transactional 注解**:
   - 在 Service 层使用，不要在 Controller 层使用
   - 明确指定 rollbackFor = Exception.class
   ```java
   @Transactional(rollbackFor = Exception.class)
   public void createClaim(ClaimRequest request) {
       // business logic
   }
   ```

---

## 6. Spring 与配置约定

### 6.1 注解使用规范

1. **Spring 标准注解**:
   - 使用 `@RestController`, `@Controller`, `@Service`, `@Repository`, `@Component`
   - 依赖注入使用 `@Autowired` 或 `@Resource`，与周围代码保持一致
   
2. **Lombok 注解** (强制使用):
   - 必须使用 Lombok 注解：`@Data`, `@Slf4j`, `@Getter`, `@Setter`, `@NoArgsConstructor`, `@AllArgsConstructor` 等
   - 所有新代码都必须使用 Lombok
   - DO 类使用 `@Data` 注解
   - 需要日志的类使用 `@Slf4j` 注解
   
3. **@Transactional 注解**:
   - 在 Business 层使用，不要在 Controller 层使用
   - 明确指定 `rollbackFor = Exception.class`
   ```java
   @Transactional(rollbackFor = Exception.class)
   public void createConfig(ConfigRequest request) {
       // business logic
   }
   ```

### 6.2 Profile 与配置

1. **Profile 设置**:
   - 尊重现有的 profile 设置
   - `application.yml` + `application-{env}.yml`
   - 不要硬编码环境特定的值；使用配置和现有的属性模式
   
2. **异步与 MQ**:
   - 使用现有的异步执行器和 MQ 配置
   - 除非必要，不要创建新的线程池
   
3. **事务**:
   - 在 Business 方法上使用 `@Transactional`，不要在 Controller 上使用
   - 遵循同一模块/包中现有的事务传播和回滚策略

---

## 7. API 设计与错误处理

### 7.1 REST API 规范

1. **REST API**:
   - 在类级别使用 `@Controller` 或 `@RestController` + `@RequestMapping`
   - 在方法级别使用 HTTP 方法注解 (`@GetMapping`, `@PostMapping` 等)
   - 使用 `{model}-api-param` 中的 DTO 作为请求/响应负载
   - 请求参数使用 `@RequestBody`, `@PathVariable`, `@RequestParam` 等
   
2. **Swagger / OpenAPI**:
   - 使用 `io.swagger.v3.oas.annotations` (不是 v2)
   - 类级别：`@Schema(description = "...")`
   - 方法级别：`@Operation(summary = "...")`
   - 参数级别：`@Parameter(description = "...")`
   
### 7.2 错误处理

1. **异常处理**:
   - 优先复用现有的异常类型和全局处理器
   - 不要引入新的全局异常模式，除非先查看现有模式
   
2. **返回类型**:
   - 使用 `Result<T>` 统一包装返回结果
   - 使用 `Page<T>` 返回分页数据

---

## 8. 日志与监控

### 8.1 日志规范

1. **日志框架**: 使用 SLF4J + Logback
2. **Lombok 日志**: 必须使用 **Lombok `@Slf4j`** 注解
   ```java
   @Slf4j
   @Service
   public class ConfigServiceImpl {
       public void process() {
           log.info("处理开始");
           log.error("处理失败", e);
       }
   }
   ```
   
3. **日志级别**:
   - `info` 用于正常业务流程
   - `debug` 用于详细诊断
   - `warn` 用于潜在问题
   - `error` 仅用于真正的错误/异常
   
4. **性能考虑**:
   - 不要在性能敏感的代码路径中添加过多日志 (大结果集的循环、高频任务)
   
5. **日志内容**:
   - 不要使用 `System.out.println`
   - 必须过滤敏感信息（密码、Token 等）

---

## 9. 测试约定

1. 使用现有的测试设置 (JUnit, Spring Boot test)
2. 将测试放在相应的 `src/test/java/...` 包中，镜像主包结构
3. 优先编写**小型、专注**的测试，围绕新增或修改的行为，除非必要否则避免大型集成测试

---

## 10. 重构与向后兼容

### 10.1 重构原则

1. **不要**更改公共方法签名或明显被其他服务使用的 Feign API，除非:
   - 有明确的用户请求，并且
   - 你概述了影响和迁移步骤
   
2. **重构时**:
   - 优先进行**小型、渐进式**重构
   - 保持行为不变，除非任务明确要求改变行为
   
3. **业务规则**:
   - 保留现有的业务规则，除非明确指示更改
   - 特别是那些在配置中编码的规则

### 10.2 API 兼容性

1. **Feign API 接口**:
   - 不要修改已有的接口签名
   - 增加新接口时需要考虑向下兼容
   
2. **DTO 结构**:
   - 增加字段时使用默认值或可选
   - 不要删除已有字段，除非确认没有使用

---

## 11. Qoder 应该如何工作

### 11.1 基本原则

1. **始终**:
   - 简要解释**为什么**建议某个更改 (业务或技术原因)
   - 遵循周围代码的风格和模式
   - 使用现有的工具和模块，而不是重新实现类似的逻辑
   - **严格遵守分层调用规则**
   
2. **添加或修改代码时**:
   - 仅显示**必要的最小差异**，在需要时使用 `// ... existing code ...` 占位符
   - 避免引入新的横切模式 (自定义 AOP、新的全局拦截器)，除非明确要求
   - **确保代码放在正确的层级和模块中**
   
3. **不确定时**:
   - 优先询问用户以确认设计决策 (例如新模块、新依赖、新公共 API)
   - 优先采用不会破坏现有行为的保守方法

### 11.2 代码生成规范

1. **分层检查**:
   - 生成 Controller 时，确保只调用 Business 层
   - 生成 Business 时，确保调用 DO Service 层
   - 生成 DO Service 时，确保只调用 Mapper 层
   - **绝对不要跨层调用或反向调用**
   
2. **代码质量**:
   - 必须使用 Lombok 注解
   - 必须使用 MapStruct 进行对象转换
   - 禁止使用反射进行对象复制
   - 禁止在 DO Service 中写 if 逻辑、SQL 或业务逻辑
   
3. **命名规范**:
   - DO: `{Name}Do`
   - DTO: `{Name}Dto`
   - Converter: `{Name}DtoConverter`
   - DO Service Interface: `I{Name}DoService`
   - DO Service Impl: `{Name}DoServiceImpl`
   - Business Service: `{Name}Service` 或 `{Name}BusinessService`
   - Mapper: `{Name}DoMapper`
   - Controller: `{Name}Controller`

---

# 12. 不要做的事情

### 12.1 架构层面

- ❌ 不要在没有明确用户请求的情况下引入新的主要框架或基础设施组件
- ❌ 不要仅为了"风格"原因而重写系统的大部分内容
- ❌ 不要在没有明确指示的情况下更改业务关键常量、代码或配置键
- ❌ 不要创建新的文档文件 (`*.md`, `*.txt`, README 等)，除非用户明确要求

### 12.2 代码层面

- ❌ 不要跨层调用 (Controller 直接调用 Mapper)
- ❌ 不要反向调用 (Mapper 调用 Service)
- ❌ 不要在 DO Service 中写 if 逻辑、SQL 或业务逻辑
- ❌ 不要使用反射进行对象复制，必须使用 MapStruct
- ❌ 不要在新代码中不使用 Lombok
- ❌ 不要硬编码敏感信息 (密码、Token、密钥等)

### 12.3 规范层面

- ❌ 不要违反阿里巴巴 Java 开发手册规范
- ❌ 不要使用 `System.out.println`，必须使用 `@Slf4j`
- ❌ 不要在日志中输出敏感信息
- ❌ 不要修改已有的 Feign API 接口签名

---

## 13. 开发流程规范

### 13.1 开发前准备

**工具链要求**:
- JDK: Java 21 (必须)
- Maven: 3.9.6+
- IDE: IntelliJ IDEA (推荐)
- 插件: Lombok Plugin, MapStruct Support

**开发前 Checklist**:
- [ ] 我已明确本次功能的需求和验收标准
- [ ] 我已确认代码应该放在哪个模块和包中
- [ ] 我已确认分层调用关系正确
- [ ] 我已确认本地环境 Java 21 正确性

### 13.2 开发中规范

**开发中 Checklist**:
- [ ] 我使用小步提交，每步可运行、可测试
- [ ] 我写了单元测试（至少一个正向 + 一个异常 case）
- [ ] 我使用 `@Slf4j` 日志，不使用 `System.out.println`
- [ ] 我使用 Lombok 注解，不手写 getter/setter
- [ ] 我使用 MapStruct 转换，不使用反射复制
- [ ] 我处理了空值、异常边界情况
- [ ] 我没有在 DO Service 中写 if/SQL/业务逻辑
- [ ] 我没有跨层或反向调用

### 13.3 开发后检查

**开发后 Checklist**:
- [ ] 所有测试通过（`mvn test`）
- [ ] 运行 `mvn spotless:apply` 格式化代码
- [ ] 查看 SonarLint 有无新问题
- [ ] 确认分层调用关系正确
- [ ] 确认使用了 Lombok 和 MapStruct
- [ ] 确认没有硬编码敏感信息
- [ ] 提交代码并写清晰的 Commit Message
- [ ] 推送到远程仓库并确认 CI 全绿

---

## 14. 项目特定规范

### 14.1 MyBatis 使用规范

1. **Mapper 接口**:
   - 继承 `com.baomidou.mybatisplus.core.mapper.BaseMapper<DO>`
   - 单表查询可以使用注解或默认方法
   - 多表查询必须使用 XML 配置
   
2. **XML 配置位置**:
   - `{model}-service/src/main/resources/mapper/com/yili/{model}/...`
   
3. **分页查询**:
   - 使用 `com.baomidou.mybatisplus.extension.plugins.pagination.Page`
   - 使用 `PageParam<DTO, DO>` 封装分页参数

### 14.2 对象转换规范

1. **MapStruct Converter**:
   ```java
   @Mapper(componentModel = "spring")
   public interface ConfigDtoConverter {
       ConfigDtoConverter INSTANCE = Mappers.getMapper(ConfigDtoConverter.class);
       
       ConfigDto toDto(ConfigDo configDo);
       
       ConfigDo toDo(ConfigDto configDto);
       
       List<ConfigDto> toDtoList(List<ConfigDo> configDoList);
   }
   ```
   
2. **禁止使用**:
   - ❌ `BeanUtils.copyProperties` (使用反射)
   - ❌ `PropertyUtils.copyProperties` (使用反射)
   - ❌ 任何基于反射的对象复制工具
   
3. **转换位置**:
   - Controller → Business: DTO 直接传递
   - Business → DO Service: DTO 转 DO (使用 Converter)
   - DO Service → Business: DO 转 DTO (使用 Converter)
   - Business → Controller: DTO 直接返回

### 14.3 异常处理规范

1. **全局异常处理器**:
   - 使用 `@RestControllerAdvice` 统一处理异常
   - 返回统一的 `Result<T>` 结构
   
2. **业务异常**:
   - 使用自定义业务异常 `BusinessException`
   - 在 Business 层抛出，在全局处理器捕获
   
3. **日志记录**:
   - 异常必须记录日志 `log.error("错误信息", e)`
   - 不要吞掉异常

---

## 15. 附录

### 15.1 常用工具类位置

- 日期工具: `com.yili.common.util.*` (使用项目通用工具类)
- 分页请求: `com.yili.common.db.mybatis.pojo.PageParam`
- 统一返回: `com.yili.fssc.util.pojo.Result`
- Spring 上下文: `org.springframework.context.ApplicationContext`

使用这些现有工具类而不是引入新的工具库。

### 15.2 分层调用关系图

```
HTTP Request
    ↓
┌────────────────────────┐
│   Controller 层         │  ❌ 禁止直接调用 Service/Mapper
│  (@Controller/@Rest)    │  ❌ 禁止包含业务逻辑
└────────────────────────┘
    ↓ 只调用
┌────────────────────────┐
│   Business 层          │  ✅ 业务逻辑处理
│  (@Service/@Component)  │  ✅ 事务管理
│                        │  ✅ 调用多个 DO Service
│                        │  ✅ 可调用平层 Business
└────────────────────────┘
    ↓ 只调用
┌────────────────────────┐
│   DO Service 层        │  ❌ 禁止业务逻辑
│  (@Service)            │  ❌ 禁止 SQL
│                        │  ❌ 禁止 if 逻辑
│                        │  ✅ 只与 Mapper 交互
└────────────────────────┘
    ↓ 只调用
┌────────────────────────┐
│   Mapper 层            │  ✅ CRUD 操作
│  (@Mapper)             │  ✅ SQL 实现
│                        │  ✅ 单表用注解
│                        │  ✅ 多表用 XML
└────────────────────────┘
    ↓
Database (DO 对象)
```

### 15.3 模块结构示例

```
fssc-config-service/
├── fssc-config-do/                    # DO 层
│   └── src/main/java/com/yili/config/
│       ├── common/DO/                  # 通用 DO
│       ├── item/DO/                    # 项目 DO
│       └── acpt/DO/                    # 承兑 DO
│
├── fssc-config-api-param/             # DTO 和 Converter 层
│   └── src/main/java/com/yili/config/api/param/
│       ├── common/
│       │   ├── dto/                    # DTO
│       │   └── converter/              # MapStruct Converter
│       ├── item/
│       └── acpt/
│
├── fssc-config-api/                   # Feign API 层
│   └── src/main/java/com/yili/config/api/feign/
│       ├── item/
│       └── acpt/
│
├── fssc-config-service/               # 业务逻辑层
│   └── src/main/java/com/yili/config/
│       ├── common/
│       │   ├── business/           # Business 层
│       │   ├── service/            # DO Service 层
│       │   └── mapper/             # Mapper 层
│       ├── item/
│       └── acpt/
│
└── fssc-config-web/                   # Web 层
    └── src/main/java/com/yili/config/web/
        └── controller/                # Controller 层
            ├── common/
            ├── item/
            └── acpt/
```

### 15.4 快速参考

**关键原则**:
1. ✅ 必须使用 Java 21
2. ✅ 必须使用 Lombok
3. ✅ 必须使用 MapStruct
4. ❌ 禁止跨层调用
5. ❌ 禁止反向调用
6. ❌ DO Service 禁止 if/SQL/业务逻辑
7. ❌ 禁止使用反射复制对象
8. ❌ 禁止硬编码敏感信息

**分层调用**:
- Controller → Business
- Business → DO Service + 平层 Business
- DO Service → Mapper
- Mapper → Database

**命名模式**:
- DO: `XxxDo`
- DTO: `XxxDto`
- Converter: `XxxDtoConverter`
- Service: `IXxxDoService` / `XxxDoServiceImpl`
- Mapper: `XxxDoMapper`
- Controller: `XxxController`

---

## 总结

本文档是 **fssc-config-service** 项目的 AI 助手工作规范。所有 Qoder AI 助手在生成代码、重构代码或提供建议时，必须严格遵守以下核心原则：

1. **分层架构强制执行**: 绝对不允许跨层或反向调用
2. **DO Service 纯洁性**: 绝对不允许包含 if/SQL/业务逻辑
3. **技术栈限制**: 必须使用 Java 21 + Lombok + MapStruct
4. **安全规范**: 绝对不允许硬编码敏感信息
5. **代码质量**: 严格遵守阿里巴巴 Java 开发手册

遵守这些规则可以确保代码质量、可维护性和团队协作效率。
