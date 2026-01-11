# T047 Load 接口返回参数格式说明

## 📋 接口信息

**接口路径**: `POST /T047/load`

**返回类型**: `TRmbsClaimPageFullDto`

**说明**: 返回报账单的完整信息，包括主表、明细行、付款计划、附件等所有相关数据

---

## 📦 返回数据结构

### 顶层结构

```java
TRmbsClaimPageFullDto {
    // 基本信息
    Long claimId;                    // 报账单ID
    String claimNo;                  // 报账单编号
    String itemId;                   // 模板ID (如: "T047")
    String item2Id;                  // 业务大类ID (如: "047006")
    
    // 核心数据
    TRmbsClaimPageDto claim;         // 报账单头（主表信息）
    TRmbsClaimLinePageDto claimLine; // 明细行信息
    TRmbsPaylistPageDto paylist;     // 付款计划行
    TRmbsClaimRelPageDto claimRel;   // 借款核销行
    
    // 其他信息
    TRmbsClaimPageDto oldClaim;      // 旧报账单信息（用于对比）
    List<TRmbsClaimPageDto> assClaims; // 级联报账单列表
    TRmbsTemplateDto template;       // 模板信息
    EimImageFullDto eimImage;        // 电子影像信息
    TCoItemLevel2Dto itemLevel2;     // 大类信息
    TCoItemLevel3Dto itemLevel3Dto;  // 小类信息
    CmContractDto cmContract;        // 合同信息
    
    // 附件和流程
    List<TAttachmentDto> attachments; // 附件列表
    List<TProcessWiRecordDto> processWiRecords; // 流程记录
    TProcessWiRecordDto curProcessWiRecords;    // 当前流程环节
    
    // 其他页签（根据业务类型不同）
    TRmbsClaimBankPageDto claimBankPage; // 承兑汇票页签
    TClaimInvoiceRelationAllSumDto tax;  // 税金信息
    TBlackListResultDto black;           // 黑名单信息
    // ... 更多字段
}
```

---

## 🔍 主要字段详解

### 1. claim (报账单头)

**类型**: `TRmbsClaimPageDto`

**说明**: 报账单头信息，包含报账单的所有主表字段

**主要字段**:

```java
{
    // 基本信息
    Long claimId;                    // 报账单ID
    String claimNo;                  // 报账单编号
    String itemId;                   // 模板ID
    String item2Id;                  // 业务大类ID
    String status;                   // 状态 (如: "0" 表示草稿)
    String processState;             // 流程状态 (如: "起草人")
    
    // 金额信息
    BigDecimal applyAmount;          // 申请金额
    BigDecimal valueAddedTaxAmount;  // 增值税税额
    BigDecimal adjustPayAmount;     // 调整后付款金额
    BigDecimal sumAmount;            // 合计金额
    BigDecimal payAmount;            // 付款金额
    
    // 申请人信息
    Long applyUserId;                // 申请人ID
    String applyUserName;            // 申请人姓名
    Long applyDeptId;                // 申请部门ID
    String applyDeptName;            // 申请部门名称
    Long expenseIssuerId;            // 费用发生人ID
    String expenseIssuerName;        // 费用发生人姓名
    
    // 组织信息
    Long compId;                     // 公司ID
    Long orgId;                      // 组织ID
    String orgName;                  // 组织名称
    String coSegCode;                // 公司段编码
    String coSeg;                    // 公司段名称
    String buSegCode;                // 事业部段编码
    String buSeg;                    // 事业部段名称
    
    // 供应商信息
    Long vendorClientId;             // 供应商ID
    String vendorNo;                // 供应商编号
    String vendorName;               // 供应商名称
    
    // 其他信息
    String currency;                 // 币种 (如: "CNY")
    BigDecimal exchangeRate;         // 汇率
    String remark;                   // 备注
    // ... 更多字段
}
```

### 2. claimLine (明细行信息)

**类型**: `TRmbsClaimLinePageDto`

**结构**:

```java
{
    List<TRmbsClaimLineDto> lines;   // 明细行列表（行数据）
    BigDecimal amount;               // 总计
    BigDecimal adjustAmount;         // 调整总计
    BigDecimal loanAmount;            // 借-贷金额
    BigDecimal foreignApplyAmountTotal; // 外币报销金额合计
}
```

