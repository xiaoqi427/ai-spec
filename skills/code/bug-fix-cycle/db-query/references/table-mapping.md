# 业务表映射参考

> 从项目 DO 实体类的 `@TableName` 注解提取，用于 db-query 快速定位要查哪个表。

## 核心业务表（报账单相关）

| 表名 | 说明 | 常用查询字段 | 索引字段 |
|------|------|------------|---------|
| T_RMBS_CLAIM | 报账单主表 | CLAIM_NO, TEMPLATE_ID, STATUS, TOTAL_AMOUNT, CREATOR | CLAIM_NO, TEMPLATE_ID, CREATOR |
| T_RMBS_CLAIM_ITEM | 报账单行明细 | CLAIM_NO, LINE_NO, ITEM_CODE, AMOUNT | CLAIM_NO |
| T_RMBS_PAYLIST | 支付单表 | PAYLIST_NO, CLAIM_NO, PAY_STATUS, PAY_AMOUNT | PAYLIST_NO, CLAIM_NO |
| T_RMBS_TEMPLATE | 模板表 | TEMPLATE_ID, TEMPLATE_NAME, STATUS | TEMPLATE_ID |

## 配置服务 (fssc-config-service)

### 会计项目

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_CO_ITEMLEVEL2 | TCoItemlevel2Do | 会计项目二级表 |
| T_CO_ITEMLEVEL3 | TCoItemlevel3Do | 会计项目三级表 |
| T_CO_ITEMLEVEL3_MUTI | TCoItemlevel3MutiDo | 会计项目三级多类型表 |
| T_CO_ITEMLEVEL3_MUTI_T020 | TCoItemlevel3MutiT020Do | 会计项目三级多类型T020表 |
| T_CO_ITEMLEVEL3_T020 | TCoItemlevel3T020Do | 会计项目三级T020表 |
| T_CO_ITEML3_CONF | TCoIteml3ConfDo | 会计项目三级配置表 |
| T_CO_ITEMLEVEL3_OU | TCoItemlevel3OuDo | 会计项目三级组织表 |
| T_CO_ITEM2_DEPTCOST | TCoItem2DeptcostDo | 会计项目二级部门成本表 |
| T_ITEM3_ACC | TItem3AccDo | 会计项目三级账户表 |

### 账务团队

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_PROC_ACCOUNTANTTEAM | AccountantTeamDo | 账务团队(会计分组)表 |
| T_PROC_ACCOUNTANTTEAM_ITEM | TProcAccountantteamItemDo | 账务团队项目表 |
| T_PROC_ACCOUNTANTTEAM_USER | TProcAccountantteamUserDo | 账务团队用户(座席)表 |

### 业务账户与配置

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_PROC_BIZ_ACCOUNT | TProcBizAccountDo | 业务账户表 |
| T_MIS_EXCHANGE_RATE | TMisExchangeRateDo | 汇率表 |
| T_AP_PROJECT_T020_CONF | TApProjectT020ConfDo | AP项目T020配置表 |
| T_CAC_TASK | TCacTaskDo | CAC任务表 |
| T_GL_AUTO_SETTLEMENT_CONDITION | TGlAutoSettlementConditionDo | 总账自动结算条件表 |

### 接受验收

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_ACPT_ROLE_CONFIG | TAcptRoleConfigDo | 接受角色配置表 |
| T_ACPT_DISPATCH_RULE | TAcptDispatchRuleDo | 接受分配规则表 |
| T_ACPT_VENDOR_RATE_CFG | TAcptVendorRateCfgDo | 接受供应商费率配置表 |
| T_ACPT_VENDOR_BANK_CFG | TAcptVendorBankCfgDo | 接受供应商银行配置表 |
| T_ACPT_VENDOR_AMOUNT_CFG | TAcptVendorAmountCfgDo | 接受供应商金额配置表 |

### 其他配置

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_QUY_AR_RECEIPT_REMARK | TQuyArReceiptRemarkDo | 应收收据备注表 |
| T_RMBS_HRDEP_ROLE_OU | TRmbsHrdepRoleOuDo | 人力资源部门角色组织表 |
| T_RMBS_HRDEP_ROLE_MAP | TRmbsHrdepRoleMapDo | 人力资源部门角色映射表 |

## 报账服务 (fssc-claim-service)

