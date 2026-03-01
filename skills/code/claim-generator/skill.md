---
name: claim-generator
description: 报账单模块生成器
---
# Claim Module Generator (报账单模块生成器)

## 概述

此skill用于快速生成财务共享服务中心各类报账单模块的完整代码，包括Controller、Service、Mapper等所有层级的代码。

支持的模块类型：
- **TR模块** (claim-tr) - 资金类报账单
- **OTC模块** (claim-otc) - 订单到现金报账单  
- **PTP模块** (claim-ptp) - 采购到付款报账单
- **其他模块** - 可扩展支持

## 适用场景

当用户需要创建新的报账单模块时使用，例如：
- "创建TR模块的T014报账单"
- "生成OTC模块的T044完整代码"
- "创建PTP模块的新报账单T099"

## 功能特性

- ✅ 自动生成Controller层（Web层）
- ✅ 自动生成Service接口和实现（head、line、pay、bpm四个维度）
- ✅ 自动生成基础的Mapper、DTO、Converter
- ✅ 遵循项目分层架构规范
- ✅ 支持自定义业务描述
- ✅ 支持是否包含付款行（pay）功能
- ✅ 支持BPM流程回调功能

## 技术架构

报账单模块遵循以下分层结构：

```
claim-{module}-web/                     # Web层
  └── controller/claim/
      └── T{XXX}ClaimController.java    # Controller

claim-{module}-service/                 # Service层
  └── claim/t{xxx}/
      ├── head/                         # 报账单头服务
      │   ├── IT{XXX}NewClaimService.java
      │   ├── IT{XXX}LoadClaimService.java
      │   ├── IT{XXX}SaveClaimService.java
      │   ├── IT{XXX}DeleteClaimService.java
      │   └── impl/
      │       ├── T{XXX}NewClaimServiceImpl.java
      │       ├── T{XXX}LoadClaimServiceImpl.java
      │       ├── T{XXX}SaveClaimServiceImpl.java
      │       └── T{XXX}DeleteClaimServiceImpl.java
      ├── line/                         # 报账单明细行服务
      │   ├── IT{XXX}NewClaimLineService.java
      │   ├── IT{XXX}SaveClaimLineService.java
      │   ├── IT{XXX}UpdateClaimLineService.java
      │   ├── IT{XXX}DeleteClaimLineService.java
      │   └── impl/
      │       ├── T{XXX}NewClaimLineServiceImpl.java
      │       ├── T{XXX}SaveClaimLineServiceImpl.java
      │       ├── T{XXX}UpdateClaimLineServiceImpl.java
      │       └── T{XXX}DeleteClaimLineServiceImpl.java
      ├── pay/                          # 发票核销明细行服务（可选）
      │   ├── IT{XXX}NewClaimPayLineService.java
      │   ├── IT{XXX}SaveClaimPayLineService.java
      │   ├── IT{XXX}DeleteClaimPayLineService.java
      │   └── impl/
      │       ├── T{XXX}NewClaimPayLineServiceImpl.java
      │       ├── T{XXX}SaveClaimPayLineServiceImpl.java
      │       └── T{XXX}DeleteClaimPayLineServiceImpl.java
      └── bpm/                          # BPM流程回调服务
          ├── IT{XXX}CallBackClaimService.java
          ├── IT{XXX}SubmitClaimService.java
          └── impl/
              ├── T{XXX}CallBackClaimServiceImpl.java
              └── T{XXX}SubmitClaimServiceImpl.java
```

## 使用方式

### 基本用法

```bash
# 生成TR模块不包含付款行的报账单
/skill claim-generator tr T014 "资产采购报账单" "资金类报账"

# 生成OTC模块包含付款行的报账单
/skill claim-generator otc T065 "收入成本报账单" "订单到收款" --with-pay

# 生成PTP模块的报账单
/skill claim-generator ptp T099 "采购报账单" "采购到付款"
```

### 参数说明

1. **模块名称** (必填): claim模块名，如tr、otc、ptp等
2. **模板编号** (必填): 报账单的编号，如T014、T044、T065等
3. **业务描述** (必填): 报账单的业务说明，如"资产采购报账单"
4. **业务分类** (必填): 报账单所属业务大类
5. **--with-pay** (可选): 是否包含付款行功能，默认为false

### 生成示例

#### 示例1：生成TR模块的T014资产采购报账单

```
用户: /skill claim-generator tr T014 "资产采购报账单" "资金类报账"
```

生成的内容：
- Controller: `T014ClaimController.java`
- Head Services: IT014NewClaimService、IT014LoadClaimService等
- Line Services: IT014NewClaimLineService、IT014SaveClaimLineService等

#### 示例2：生成OTC模块的T065收入成本报账单（含付款行）

```
用户: /skill claim-generator otc T065 "收入成本报账单" "订单到收款" --with-pay
```