**说明**: 
- `lines`: 明细行列表，包含所有明细行数据
- 每个元素 `TRmbsClaimLineDto` 代表一条明细行

**明细行对象 (TRmbsClaimLineDto) 主要字段**:

**说明**: 每个 `TRmbsClaimLineDto` 对象代表一条明细行

```java
{
    // 基本信息
    Long claimLineId;                // 明细行ID
    Long claimId;                    // 报账单ID
    BigDecimal applyAmount;          // 申请金额
    BigDecimal adjustAmount;         // 调整金额
    BigDecimal payAmount;            // 付款金额
    
    // 物料信息
    String materialNo;                // 物料编码
    String materialName;             // 物料名称
    String taxCode;                  // 税码
    String uomCode;                  // 单位编码
    Long inventoryItemId;            // 库存物料ID
    Integer quantityT047;            // 数量
    BigDecimal price;                // 单价
    
    // 段值信息
    String costSegCode;              // 成本中心段编码
    String costSeg;                  // 成本中心段名称
    String buSegCode;                // 事业部段编码
    String buSeg;                    // 事业部段名称
    String brVal;                    // 借方8段值
    String brName;                   // 借方8段名称
    String crVal;                    // 贷方8段值
    String crName;                   // 贷方8段名称
    
    // 其他信息
    String currency;                 // 币种
    BigDecimal exchangeRate;         // 汇率
    String dcType;                   // 借贷类型 ("借方" 或 "贷方")
    // ... 更多字段
}
```

### 3. paylist (付款计划行)

**类型**: `TRmbsPaylistPageDto`

**结构**:

```java
{
    List<TRmbsPaylistDto> lines;    // 付款计划行列表（行数据）
    Boolean hasZeroPayAmount;        // 是否有零付款金额
    BigDecimal payListPayAmount;     // 付款计划金额合计
    Integer vendorListSize;          // 供应商列表数量
}
```

**说明**: 
- `lines`: 付款计划行列表，包含所有付款计划行数据

### 4. claimRel (借款核销行)

**类型**: `TRmbsClaimRelPageDto`

**结构**:

```java
{
    List<TRmbsClaimRelDto> lines;   // 借款核销行列表（行数据）
    BigDecimal relAmount;            // 核销金额合计
    String claimRelType;             // 核销类型
}
```

**说明**: 
- `lines`: 借款核销行列表，包含所有借款核销行数据

### 5. attachments (附件列表)

**类型**: `List<TAttachmentDto>`

**附件对象主要字段**:

```java
{
    Long attachId;                   // 附件ID
    Long claimId;                    // 报账单ID
    String attachName;               // 附件名称
    String attachPath;               // 附件路径
    String createDate;               // 创建时间
    String createUserName;           // 创建人姓名
}
```

---

## 📊 真实数据示例

基于 `claimId=16017569, item2_id=047006` 的真实数据：

```json
{
    "claimId": 16017569,
    "claimNo": "22010025102504700003",
    "itemId": "T047",
    "item2Id": "047006",
    "claim": {
        "claimId": 16017569,
        "claimNo": "22010025102504700003",
        "itemId": "T047",
        "item2Id": "047006",
        "applyAmount": 1151833.03,
        "valueAddedTaxAmount": 0,
        "adjustPayAmount": 0,
        "sumAmount": 0,
        "currency": "CNY",
        "exchangeRate": 1,
        "applyUserId": 1012335,
        "applyUserName": "张颖",
        "applyDeptId": 10140,
        "applyDeptName": "液态奶事业部浙沪营销总部营销财务",
        "orgId": 102,
        "orgName": "220100_OU_内蒙古伊利实业集团股份有限公司液态奶事业部",
        "buSegCode": "02",
        "buSeg": "液态奶事业部",
        "status": "0",
        "processState": "起草人",
        "remark": "收到液态奶事业部浙沪营销总部营销财务张颖提报补录发票（业务财务提单）",
        // ... 更多字段
    },
    "claimLine": {
        "lines": [
            {
                "claimLineId": 54001717,
                "claimId": 16017569,
                "applyAmount": 1151833.03,
                "adjustAmount": 0,
                "materialNo": "20D101000300",
                "materialName": "1*10*200g利乐冠安慕希常温酸奶黄桃燕麦味",
                "taxCode": "VAT13产品",
                "costSegCode": "4202259100",
                "costSeg": "液奶浙沪营销财务-不分明细",
                "buSegCode": "02",
                "buSeg": "液态奶事业部",
                "brVal": "220100.02.4202259100.0.0.0.0.0",
                "crVal": "220100.02.0.0.0.0.0.0",
                "dcType": "贷方",
                // ... 更多字段
            }
        ],
        "amount": 0,
        "adjustAmount": 0,
        "loanAmount": 1151833.03,
        "foreignApplyAmountTotal": 0
    },
    "paylist": {
        "lines": [],
        "hasZeroPayAmount": null,
        "payListPayAmount": 0,
        "vendorListSize": 0
    },
    "claimRel": {
        "lines": [],
        "relAmount": 0,
        "claimRelType": "1"
    },
    "attachments": [
        {
            "attachId": 46107581,
            "claimId": 16017569,
            "attachName": "上海光誉贸易有限公司-撤销流程.pdf",
            "attachPath": "/data/server/appfiles_use/attachment/2025/10/comp_1001/RMB_1761362694739.pdf",
            "createDate": "2025-10-25 11:24:54",
            "createUserName": "张颖"
        }
    ],
    "itemLevel2": {
        "itemId": "047006",
        "itemName": "补录发票（业务财务提单）",
        "description": "业务财务提单在应收模块做发票调整业务",
        // ... 更多字段
    },
    // ... 更多字段
}
```