### OTC 相关 (claim-otc)

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_QUY_AR_AMT_REMAIN | TQuyArAmtRemainDo | 应收金额余额表 |
| T_QUY_AR_AMT_MARGIN | TQuyArAmtMarginDo | 应收金额差额表 |
| T_QUY_AR_RECEIVCE_PAYMENT | TQuyArReceivePaymentDo | 应收收款支付表 |
| T_AR_AMT_REMAIN_CONFIG | TArAmtRemainConfigDo | 应收金额余额配置表 |
| T_QUY_AR_AMT_REMAIN_TR_NEW | TQuyArAmtRemainTrNewDo | 应收金额余额转账新表 |
| T_OTC_ITEM3_PRODUCT_CONFIG | TOtcItem3ProductConfigDo | OTC第三级产品配置表 |
| T_OTC_INVOICE_RATE_CONFIG | TOtcInvoiceRateConfigDo | OTC发票费率配置表 |
| T_MANUAL_INVOICE_CONF | TManualInvoiceConfDo | 手动发票配置表 |
| T_QUY_INV_UOM_CODE | QuyInvUomCodeDo | 发票单位代码表 |
| T_QUY_RA_CUST_TRX_TYPE | QuyRaCustTrxTypeDo | 应收客户交易类型表 |
| T_RMBS_RECEIPT_SUB_INFO | ReceiptSubInfoDo | 收据分项信息表 |
| T_RMBS_RECEIPT_SUB_VENDOR_INFO | ReceiptSubVendorInfoDo | 收据分项供应商信息表 |
| T_RETURN_REMAIN_ITEM2_CONFIG | ReturnRemainItem2ConfigDo | 返回余额二级项目配置表 |
| T_RMBS_OTCSUBMISSIONAREA | TRmbsOtcsubmissionareaDo | OTC提交区域表 |

### TR 相关 (claim-tr)

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_CLAIM_T064_T065_T066 | ClaimT064T065T066Do | 差旅报销T064-T065-T066表 |

### BASE 相关 (claim-base)

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_PROC_PROVINCE_BIZDEPT_058 | TProcProvinceBizdept058Do | 报销业务部门058表 |
| T_PROC_PROVINCE_BIZDEPT_058SRC | TProcProvinceBizdept058srcDo | 报销业务部门058源表 |
| T_PROC_DEPT_DIRECTOR_058 | TProcDeptDirector058Do | 报销部门主管058表 |
| T_PROC_DEPT_DIRECTOR_058_SRC | TProcDeptDirector058SrcDo | 报销部门主管058源表 |
| T_PROC_DIRECTOR_058 | TProcDirector058Do | 报销主管058表 |
| T_PROC_DIRECTOR_058_SOURCE | TProcDirector058SourceDo | 报销主管058源表 |
| T_PROC_BIZ_ACCOUNT_058 | TProcBizAccount058Do | 报销业务账户058表 |
| T_PROC_BIZ_ACCOUNT_058_SOURCE | TProcBizAccount058SourceDo | 报销业务账户058源表 |
| T_CO_ITEMLEVEL2_058 | TCoItemlevel2058Do | 报销会计项目二级058表 |
| T_CO_ITEMLEVEL2_058_SOURCE | TCoItemlevel2058SourceDo | 报销会计项目二级058源表 |

## 公共服务 (fssc-common-service)

### 系统管理

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| SYS_USER | SysUserDo | 系统用户表 |
| SYS_ROLE | SysRoleDo | 系统角色表 |
| SYS_USER_ROLE | SysUserRoleDo | 系统用户角色表 |
| SYS_FUNCTION | SysFunctionDo | 系统功能表 |
| SYS_ROLEFUNC | SysRolefuncDo | 系统角色功能表 |
| SYS_GROUP | SysGroupDo | 系统组表 |
| SYS_USER_GROUP | SysUserGroupDo | 系统用户组表 |
| SYS_TENANT | SysTenantDo | 系统租户表 |
| SYS_TENANT_GROUP | SysTenantGroupDo | 系统租户组表 |
| SYS_OU_BU_SEG | SysOuBuSegDo | 系统组织业务单位分段表 |

### 字典与参数

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_DICT | TRmbsDictDo | 字典表 |
| T_I18N_MESSAGE | TI18nMessageDo | 国际化消息表 |
| T_SYS_PARAMETER | TSysParameterDo | 系统参数表 |
| T_CO_COMSEGCODE | TCoComSegCodeDo | 会计通用分段编码表 |
| TOTAL_OU | TotalOuDo | 总体组织表 |
| T_SYS_ALL_LOGIN_LOG | TSysAllLoginLogDo | 系统登录日志表 |

## 资金服务 (fssc-fund-service)

### 支付管理

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_PAYLIST_DELEGATION | FundRmbsPaylistDelegationDo | 支付单委托表 |
| T_RMBS_PAYLIST_FAULT | TRmbsPaylistFaultDo | 支付单故障表 |
| T_RMBS_PAYLIST_FOREIGNTURNLOG | TRmbsPaylistForeignturnlogDo | 支付单外币转账日志表 |
| T_RMBS_LC_LINE | TRmbsLcLineDo | 信用证额度行表 |
| IS_FREEZE_PAYMENTLIST | IsFreezePaymentlistDo | 冻结支付单表 |
| DELAY_PAYMENT_PAYLIST | DelayPaymentPaylistDo | 延迟支付单表 |

### 自动审计

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_AUTO_AUDIT_CONFIG | TAutoAuditConfigDo | 自动审计配置表 |
| T_AUTO_AUDIT_BASE | TAutoAuditBaseDo | 自动审计基础表 |
| T_AUTO_AUDIT_LOG | TAutoAuditLogDo | 自动审计日志表 |
| T_AUTO_AUDIT_RECONCILIATION | TAutoAuditReconciliationDo | 自动审计对账表 |
| T_AUTO_AUDIT_FUNDS_BANK | TAutoAuditFundsBankDo | 自动审计资金银行表 |
| T_AUTO_AUDIT_CBS_BANK | TAutoAuditCbsBankDo | 自动审计CBS银行表 |
| T_AUTO_AUDIT_ERP_BANK | TAutoAuditErpBankDo | 自动审计ERP银行表 |