生成的内容：
- 包含示例1的所有内容
- Pay Services: IT065NewClaimPayLineService、IT065SaveClaimPayLineService等
- Controller中增加付款相关接口

## 代码模板规范

### Controller层规范

```java
@Slf4j
@RestController
@RequestMapping("T{XXX}")
@Tag(name = "(TR){业务分类}/{业务描述}(T{XXX})", description = "{业务描述}")
public class T{XXX}ClaimController {
    
    private final String itemId = ClaimTemplateEnum.T{XXX}.name();
    
    // 注入Head服务
    @Resource
    private IT{XXX}NewClaimService newClaimService;
    @Resource
    private IT{XXX}LoadClaimService loadClaimService;
    @Resource
    private IT{XXX}SaveClaimService saveClaimService;
    @Resource
    private IT{XXX}DeleteClaimService deleteClaimService;
    
    // 注入Line服务
    @Resource
    private IT{XXX}NewClaimLineService newClaimLineService;
    // ... 其他服务
    
    // 标准接口
    @Operation(summary = "新增-页面初始化", description = "新增-页面初始化")
    @PostMapping(value = "new")
    public TRmbsClaimPageDto newClaim(@Schema(hidden = true) UserObjectFullDto user) {
        Assert.notNull(user, "[(#{sys.auth.require.login})]");
        return newClaimService.newClaim(itemId, user);
    }
    
    // ... 其他接口
}
```

### Service接口规范

```java
/**
 * T{XXX}{业务描述}-{操作}服务接口
 */
public interface IT{XXX}{Operation}ClaimService extends IBase{Operation}ClaimService {
    // 通常为空接口，继承自Base接口
}
```

### Service实现规范

```java
/**
 * T{XXX}{业务描述}-{操作}服务实现
 * 
 * T{XXX}特点：
 * - {业务特点1}
 * - {业务特点2}
 */
@Slf4j
@Service
public class T{XXX}{Operation}ClaimServiceImpl 
    extends Base{Operation}ClaimService 
    implements IT{XXX}{Operation}ClaimService {

    @Override
    protected TRmbsClaimPageDto preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
        log.debug("T{XXX}{Operation}ClaimServiceImpl.preExecute开始");
        
        // 特定业务逻辑
        
        log.debug("T{XXX}{Operation}ClaimServiceImpl.preExecute完成");
        return claim;
    }
}
```

## 标准接口清单

### Head（报账单头）接口

| 接口路径 | 接口说明 | 请求方法 |
|---------|---------|---------|
| /T{XXX}/new | 新增-页面初始化 | POST |
| /T{XXX}/load | 报账单加载 | POST |
| /T{XXX}/save | 报账单保存 | POST |
| /T{XXX}/delete | 报账单删除 | POST |

### Line（明细行）接口

| 接口路径 | 接口说明 | 请求方法 |
|---------|---------|---------|
| /T{XXX}/newClaimLine | 明细行初始化 | POST |
| /T{XXX}/saveClaimLine | 明细行新增 | POST |
| /T{XXX}/updateClaimLine | 明细行修改 | POST |
| /T{XXX}/deleteClaimLine | 明细行删除 | POST |

### Pay（付款行）接口（可选）

| 接口路径 | 接口说明 | 请求方法 |
|---------|---------|---------|
| /T{XXX}/initPaylist | 计划付款初始化 | POST |
| /T{XXX}/newClaimPayLine | 发票核销明细行初始化 | POST |
| /T{XXX}/saveClaimPayLine | 发票核销明细行保存 | POST |
| /T{XXX}/deleteClaimPayLine | 发票核销明细行删除 | POST |

## 生成流程

1. **验证输入参数**
   - 检查模板编号格式（T+3位数字）
   - 验证业务描述不为空

2. **创建目录结构**
   - Web层目录：`claim-{module}-web/src/main/java/com/yili/claim/{module}/web/controller/claim/`
   - Service层目录：`claim-{module}-service/src/main/java/com/yili/claim/{module}/claim/t{xxx}/`

3. **生成Controller**
   - 根据是否包含付款行生成相应接口

4. **生成Head Services**
   - 接口：IT{XXX}NewClaimService、IT{XXX}LoadClaimService等
   - 实现：T{XXX}NewClaimServiceImpl、T{XXX}LoadClaimServiceImpl等

5. **生成Line Services**
   - 接口：IT{XXX}NewClaimLineService等
   - 实现：T{XXX}NewClaimLineServiceImpl等

6. **生成Pay Services**（如果指定--with-pay）
   - 接口：IT{XXX}NewClaimPayLineService等
   - 实现：T{XXX}NewClaimPayLineServiceImpl等

7. **生成BPM Services**（总是生成）
   - 接口：IT{XXX}CallBackClaimService, IT{XXX}SubmitClaimService
   - 实现：T{XXX}CallBackClaimServiceImpl, T{XXX}SubmitClaimServiceImpl

8. **更新枚举配置**
   - 在ClaimTemplateEnum中添加新模板