---

## 🔑 关键字段说明

### 金额相关字段

- `applyAmount`: 申请金额（发票金额）
- `valueAddedTaxAmount`: 增值税税额
- `adjustPayAmount`: 调整后付款金额
- `sumAmount`: 合计金额（报账金额）
- `payAmount`: 付款金额

### 状态相关字段

- `status`: 报账单状态
  - `"0"`: 草稿
  - `"1"`: 待审批
  - `"2"`: 已通过
  - 等等
- `processState`: 流程状态（如: "起草人", "初核财务" 等）

### 段值相关字段

- `coSegCode` / `coSeg`: 公司段编码/名称
- `buSegCode` / `buSeg`: 事业部段编码/名称
- `costSegCode` / `costSeg`: 成本中心段编码/名称
- `brVal` / `brName`: 借方8段值/名称
- `crVal` / `crName`: 贷方8段值/名称

### 明细行相关字段

- `claimLineId`: 明细行ID（注意：不是 `lineId`）
- `dcType`: 借贷类型（"借方" 或 "贷方"）
- `materialNo` / `materialName`: 物料编码/名称
- `adjustAmount`: 调整金额

---

## 💡 使用建议

1. **获取报账单头信息**: 使用 `claim` 对象（报账单头/主表）
2. **获取明细行列表**: 使用 `claimLine.lines`（明细行数据列表）
3. **获取付款计划行列表**: 使用 `paylist.lines`（付款计划行数据列表）
4. **获取借款核销行列表**: 使用 `claimRel.lines`（借款核销行数据列表）
5. **获取附件列表**: 使用 `attachments`
6. **获取流程信息**: 使用 `processWiRecords` 或 `curProcessWiRecords`

---

## 📝 注意事项

1. **字段命名**: 
   - 明细行ID字段是 `claimLineId`，不是 `lineId`
   - `lines` 是行数据列表，包含多条行记录
2. **空值处理**: 某些字段可能为 `null`，需要做空值判断
3. **列表字段**: 
   - `claimLine.lines` - 明细行列表（可能为空列表）
   - `paylist.lines` - 付款计划行列表（可能为空列表）
   - `claimRel.lines` - 借款核销行列表（可能为空列表）
   - `attachments` - 附件列表（可能为空列表）
   - 使用前需要判断列表是否为空
4. **金额精度**: 金额字段使用 `BigDecimal` 类型，注意精度处理
5. **日期格式**: 日期字段格式为 `"yyyy-MM-dd HH:mm:ss"`

---

## 🔗 相关类定义

- `TRmbsClaimPageFullDto`: 完整报账单DTO
- `TRmbsClaimPageDto`: 报账单主表DTO
- `TRmbsClaimLinePageDto`: 明细行页DTO
- `TRmbsClaimLineDto`: 明细行DTO
- `TRmbsPaylistPageDto`: 付款计划页DTO
- `TRmbsClaimRelPageDto`: 借款核销页DTO