### 账户流水

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_FUND_ACCOUNT_TRANS_FLOW | TFundAccountTransFlowDo | 账户交易流水表 |
| T_FUND_ACCOUNT_TRANS_FLOW_TMP | TFundAccountTransFlowTmpDo | 账户交易流水临时表 |
| T_FUND_ACCOUNT_TRANS_LOCK | TFundAccountTransLockDo | 账户交易锁定表 |
| T_FUND_ACCOUNT_TRANS_HANDLELOG | TFundAccountTransHandlelogDo | 账户交易处理日志表 |
| T_FUND_HR_APPOVE_LOG | TFundHrAppoveLogDo | 人力资源审批日志表 |

## 集成服务 (fssc-integration-service)

### 接受账单

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_ACPT_BILL | TAcptBillDo | 接受账单表 |
| T_ACPT_BILL_LINE_FRONT | TAcptBillLineFrontDo | 接受账单行前端表 |
| T_ACPT_BILL_LINE_BACK | TAcptBillLineBack | 接受账单行后端表 |

### 固定资产

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_FA_ASSETS_COST_INFO | TFaAssetsCostInfoDo | 固定资产成本信息表 |
| T_FA_ASSETS_DEPRN_INFO | TFaAssetsDeprnInfoDo | 固定资产折旧信息表 |

### 发票

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_QUY_INVITEMINFO_SUBSET | TQuyInviteminfoSubsetDo | 发票项目信息子集表 |
| T_QUY_INV_ITEM_INFO_BAK | TQuyInvItemInfoBakDo | 发票项目信息备份表 |
| BW_IINVOICE_LIB_ORIGIN | BwIinvoiceLibOriginDo | BI发票库源表 |

### 凭证

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_PAYMENT_VOUCHER | TPaymentVoucherDo | 支付凭证表 |
| T_CUSTOMS_CLEARANCE_VOUCHER | TCustomsClearanceVoucherDo | 海关清关凭证表 |
| T_VOUCHER_SPILIT | TVoucherSpilitDo | 凭证分割表 |

### 其他集成

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_FUNDS_TRANSFER_CLAIM_JOB | TFundsTransferClaimJobDo | 资金转账报销单任务表 |
| T_DIRECTORY_VENDOR_CONFIG | TDirectoryVendorConfigDo | 目录供应商配置表 |
| T_SYS_ERP_PARAM | TSysErpParamDo | 系统ERP参数表 |
| T_QUY_AR_RECEIPT_ACTIVITY | TQuyArReceiptActivityDo | 应收收据活动表 |
| T_RMBS_PO_AGRI_PRO_CONFIG | TRmbsPoAgriProConfigDo | 采购农业产品配置表 |
| T_RMBS_CUSTOMER_STALE | TRmbsCustomerStaleDo | 客户陈旧数据表 |
| T_AUTOARCHIVE_USER | TAutoarchiveUserDo | 自动归档用户表 |
| BW_ASYNC_RECORDS | BwAsyncRecordsDo | BI异步记录表 |
| T_FUND_ACCOUNTS | TFundAccountsDo | 资金账户表 |
| TPM_CX_EXEC_EMP_INT | TpmCxExecEmpIntDo | 项目管理执行员工集成表 |
| INTERFACE_LOG | InterfaceLogDo | 接口日志表 |

## 快速查表指南

根据 Bug 类型快速定位要查哪个表:

| Bug 场景 | 建议查的表 |
|----------|-----------|
| 报账单保存/提交异常 | T_RMBS_CLAIM + T_RMBS_CLAIM_ITEM |
| 支付状态异常 | T_RMBS_PAYLIST + T_RMBS_PAYLIST_FAULT |
| 会计分组/座席问题 | T_PROC_ACCOUNTANTTEAM + T_PROC_ACCOUNTANTTEAM_USER |
| 会计项目配置问题 | T_CO_ITEMLEVEL2 + T_CO_ITEMLEVEL3 |
| 用户权限问题 | SYS_USER + SYS_USER_ROLE + SYS_ROLEFUNC |
| 字典/参数配置 | T_RMBS_DICT + T_SYS_PARAMETER |
| 接受验收问题 | T_ACPT_BILL + T_ACPT_BILL_LINE_FRONT |
| 固定资产问题 | T_FA_ASSETS_COST_INFO + T_FA_ASSETS_DEPRN_INFO |
| 发票问题 | T_QUY_INVITEMINFO_SUBSET |
| 凭证问题 | T_PAYMENT_VOUCHER + T_VOUCHER_SPILIT |
| 汇率问题 | T_MIS_EXCHANGE_RATE |
| 接口日志 | INTERFACE_LOG |
