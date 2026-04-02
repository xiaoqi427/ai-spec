# 老代码目录结构映射

## 根目录

```
yldc-caiwugongxiangpingtai-fsscYR-master/
├── src/com/ibm/gbs/efinance/              # Java 后端源码
│   ├── business/ylService/claim/          # 报账单业务逻辑
│   │   ├── T001/                          # 差旅报账单
│   │   ├── T010/                          # 采购报账单
│   │   ├── T044/                          # 杂项采购报账单
│   │   ├── T045/                          # 物流报账单
│   │   ├── T047/                          # 费用报账单
│   │   ├── T048/                          # 费用报账单(另一种)
│   │   ├── T049/                          # 杂项报账单
│   │   ├── T051/                          # 税单报账
│   │   ├── T052/                          # 税单报账(另一种)
│   │   ├── T060/                          # 应收报账
│   │   ├── T061-T069/                     # 资产类报账
│   │   ├── T065/                          # 差旅报账(特殊)
│   │   ├── T071/                          # 规则引擎
│   │   └── base/                          # 基类
│   │       ├── BaseNewClaimService.java
│   │       ├── BaseSaveOrUpdateClaimService.java
│   │       ├── BaseDeleteClaimService.java
│   │       ├── BaseLoadClaimService.java
│   │       ├── BaseCallBackClaimService.java
│   │       └── BaseSubmitClaimService.java
│   ├── dao/                               # 数据访问层
│   └── util/                              # 工具类
├── WebRoot/                               # 前端资源
│   ├── newPages/efinance/claim/           # JSP 页面
│   │   ├── T001/
│   │   ├── T044/
│   │   └── ...
│   ├── easjs/                             # JS 脚本
│   └── css/                               # 样式文件
└── WEB-INF/
    └── config/                            # 配置文件
```

## 报账单模板编号 → 模块映射

| 模板编号范围 | 业务模块 | 说明 |
|-------------|---------|------|
| T001-T009 | TR (差旅) | 差旅报账 |
| T010-T019 | PTP (采购) | 采购报账 |
| T040-T046 | OTC (杂项) | 杂项报账 |
| T047-T050 | EER (费用) | 费用报账 |
| T051-T059 | OTC (杂项) | 税单相关 |
| T060-T060 | RTR (应收) | 应收报账 |
| T061-T069 | FA (资产) | 资产报账 |
| T065 | TR (差旅) | 差旅特殊 |
| T071 | BASE (基础) | 规则引擎 |

## 每个模板目录下的标准文件

```
T{XXX}/
├── NewT{XXX}ClaimService.java              # 新建报账单头
├── NewT{XXX}ClaimLineService.java          # 新建报账单行
├── InsertT{XXX}ClaimService.java           # 保存(新增)报账单头
├── UpdateT{XXX}ClaimService.java           # 保存(更新)报账单头
├── InsertT{XXX}ClaimLineService.java       # 保存(新增)报账单行
├── UpdateT{XXX}ClaimLineService.java       # 保存(更新)报账单行
├── DeleteT{XXX}ClaimService.java           # 删除报账单头
├── DeleteT{XXX}ClaimLinesService.java      # 删除报账单行
├── LoadAllT{XXX}Service.java               # 加载报账单
├── ViewT{XXX}ClaimService.java             # 查看报账单头
├── ViewT{XXX}ClaimLineService.java         # 查看报账单行
├── CallBackT{XXX}Service.java              # 审批回调
├── SubmitT{XXX}Service.java                # 提交审批
├── ListAllT{XXX}ClaimLinesService.java     # 加载行列表
└── [可选] gd/GdXxxT{XXX}Service.java      # gd前缀文件 (不迁移)
```

## 快速定位技巧

- 用模板编号直接搜索目录: `find . -type d -name "T044"`
- 用关键词搜索方法: `grep -r "validateAmount" yldc-*/src/`
- gd 前缀的文件不需要迁移，可以忽略
- 已注释的代码块不需要迁移，但建议标注
