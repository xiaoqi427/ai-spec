# Transform Claim Service - 使用指南

## 快速开始

### 整体迁移T044（OTC模块）

```bash
/skill transform-claim otc T044 --md ./quests/T044-需求分析.md
```

AI将按顺序执行10个步骤，每步都会先分析老代码、陈述方案，等确认后再编写代码。

### 单步迁移T047的Save报账单头（步骤3）

```bash
/skill transform-claim otc T047 --step 3
```

---

## 迁移步骤速查表

| 步骤 | 功能 | 老代码 → 新代码 |
|------|------|----------------|
| 1 | New报账单头 | `NewT{XXX}ClaimService` → `T{XXX}NewClaimServiceImpl` |
| 2 | New报账单行 | `NewT{XXX}ClaimLineService` → `T{XXX}NewClaimLineServiceImpl` |
| 3 | Save报账单头 | `InsertT{XXX}ClaimService` + `UpdateT{XXX}ClaimService` → `T{XXX}SaveClaimServiceImpl` |
| 4 | Save报账单行 | `InsertT{XXX}ClaimLineService` + `UpdateT{XXX}ClaimLineService` → `T{XXX}SaveClaimLineServiceImpl` |
| 5 | Delete报账单头 | `DeleteT{XXX}ClaimService` → `T{XXX}DeleteClaimServiceImpl` |
| 6 | Delete报账单行 | `DeleteT{XXX}ClaimLinesService` → `T{XXX}DeleteClaimLineServiceImpl` |
| 7 | Load报账单 | `LoadAllT{XXX}Service` + `ViewT{XXX}*Service`(多个) → `T{XXX}LoadClaimServiceImpl` |
| 8 | CallBack | `CallBackT{XXX}Service` → `T{XXX}CallBackClaimServiceImpl` |
| 9 | Submit | `SubmitT{XXX}Service` → `T{XXX}SubmitClaimServiceImpl` |
| 10 | Load报账单行 | `ListAllT{XXX}ClaimLinesService` → `T{XXX}LoadClaimLineService` |

---

## 完整示例：迁移OTC模块T044

### 步骤1：New报账单头

**分析老代码** `NewT044ClaimService`，识别其中的业务逻辑：
- 初始化报账单头字段
- 设置默认值
- 用户信息填充

**对比新框架** `BaseNewClaimService`：
- 已有：用户信息初始化、通用字段设置
- 需重写：T044特有的默认值设置

**迁移结果**：
```java
@Slf4j
@Service
public class T044NewClaimServiceImpl extends BaseNewClaimService implements IT044NewClaimService {
    
    /**
     * T044新建报账单-预处理
     * 原代码对应: NewT044ClaimService.java 第30-65行
     */
    @Override
    protected TRmbsClaimPageDto preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
        log.debug("T044NewClaimServiceImpl.preExecute开始");
        // T044特有逻辑...
        log.debug("T044NewClaimServiceImpl.preExecute完成");
        return claim;
    }
}
```

### 步骤3：Save报账单头（Insert + Update 合并）

**分析老代码**：
- `InsertT044ClaimService` - 新增保存逻辑
- `UpdateT044ClaimService` - 修改保存逻辑

**合并策略**：在新的 `T044SaveClaimServiceImpl` 中，通过判断是新增还是修改来分流处理。

### 步骤7：Load报账单（多个Service合并）

**分析老代码**（需合并以下多个Service）：
- `LoadAllT044Service` - 加载全部
- `ViewT044ClaimService` - 查看报账单头
- `ViewT044ClaimLineService` - 查看报账单行
- `ViewT044ClaimBankReceiptOneVendorService` - 银行回单（单供应商）
- `ViewT044ClaimBankReceiptService` - 银行回单
- `ViewT044ClaimBankReceiptVendorService` - 银行回单（供应商）

**合并到** `T044LoadClaimServiceImpl`，在不同的hook方法中处理。

---

## 约束清单（Checklist）

每步迁移完成后，请对照以下清单确认：

- [ ] 不修改继承类的代码，需要变更请重写
- [ ] 存在父类逻辑直接调用，不重复实现
- [ ] 逻辑完整，没有遗漏老代码
- [ ] 抽离出的方法注释上写了原来代码对应行数
- [ ] 不存在的字段创建在DTO中，不在DO中
- [ ] 迁移后的代码没有编译错误
- [ ] 不对传入变量重新赋值
- [ ] MyBatis Plus能实现的没有手写SQL
- [ ] 单表查询使用了 `LambdaQueryWrapperX`
- [ ] 导入包写在文件头部，没有直接写在代码里

---

## 常见问题

### Q1: 老代码中的Insert和Update如何合并到Save？
**A**: 新框架的Save通过 `preExecute`/`postExecute` 钩子区分新增和修改。通常在 `preExecute` 中根据主键是否存在判断是新增还是修改，分别执行对应逻辑。

### Q2: Load步骤合并这么多Service，怎么组织代码？
**A**: 在 `T{XXX}LoadClaimServiceImpl` 中，将各个老Service的逻辑拆分到不同的方法中，通过 `preExecute`/`postExecute` 钩子串联。银行回单等扩展逻辑可以抽成私有方法。

### Q3: 老代码中用到的工具类找不到怎么办？
**A**: 先在 `claim-ptp`、`claim-eer`、`claim-otc`、`claim-base` 中搜索是否已有实现。`NumberToCNUtil` 已存在可直接使用。其他工具类需要确认是否已迁移。

### Q4: 老代码中有直接操作数据库的逻辑怎么处理？
**A**: 遵循新框架分层规范。将SQL操作迁移到对应的 DoService/Mapper 层，业务逻辑保留在Service实现类中。

### Q5: 什么时候需要创建新的DTO字段？
**A**: 当老代码中使用了新框架DO中不存在的字段时，需要在对应的DTO中创建该字段，绝不在DO中创建。
