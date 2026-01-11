# T047 测试类结构说明

## 📁 目录结构

```
t047/
├── T047ClaimControllerTestBase.java          # 基础测试类（公共 Mock 和工具方法）
├── T047TestDataFactory.java                  # 测试数据工厂（管理不同 item2_id 的数据）
├── T047ClaimController_047006_Test.java     # 047006 业务场景测试
└── README.md                                  # 本说明文档
```

## 🎯 设计原则

### 1. 测试类分离
- **每个业务场景（item2_id）一个独立的测试类**
- **不同业务场景之间完全解耦**
- **降低维护成本，便于扩展**

### 2. 代码复用
- **基础测试类**：包含所有 Service 的 Mock 声明和公共工具方法
- **测试数据工厂**：统一管理不同业务场景的测试数据配置
- **子类只需关注具体业务场景的测试逻辑**

## 📋 文件说明

### T047ClaimControllerTestBase.java
**职责**：
- 提供所有 Service 的 Mock 声明（所有子类共享）
- 提供 MockMvc 和 ObjectMapper 的初始化
- 提供公共工具方法（创建用户、执行请求等）

**使用方式**：
```java
class T047ClaimController_047006_Test extends T047ClaimControllerTestBase {
    // 只需实现具体业务场景的测试方法
}
```

### T047TestDataFactory.java
**职责**：
- 管理不同 item2_id 的测试数据配置
- 提供从 load 接口获取数据并创建模板的方法
- 支持扩展新的业务场景

**配置方式**：
```java
// 在 TEST_DATA_CONFIG 中添加新场景
TEST_DATA_CONFIG.put("047007", new TestDataConfig(16017570L, "047007", "描述"));
```

**使用方式**：
```java
// 获取配置
TestDataConfig config = T047TestDataFactory.getConfig("047006");

// 加载真实数据
TRmbsClaimPageFullDto loadedData = T047TestDataFactory.loadRealClaimData(
    config.getClaimId(), config.getItem2Id());

// 创建模板
TRmbsClaimPageDto template = T047TestDataFactory.createClaimTemplateFromLoaded(loadedData);
```

### T047ClaimController_047006_Test.java
**职责**：
- 针对 item2_id=047006 的业务场景进行完整测试
- 使用 claimId=16017569 的真实数据作为模板
- 包含报账单头、明细行、发票核销行的完整增删改测试

**测试覆盖**：
- ✅ 数据加载测试（从 load 接口获取真实数据）
- ✅ 报账单头操作（创建、修改、删除）
- ✅ 明细行操作（创建、修改、删除、初始化）
- ✅ 发票核销行操作（初始化、保存、删除）
- ✅ 完整业务流程测试
- ✅ 其他接口测试

## 🚀 如何添加新的业务场景测试

### 步骤 1：在测试数据工厂中添加配置
```java
// 在 T047TestDataFactory.java 的 TEST_DATA_CONFIG 中添加
TEST_DATA_CONFIG.put("047007", new TestDataConfig(
    16017570L,  // claimId
    "047007",   // item2Id
    "手工发票报账单-047007场景"  // description
));
```

### 步骤 2：创建新的测试类
```java
@DisplayName("T047ClaimController 测试 - 047007业务场景")
class T047ClaimController_047007_Test extends T047ClaimControllerTestBase {
    
    private static final String ITEM2_ID = "047007";
    private static final Long REAL_CLAIM_ID = 16017570L;
    
    // 实现具体的测试方法
}
```

### 步骤 3：复制并修改测试方法
- 从 `T047ClaimController_047006_Test.java` 复制测试方法
- 修改 `ITEM2_ID` 和 `REAL_CLAIM_ID` 常量
- 根据业务场景调整测试逻辑

## ✅ 测试运行

### 运行单个测试类
```bash
# 运行 047006 场景测试
mvn test -Dtest=T047ClaimController_047006_Test
```

### 运行所有 T047 测试
```bash
mvn test -Dtest=T047ClaimController_*_Test
```

### 运行特定测试方法
```bash
mvn test -Dtest=T047ClaimController_047006_Test#should_load_real_claim_data_successfully_for_047006
```

## 📝 注意事项

1. **测试数据来源**：
   - ✅ `loadRealClaimData` 方法已基于真实数据（claimId=16017569, item2_id=047006）创建测试对象
   - 数据来源：真实的 load 接口返回的 JSON 数据
   - 包含完整的报账单头信息和明细行信息
   - 未来如需更新数据，可直接修改 `T047TestDataFactory.loadRealClaimData` 方法

2. **测试独立性**：
   - 每个测试类完全独立，可以单独运行
   - 不同业务场景的测试互不影响

3. **扩展性**：
   - 新增业务场景只需添加配置和测试类
   - 不需要修改现有代码

4. **维护性**：
   - 公共代码在基础类中，修改一处即可影响所有子类
   - 业务场景特定的代码在各自的测试类中，互不干扰

## 🔄 未来扩展

当需要添加新的业务场景时：
1. 在 `T047TestDataFactory` 中添加配置
2. 创建新的测试类 `T047ClaimController_XXXXX_Test`
3. 实现该业务场景的测试方法
4. 无需修改现有测试类

这样的设计确保了：
- ✅ 测试类之间完全解耦
- ✅ 维护成本低
- ✅ 扩展性强
- ✅ 代码复用率高