## 注意事项

1. **命名规范**
   - 所有T{XXX}必须保持大小写一致
   - 包名使用小写t{xxx}
   - 类名使用大写T{XXX}

2. **依赖关系**
   - Controller只能调用Service
   - Service继承自BaseService
   - 遵循项目分层架构

3. **必需的枚举配置**
   生成代码后需要在`ClaimTemplateEnum`中添加：
   ```java
   T{XXX}("{XXX}", "{业务描述}"),
   ```

4. **必需的Common层组件**
   确保已存在：
   - `TRmbsClaimPageDto` - 报账单页面DTO
   - `TRmbsClaimPageFullDto` - 报账单完整DTO
   - `TRmbsClaimLineDto` - 明细行DTO
   - `BaseNewClaimService` - 新建服务基类
   - `BaseLoadClaimService` - 加载服务基类
   - `BaseSaveClaimService` - 保存服务基类
   - `BaseDeleteClaimService` - 删除服务基类

## 扩展功能

生成基础代码后，可以在Service实现类中扩展以下功能：

1. **preExecute** - 执行前的数据初始化和验证
2. **postExecute** - 执行后的数据处理
3. **customValidation** - 自定义业务验证
4. **specialBusinessLogic** - 特殊业务逻辑

## 相关参考

- 项目规范：`/ai-spec/rules/agents.md`
- 现有模板：TR模块(T015、T065)、OTC模块、PTP模块
- 基类实现：`claim-common-service/src/main/java/com/yili/claim/common/service/claim/service/impl/`

---

## Skill实现说明

当AI接收到调用此skill的指令时，应执行以下步骤：

1. 解析参数（模板编号、业务描述、是否包含付款行）
2. 验证参数有效性
3. 按照上述模板生成所有必需的文件
4. 提示用户需要手动添加的配置（如枚举）
5. 确认所有文件已创建成功

生成的代码必须：
- ✅ 遵循阿里巴巴Java开发手册
- ✅ 使用Lombok注解
- ✅ 使用正确的包结构
- ✅ 包含完整的Javadoc注释
- ✅ 遵循项目分层架构
- ✅ 使用@Resource进行依赖注入

---

## 模板文件清单

已创建的模板文件：

### Controller层
- `templates/controller-template.java` - Controller模板

### Head层（报账单头）
- `templates/head/interface-new-template.java` - New接口模板
- `templates/head/impl-new-template.java` - New实现模板
- `templates/head/interface-load-template.java` - Load接口模板
- `templates/head/impl-load-template.java` - Load实现模板
- `templates/head/interface-save-template.java` - Save接口模板
- `templates/head/impl-save-template.java` - Save实现模板
- `templates/head/interface-delete-template.java` - Delete接口模板
- `templates/head/impl-delete-template.java` - Delete实现模板

### Line层（明细行）
- `templates/line/interface-new-template.java` - New接口模板
- `templates/line/impl-new-template.java` - New实现模板
- `templates/line/interface-save-template.java` - Save接口模板
- `templates/line/impl-save-template.java` - Save实现模板
- `templates/line/interface-update-template.java` - Update接口模板
- `templates/line/impl-update-template.java` - Update实现模板
- `templates/line/interface-delete-template.java` - Delete接口模板
- `templates/line/impl-delete-template.java` - Delete实现模板

### Pay层（付款行-可选）
- `templates/pay/interface-new-template.java` - New接口模板
- `templates/pay/impl-new-template.java` - New实现模板
- `templates/pay/interface-save-template.java` - Save接口模板
- `templates/pay/impl-save-template.java` - Save实现模板
- `templates/pay/interface-delete-template.java` - Delete接口模板
- `templates/pay/impl-delete-template.java` - Delete实现模板

### BPM层（流程回调）
- `templates/bpm/interface-callback-template.java` - CallBack接口模板
- `templates/bpm/impl-callback-template.java` - CallBack实现模板
- `templates/bpm/interface-submit-template.java` - Submit接口模板
- `templates/bpm/impl-submit-template.java` - Submit实现模板

## 模板变量说明

所有模板文件使用以下变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{module}}` | 模块名称（小写） | tr, otc, ptp |
| `{{moduleUpper}}` | 模块名称（大写） | TR, OTC, PTP |
| `{{templateNum}}` | 模板编号（大写） | 065 |
| `{{templateNumLower}}` | 模板编号（小写） | 065 |
| `{{businessDesc}}` | 业务描述 | 收入成本报账单 |
| `{{businessCategory}}` | 业务分类 | 订单到收款总账记账业务 |
| `{{author}}` | 作者名称 | sevenxiao |
| `{{date}}` | 创建日期 | 2025-02-26 |
| `{{feature1}}` | 业务特点1（可选） | - |
| `{{feature2}}` | 业务特点2（可选） | - |
| `{{withPay}}` | 是否包含付款行 | true/false |
