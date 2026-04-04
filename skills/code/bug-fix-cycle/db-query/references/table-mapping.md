# 业务表映射参考（完整版）

> 从项目 DO 实体类的 `@TableName` 注解自动提取，共覆盖 **15 个服务模块、600+ 张表**。
> 用于 db-query 快速定位要查哪个表。

---

## 1. 公共服务 (fssc-common-service) — 16 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| SYS_USER | SysUserDo | 系统用户表 |
| SYS_ROLE | SysRoleDo | 系统角色表 |
| SYS_USER_ROLE | SysUserRoleDo | 用户角色关联表 |
| SYS_FUNCTION | SysFunctionDo | 系统功能表 |
| SYS_ROLEFUNC | SysRolefuncDo | 角色功能关联表 |
| SYS_GROUP | SysGroupDo | 系统组表 |
| SYS_USER_GROUP | SysUserGroupDo | 用户组关联表 |
| SYS_TENANT | SysTenantDo | 租户表 |
| SYS_TENANT_GROUP | SysTenantGroupDo | 租户组表 |
| SYS_OU_BU_SEG | SysOuBuSegDo | 组织业务单位分段表 |
| TOTAL_OU | TotalOuDo | 组织总表 |
| T_RMBS_DICT | TRmbsDictDo | 字典表 |
| T_I18N_MESSAGE | TI18nMessageDo | 国际化消息表 |
| T_SYS_PARAMETER | TSysParameterDo | 系统参数表 |
| T_CO_COMSEGCODE | TCoComSegCodeDo | 会计通用分段编码表 |
| T_SYS_ALL_LOGIN_LOG | TSysAllLoginLogDo | 登录日志表 |

---

## 2. 配置服务 (fssc-config-service) — 149 表

### 账务团队与审批

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_PROC_ACCOUNTANTTEAM | AccountantTeamDo | 账务团队(会计分组)表 |
| T_PROC_ACCOUNTANTTEAM_ITEM | TProcAccountantteamItemDo | 账务团队项目表 |
| T_PROC_ACCOUNTANTTEAM_USER | TProcAccountantteamUserDo | 账务团队用户(座席)表 |
| T_PROC_BIZ_ACCOUNT | TProcBizAccountDo | 业务账户表 |
| T_PROC_DEPT_DIRECTOR | TProcDeptDirectorDo | 部门主管表 |
| T_PROC_DIRECTOR | TProcDirectorDo | 主管表 |
| T_PROC_PROVINCE_BIZDEPT | TProcProvinceBizdeptDo | 省业务部门表 |
| T_PROC_VISA_LEADER | TProcVisaLeaderDo | 签证负责人表 |
| T_PROC_OPERATION_PRINCIPAL | TProcOperationPrincipalDo | 运营负责人表 |
| T_PROC_PAYMENT_CONTROL | TProcPaymentControlDo | 支付控制表 |
| T_PROC_ACCOUNT_DOUBLECHECK | TProcAccountDoublecheckDo | 会计复核表 |
| T_PROC_ACCOUNT_DOUBLECHECK_LOG | TProcAccountDoublecheckLogDo | 会计复核日志表 |
| T_PROC_ACCOUNT_MANAGER | TProcAccountManagerDo | 会计经理表 |
| T_CLAIM_APPROVERS | TClaimApproversDo | 报账单审批人表 |
| T_PROCESS_OPINION | TProcessOpinionDo | 审批意见表 |

### 会计项目

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_CO_ITEMLEVEL2 | TCoItemlevel2Do | 会计项目二级表 |
| T_CO_ITEMLEVEL3 | TCoItemlevel3Do | 会计项目三级表 |
| T_CO_ITEMLEVEL3_MUTI | TCoItemlevel3MutiDo | 会计项目三级多类型表 |
| T_CO_ITEMLEVEL3_MUTI_T020 | TCoItemlevel3MutiT020Do | 会计项目三级多类型T020表 |
| T_CO_ITEMLEVEL3_MUTI_T020_OU | TCoItemlevel3MutiT020OuDo | 会计项目三级多类型T020组织表 |
| T_CO_ITEMLEVEL3_T020 | TCoItemlevel3T020Do | 会计项目三级T020表 |
| T_CO_ITEML3_CONF | TCoIteml3ConfDo | 会计项目三级配置表 |
| T_CO_ITEMLEVEL3_OU | TCoItemlevel3OuDo | 会计项目三级组织表 |
| T_CO_ITEM2_DEPTCOST | TCoItem2DeptcostDo | 会计项目二级部门成本表 |
| T_CO_INSIDE_ITEM2 | TCoInsideItem2Do | 内部会计项目二级表 |
| T_CO_INSIDE_ITEM2_ITEM3 | TCoInsideItem2Item3Do | 内部会计项目二三级关联表 |
| T_ITEM3_ACC | TItem3AccDo | 会计项目三级账户表 |
| T_CO_COMSEGCODE | TCoComsegcodeDo | 会计通用分段编码表 |

### 接受验收

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_ACPT_ROLE_CONFIG | TAcptRoleConfigDo | 接受角色配置表 |
| T_ACPT_DISPATCH_RULE | TAcptDispatchRuleDo | 接受分配规则表 |
| T_ACPT_VENDOR_RATE_CFG | TAcptVendorRateCfgDo | 供应商费率配置表 |
| T_ACPT_VENDOR_BANK_CFG | TAcptVendorBankCfgDo | 供应商银行配置表 |
| T_ACPT_VENDOR_AMOUNT_CFG | TAcptVendorAmountCfgDo | 供应商金额配置表 |

### 规则引擎

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_ENGINE_CATEGORY | TEngineCategoryDo | 引擎分类表 |
| T_ENGINE_CATEGORY_RULE | TEngineCategoryRuleDo | 引擎分类规则表 |
| T_ENGINE_ELEMENT | TEngineElementDo | 引擎元素表 |
| T_ENGINE_EXE_RULE | TEngineExeRuleDo | 引擎执行规则表 |
| T_ENGINE_FORM | TEngineFormDo | 引擎表单表 |
| T_ENGINE_FORM_068 | TEngineForm068Do | 引擎表单068表 |
| T_ENGINE_FORM_ITEM2 | TEngineFormItem2Do | 引擎表单二级项目表 |
| T_ENGINE_FORM_OU | TEngineFormOuDo | 引擎表单组织表 |
| T_ENGINE_FORM_RULE | TEngineFormRuleDo | 引擎表单规则表 |

### 资产配置

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_ASSET_ADJUST_TYPE_CONF | TAssetAdjustTypeConfDo | 资产调整类型配置表 |
| T_ASSET_SHOW | TAssetShowDo | 资产展示表 |
| T_ASSET_SUBJECT | TAssetSubjectDo | 资产科目表 |
| T_FA_ASSETS_CATEGORY_INFO | TFaAssetsCategoryInfoDo | 固定资产分类信息表 |
| T_RMBS_ASSETSBRAND | TRmbsAssetsbrandDo | 资产品牌表 |
| T_RMBS_ASSET_CATEGORY | TRmbsAssetCategoryDo | 资产分类表 |
| T_RMBS_ASSET_CLAIM_ITEMNAME | TRmbsAssetClaimItemNameDo | 资产报账项目名称表 |
| T_RMBS_ASSET_CLAIM_VALIDATE | TRmbsAssetClaimValidateDo | 资产报账验证表 |
| T_RMBS_ASSET_QUANTITY | TRmbsAssetQuantityDo | 资产数量表 |

### 供应商与黑名单

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_BLACKLIST | TBlacklistDo | 黑名单表 |
| T_BLACK_LIST_LOG | TBlackListLogDo | 黑名单日志表 |
| T_BLACK_LIST_SET | TBlackListSetDo | 黑名单设置表 |
| T_VENDOR_ASSOCIATE_CONFIG | TVendorAssociateConfigDo | 供应商关联配置表 |
| T_VENDOR_CONTROL_OU_CONFIG | TVendorControlOuConfigDo | 供应商控制组织配置表 |
| T_VENDOR_CONTROL_RANGE_CONFIG | TVendorControlRangeConfigDo | 供应商控制范围配置表 |
| T_RMBS_VENDOR_FREEZE_HEAD | TRmbsVendorFreezeHeadDo | 供应商冻结头表 |
| T_RMBS_VENDOR_UN_FREEZE | TRmbsVendorUnFreezeDo | 供应商解冻表 |
| T_RMBS_FOREIGN_BANK_ACCOUNT | TRmbsForeignBankAccountDo | 外币银行账户表 |

### 其他配置

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_MIS_EXCHANGE_RATE | TMisExchangeRateDo | 汇率表 |
| T_AP_PROJECT_T020_CONF | TApProjectT020ConfDo | AP项目T020配置表 |
| T_CAC_TASK | TCacTaskDo | CAC任务表 |
| T_GL_AUTO_SETTLEMENT_CONDITION | TGlAutoSettlementConditionDo | 自动结算条件表 |
| T_QUY_AR_RECEIPT_REMARK | TQuyArReceiptRemarkDo | 应收收据备注表 |
| T_RMBS_HRDEP_ROLE_OU | TRmbsHrdepRoleOuDo | 人力部门角色组织表 |
| T_RMBS_HRDEP_ROLE_MAP | TRmbsHrdepRoleMapDo | 人力部门角色映射表 |
| SYS_USER_TRAVEL_INFO | SysUserTravelInfoDo | 用户差旅信息表 |
| TRAVEL_CITY | TravelCityDo | 出差城市表 |
| T_RMBS_TRAVEL_CITY_TRANSPORT | TRmbsTravelCityTransportDo | 差旅城市交通表 |
| T_ALLOCATION_CONFIG | TAllocationConfigDo | 分摊配置表 |
| T_ALLOCATION_CONFIG_USER | TAllocationConfigUserDo | 分摊配置用户表 |
| T_ANNOUNCEMENT | TAnnouncementDo | 公告表 |
| T_ANNOUNCEMENT_MESSAGE | TAnnouncementMessageDo | 公告消息表 |
| T_ANNOUNCEMENT_SCROLL_CONFIG | TAnnouncementScrollConfigDo | 公告滚动配置表 |
| T_APP_CONFIG | TAppConfigDo | APP配置表 |
| T_APP_LOGIN_RECORD | TAppLoginRecordDo | APP登录记录表 |
| T_BILL_WARDEN_PERMISSIONS | TBillWardenPermissionsDo | 账单守护权限表 |
| T_BUSEG_NOTICE | TBusegNoticeDo | 业务段通知表 |
| T_BUSEG_NOTICE_LOG | TBusegNoticeLogDo | 业务段通知日志表 |
| T_BU_SEG_CODE_T035_CONF | TBuSegCodeT035ConfDo | 业务段编码T035配置表 |
| T_CLAIM_IINTERLLI_CONF | TClaimIinterlliConfDo | 报账单智能配置表 |
| T_CLAIM_NAVIGATION | TClaimNavigationDo | 报账单导航表 |
| T_CONFIGURATION_PAYMENTBANK | TConfigurationPaymentbankDo | 支付银行配置表 |
| T_DEPT_OU | TDeptOuDo | 部门组织关联表 |
| T_DOWN_REPORT_SET | TDownReportSetDo | 下载报告设置表 |
| T_DOWN_REPORT_SET_ISALLOU | TDownReportSetIsallouDo | 下载报告全组织设置表 |
| T_FUND_TIMECONFIG | TFundTimeconfigDo | 资金时间配置表 |
| T_MAINTAIN_PROCESS_CONFIG | TMaintainProcessConfigDo | 维护流程配置表 |
| T_MAINTAIN_PROCESS_CONFIG_TEMP | TMaintainProcessConfigTempDo | 维护流程配置临时表 |
| T_MATERIAL_GL_CONFIG | TMaterialGlConfigDo | 物料总账配置表 |
| T_OPERATOR_CONFIG | TOperatorConfigDo | 操作员配置表 |
| T_ORGANIZATION_OU_RELATION | TOrganizationOuRelationDo | 组织关系表 |
| T_PROJECT_BIZ_ACCOUNT | TProjectBizAccountDo | 项目业务账户表 |
| T_QUY_INV_ITEM_INFO_ITEM2 | TQuyInvItemInfoItem2Do | 发票项目二级信息表 |
| T_RENTAL_DISCOUNT_RATE | TRentalDiscountRateDo | 租赁折扣率表 |
| T_RMBS_ABM_MATCH_CONFIG | TRmbsAbmMatchConfigDo | ABM匹配配置表 |
| T_RMBS_AUTO_IMPORT_CONFIG | TRmbsAutoImportConfigDo | 自动导入配置表 |
| T_RMBS_CLAIM_DEL_REQ_HANDLER | TRmbsClaimDelReqHandlerDo | 报账单删除请求处理表 |
| T_RMBS_COST_SHARE_RATIO | TRmbsCostShareRatioDo | 费用分摊比例表 |
| T_RMBS_COST_SHARE_RATIO_ITEM | TRmbsCostShareRatioItemDo | 费用分摊比例项目表 |
| T_RMBS_DELAY_INVOICE_IMPORT | TRmbsDelayInvoiceImportDo | 延迟发票导入表 |
| T_RMBS_DELAY_INVOICE_UPDATELOG | TRmbsDelayInvoiceUpdatelogDo | 延迟发票更新日志表 |
| T_RMBS_ERP_CLAIM_RULE | TRmbsErpClaimRuleDo | ERP报账规则表 |
| T_RMBS_ERP_CLAIM_RULE_CHILD | TRmbsErpClaimRuleChildDo | ERP报账规则子表 |
| T_RMBS_GL_AUTO_VENDOR | TRmbsGlAutoVendorDo | 总账自动供应商表 |
| T_RMBS_GL_CATEGORY_MAP_REL | TRmbsGlCategoryMapRelDo | 总账分类映射关系表 |
| T_RMBS_INVOICE_AUTHENTICATION | TRmbsInvoiceAuthenticationDo | 发票认证表 |
| T_RMBS_JINDERUI_XT_VOUCHERINFO | TRmbsJinderuiXtVoucherinfoDo | 金蝶凭证信息表 |
| T_RMBS_MY_RED_LETTER_CONFIG | TRmbsMyRedLetterConfigDo | 红字配置表 |
| T_RMBS_OU_TAX | TRmbsOuTaxDo | 组织税务表 |
| T_RMBS_PAYCAT_CONF | TRmbsPaycatConfDo | 支付类别配置表 |
| T_RMBS_PROJECT_LOCK | TRmbsProjectLockDo | 项目锁定表 |
| T_RMBS_TPM_CONFIG | TRmbsTpmConfigDo | TPM配置表 |
| T_RMBS_TR_JOB | TRmbsTrJobDo | 差旅任务表 |
| T_RMBS_TR_JOB_LOG | TRmbsTrJobLogDo | 差旅任务日志表 |
| T_SCHEDULED_TASKS | TScheduledTasksDo | 定时任务表 |
| T_SCHEDULED_TASKS_LOG | TScheduledTasksLogDo | 定时任务日志表 |
| T_SYS_ACCOUNT_VALIDATE_CONF | TSysAccountValidateConfDo | 账户验证配置表 |
| T_SYS_CLAIM_VALIDATE_CONF | TSysClaimValidateConfDo | 报账验证配置表 |
| T_SYS_PLAN_PAYROLL | TSysPlanPayrollDo | 计划薪资表 |
| T_SYS_SPE_ACCOUNT_VALICONF | TSysSpeAccountValiconfDo | 特殊账户验证配置表 |
| T_SYS_TAX_CONF | TSysTaxConfDo | 税务配置表 |
| T_SYS_WSCFG | TSysWscfgDo | WebService配置表 |
| AAM_BORROWING_ARCHIVE_WAITDEAL | AamBorrowingArchiveWaitdealDo | 借阅归档待办表 |
| AAM_ITEM | AamItemDo | 档案项目表 |
| AAM_TRANSFER_ARCHIVE_WAITDEAL | AamTransferArchiveWaitdealDo | 移交归档待办表 |
| ABM_BILL | AbmBillDo | ABM账单表 |
| ABM_BZ | AbmBzDo | ABM包装表 |
| ABM_CB | AbmCbDo | ABM成本表 |
| AUTO_INVOICE_SET | AutoInvoiceSetDo | 自动开票设置表 |
| AUTO_POST_BOX | AutoPostBoxDo | 自动过账箱表 |
| BUDAN_CONFIG | BudanConfigDo | 补单配置表 |
| EIM_IMAGE_PER_USER | EimImagePerUserDo | 影像用户表 |
| FUND_ALLOCATION_CONFIG | FundAllocationConfigDo | 资金分配配置表 |
| HANDLE_MEDDLE_CONFIG | HandleMeddleConfigDo | 人工干预配置表 |
| INVOICE_RATE_REL_CONFIG | InvoiceRateRelConfigDo | 发票费率关联配置表 |
| ITEM_NOTICE | ItemNoticeDo | 项目通知表 |
| LEDGER_PAYMENT_ONLINE_CONFIG | LedgerPaymentOnlineConfigDo | 总账在线支付配置表 |
| MANDATORY_WRITE_OFF_CONFIG | MandatoryWriteOffConfigDo | 强制核销配置表 |
| MILKDEDUCTIONSLISTVIEW | MilkdeductionslistviewDo | 牛奶扣款列表视图 |
| OCR_WHITELIST_CONFIG | OcrWhitelistConfigDo | OCR白名单配置表 |
| PM_PROJECT | PmProjectDo | 项目管理表 |
| PM_PROJECT_LOG | PmProjectLogDo | 项目管理日志表 |
| PM_PROJECT_VALID_LOG | PmProjectValidLogDo | 项目管理验证日志表 |
| PROJECT_WAITDEAL | ProjectWaitdealDo | 项目待办表 |
| SHARED_MAILING_ADDRESS | SharedMailingAddressDo | 共享邮寄地址表 |

---

## 3. 报账服务 (fssc-claim-service)

### 3.1 核心报账 (claim-common) — 120+ 表

#### 报账单主体

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_CLAIM | TRmbsClaimDo | 报账单主表 |
| T_RMBS_CLAIM_LINE | TRmbsClaimLineDo | 报账单行明细表 |
| T_RMBS_CLAIM_LINE_HIS | TRmbsClaimLineHisDo | 报账单行历史表 |
| T_RMBS_CLAIM_LINE_TAX | TRmbsClaimLineTaxDo | 报账单行税务表 |
| T_RMBS_CLAIM_HIS | TRmbsClaimHisDo | 报账单历史表 |
| T_RMBS_CLAIM_HIS_YR | TRmbsClaimHisYrDo | 报账单年度历史表 |
| T_RMBS_CLAIM_LOCK | TRmbsClaimLockDo | 报账单锁定表 |
| T_RMBS_CLAIM_REPORT | TRmbsClaimReportDo | 报账单报告表 |
| T_RMBS_CLAIM_CVT_RECORD | TRmbsClaimCvtRecordDo | 报账单转换记录表 |
| T_RMBS_CLAIM_GENERATE_RULES | TRmbsClaimGenerateRulesDo | 报账单生成规则表 |
| T_RMBS_CLAIM_GL_AUTO | TRmbsClaimGlAutoDo | 报账单自动过账表 |
| T_RMBS_CLAIM_GL_AUTO_OCR_LOG | TRmbsClaimGlAutoOcrLogDo | 报账自动过账OCR日志表 |
| T_RMBS_CLAIM_ORGINVOICE | TRmbsClaimOrgInvoiceDo | 报账单原始发票表 |
| T_RMBS_CLAIM_COST_LINE | TRmbsClaimCostLineDo | 报账单费用行表 |
| T_RMBS_CLAIM_REL | TRmbsClaimRelDo | 报账单关联表 |
| T_RMBS_CLAIM_EXT_T061T062 | TRmbsClaimExtT061T062Do | 报账单扩展T061T062表 |
| T_RMBS_CLAIM_TRAVEL_JOB | TRmbsClaimTravelJobDo | 报账单差旅任务表 |
| T_RMBS_CLAIMSEQ | TRmbsClaimseqDo | 报账单序列表 |
| T_RMBS_TEMPLATE | TRmbsTemplateDo | 模板表 |
| WRITEOFFVIEW | WriteoffviewDo | 核销视图 |
| T_RMBS_CLAIM_IVOICE_CANCEL_LOG | TRmbsClaimIvoiceCancelLogDo | 报账单发票取消日志表 |
| T_RMBS_CLAIM_PRE_DISCOUNT | ClaimPreDiscountDo | 报账单预折扣表 |

#### 支付相关

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_PAYLIST | TRmbsPaylistDo | 支付单表 |
| T_RMBS_PAYLIST_YR | TRmbsPaylistYrDo | 支付单年度表 |
| T_RMBS_PAYLIST_LOCK | TRmbsPaylistLockDo | 支付单锁定表 |
| T_RMBS_PAYLIST_STOPLOG | TRmbsPaylistStoplogDo | 支付单停止日志表 |
| T_RMBS_PAYLIST_UPDATE_LOG | TRmbsPaylistUpdateLogDo | 支付单更新日志表 |
| T_RMBS_PAYLIST_UPD_VEND_LOG | TRmbsPaylistUpdVendLogDo | 支付单更新供应商日志表 |
| T_RMBS_PAYLIST_HANDLELOG | TRmbsPaylistHandleLogDo | 支付单处理日志表 |
| T_RMBS_PAYLIST_DELEGATION | TRmbsPaylistDelegationDo | 支付单委托表 |
| T_RMBS_PAYLIST_FAULT | TRmbsPaylistFaultDo | 支付单故障表 |
| T_RMBS_CLAIM_PAY_LINE | TRmbsClaimPayLineDo | 报账单支付行表 |
| T_RMBS_CLAIM_PAY_LINE_BAOLI | TRmbsClaimPayLineBaoliDo | 报账单保利支付行表 |
| T_RMBS_CLAIM_BANK | TRmbsClaimBankDo | 报账单银行表 |
| T_RMBS_CLAIM_BANK_LINE | TRmbsClaimBankLineDo | 报账单银行行表 |
| T_RMBS_PAY_FLEX | TRmbsPayFlexDo | 弹性支付表 |
| T_CD_PAYLIST | TCdPaylistDo | 承兑支付单表 |
| T_CD_LINE | TCdLineDo | 承兑行表 |
| T_CD_LINE_HIS | TCdLineHisDo | 承兑行历史表 |
| T_RMBS_MANUAL_PAY_CONFIG | TRmbsManualPayConfigDo | 手动支付配置表 |
| T_RMBS_CONTRACT_PAYMENT_SCHED | TRmbsContractPaymentSchedDo | 合同付款计划表 |
| T_LEASE_CONTRACT_PAY | TLeaseContractPayDo | 租赁合同支付表 |

#### 发票相关

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| ITM_INVOICE | ItmInvoiceDo | 发票表 |
| T_CLAIM_INVOICE_RELATION | TClaimInvoiceRelationDo | 报账单发票关联表 |
| T_RMBS_INPUT_TAX_AUTOTRANSFER | TRmbsInputTaxAutotransferDo | 进项税自动转移表 |
| T_RMBS_INPUT_TAX_AUTOTRAN_YR | TRmbsInputTaxAutotranYrDo | 进项税自动转移年度表 |
| T_APP_INVOICE_FOLDER | TAppInvoiceFolderDo | 发票夹表 |
| T_APP_INVOICE_FOLDER_BLACKLIST | TAppInvoiceFolderBlacklistDo | 发票夹黑名单表 |

#### 审批流程

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_PROCESS_WI_RECORD | TProcessWiRecordDo | 流程工作项记录表 |
| T_PROCESS_WI_RECORD_YR | TProcessWiRecordYrDo | 流程工作项记录年度表 |
| T_PROCESS_WI_RECORD_T001 | TProcessWiRecordT001Do | 流程工作项T001表 |
| T_PROCESS_WI_RECORD_CHG_HIS | TProcessWiRecordChgHisDo | 流程工作项变更历史表 |
| T_PROCESS_WI_HISTORY | TProcessWiHistoryDo | 流程工作项历史表 |
| T_PROCESS_WI_HISTORY_YR | TProcessWiHistoryYrDo | 流程工作项历史年度表 |
| T_ENGINE_PROCESS_DELEGATION | TEngineProcessDelegationDo | 引擎流程委托表 |

#### 合同相关

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| CM_CONTRACT | CmContractDo | 合同主表 |
| CM_CONTRACT_TERM | CmContractTermDo | 合同条款表 |
| CM_CONTRACT_WAITDEAL | CmContractWaitdealDo | 合同待办表 |
| T_LEASE_CONTRACT | TLeaseContractDo | 租赁合同表 |
| T_LEASE_CONTRACT_CHANGE | TLeaseContractChangeDo | 租赁合同变更表 |
| T_LEASE_CONTRACT_INTEREST | TLeaseContractInterestDo | 租赁合同利息表 |
| T_LEASE_CONTRACT_INTEREST_JOB | TLeaseContractInterestJobDo | 租赁合同利息任务表 |
| T_RMBS_CONTRACT_ENITY | TRmbsContractEnityDo | 合同实体表 |
| T_RMBS_CONTRACT_EXEC_USER | TRmbsContractExecUserDo | 合同执行用户表 |
| T_RMBS_CONTRACT_PROJECT | TRmbsContractProjectDo | 合同项目表 |

#### 资产相关

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_ASSET | TRmbsAssetDo | 报账资产主表 |
| T_RMBS_ASSET_AB | TRmbsAssetAbDo | 资产AB表 |
| T_RMBS_ASSET_CHANGE | TRmbsAssetChangeDo | 资产变更表 |
| T_RMBS_ASSET_CHANGE_DISTRIBUT | TRmbsAssetChangeDistributDo | 资产变更分配表 |
| T_RMBS_ASSET_DISTRIBUT | TRmbsAssetDistributDo | 资产分配表 |
| T_RMBS_ASSET_ORGAMT_ADJUST | TRmbsAssetOrgamtAdjustDo | 资产原值调整表 |
| T_RMBS_ASSET_OTHER_ADD | TRmbsAssetOtherAddDo | 资产其他增加表 |
| T_RMBS_ASSET_OTHER_REDUCE | TRmbsAssetOtherReduceDo | 资产其他减少表 |
| T_RMBS_ASSET_OTHER_REDUCE_LINE | TRmbsAssetOtherReduceLineDo | 资产其他减少行表 |
| T_FA_ASSETS_CATEGORY_INFO | TFaAssetsCategoryInfoDo | 固定资产分类信息表 |
| T_FA_ASSETS_PHYSICAL_INFO | TFaAssetsPhysicalInfoDo | 固定资产实物信息表 |

#### 保利/V2自动

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_BAOLI023CLAIM_REMIND | TRmbsBaoli023claimRemindDo | 保利023报账提醒表 |
| T_RMBS_BAOLICLAIM_CREATE023 | TRmbsBaoliclaimCreate023Do | 保利报账创建023表 |
| T_RMBS_BAOLICLAIM_EARLYWARNING | TRmbsBaoliclaimEarlywarningDo | 保利报账预警表 |
| T_RMBS_CLAIM_BAOLI_RELINE | TRmbsClaimBaoliRelineDo | 报账单保利重新行表 |
| T_FACTOR_BUS_TYPE_Y | TFactorBusTypeYDo | 保理业务类型年度表 |
| T_FACTOR_CLAIM_FINANCE_RELATE | TFactorClaimFinanceRelateDo | 保理报账财务关联表 |
| T_FACTOR_DETAIL_INFO | TFactorDetailInfoDo | 保理详情信息表 |
| T_FACTOR_OVER_FINANCE_INFO | TFactorOverFinanceInfoDo | 保理超额财务信息表 |
| T_V2_AUTO_CLAIM_JOB | TV2AutoClaimJobDo | V2自动报账任务表 |
| T_V2_AUTO_CLAIM_JOB_T031 | TV2AutoClaimJobT031Do | V2自动报账T031任务表 |
| T_V2_AUTO_CLAIM_JOB_T031_BACKUP | TV2AutoClaimJobT031BackupDo | V2自动报账T031备份表 |
| T_V2_CREATE_REQ | TV2CreateReqDo | V2创建请求表 |
| T_V2_CREATE_REQ_LINE | TV2CreateReqLineDo | V2创建请求行表 |

#### 其他公共

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| SYS_LOG | SysLogDo | 系统日志表 |
| TPM_CLAIM_AMOUNT | TpmClaimAmountDo | TPM报账金额表 |
| TPM_CLAIM_LINE | TpmClaimLineDo | TPM报账行表 |
| TPM_CX_EXEC_INT | TpmCxExecIntDo | TPM营销执行文件表 |
| T_ACPT_BILL | TAcptBillDo | 接受账单表 |
| T_ACPT_BILL_ITEM_CFG | TAcptBillItemCfgDo | 接受账单项目配置表 |
| T_ALERT_CONTROL | TAlertControlDo | 预警控制表 |
| T_ALLOCATION_HEAD | TAllocationHeadDo | 分摊头表 |
| T_ALLOCATION_LINE | TAllocationLineDo | 分摊行表 |
| T_ALLOCATION_TAX_LINE | TAllocationTaxLineDo | 分摊税行表 |
| T_BANK_RECEIPT | TBankReceiptDo | 银行回单表 |
| T_CM_CLAIM_CANCEL | TCmClaimCancelDo | 合同报账取消表 |
| T_COST_LINE | TCostLineDo | 成本行表 |
| T_FUND_ACCOUNT_INFO | TFundAccountInfoDo | 资金账户信息表 |
| T_FUND_ACCOUNT_TRANS_FLOW | TFundAccountTransFlowDo | 账户交易流水表 |
| T_FUND_ACCOUNT_TRANS_HANDLELOG | TFundAccountTransHandlelogDo | 账户交易处理日志表 |
| T_FUNDS_TRANSFER_CLAIM_JOB | TFundsTransferClaimJobDo | 资金转账报账任务表 |
| T_ITSM_QA_CREATE | TItsmQaCreateDo | ITSM质量创建表 |
| T_ITSM_QA_CREATE_RESPONSE | TItsmQaCreateResponseDo | ITSM质量创建响应表 |
| T_ITSM_QA_SCORE | TItsmQaScoreDo | ITSM质量评分表 |
| T_LINE_DIFF_AMOUNT | TLineDiffAmountDo | 行差异金额表 |
| T_LOAN | TLoanDo | 借款表 |
| T_LOAN_CONTRACT | TLoanContractDo | 借款合同表 |
| T_MILK_ACCOUNT | TMilkAccountDo | 牛奶账户表 |
| T_MISPROC_CLAIM | TMisprocClaimDo | 异常处理报账表 |
| T_MISPROC_LOG | TMisprocLogDo | 异常处理日志表 |
| T_MIS_AP_PROFILE_OPTIONS | TMisApProfileOptionsDo | AP配置选项表 |
| T_MIS_INQPAYMENTBANKINFO | TMisInqpaymentbankinfoDo | 支付银行信息查询表 |
| T_MIS_INQPAYMENTDOCUMENTSINFO | TMisInqpaymentdocumentsinfoDo | 支付文档信息查询表 |
| T_MIS_INQVENDORSITE | TMisInqvendorsiteDo | 供应商站点查询表 |
| t_mis_inqvendor | TMisInqvendorDo | 供应商查询表 |
| t_mis_inqvendorbank | TMisInqvendorBank | 供应商银行查询表 |
| T_MIS_INQVSETVALUEINFO | TMisInqvsetvalueinfoDo | 值集信息查询表 |
| T_MIS_SYNC_VOUCHER_HEAD | TMisSyncVoucherHeadDo | 同步凭证头表 |
| T_MIS_SYNC_VOUCHER_LINE | TMisSyncVoucherLineDo | 同步凭证行表 |
| T_OA_PROCESS_INFO | TOaProcessInfoDo | OA流程信息表 |
| OA_PENDING_LOG | OaPendingLogDo | OA待办日志表 |
| OCR_MULTIY_CALLBACK_LOG | OcrMultiyCallbackLogDo | OCR多次回调日志表 |
| OCR_VALIDATION_CONFIG | OcrValidationConfigDo | OCR验证配置表 |
| T_PAYMENT_NOTICE_VOUCHER | TPaymentNoticeVoucherDo | 支付通知凭证表 |
| T_PAYOBJECT_INQVENDOR | TPayobjectInqvendorDo | 支付对象供应商查询表 |
| T_QUY_AR_BATCH_SOURCE | TQuyArBatchSourceDo | 应收批次来源表 |
| T_QUY_AR_CUST_SITE_INFO | TQuyArCustSiteInfoDo | 客户站点信息表 |
| T_QUY_AR_RE_METHOD | TQuyArReMethodDo | 应收方法表 |
| T_QUY_EBS_OUSYBWHSE | TQuyEbsOusybwhseDo | EBS组织仓库表 |
| T_QUY_INV_ITEM_INFO | TQuyInvItemInfoDo | 发票项目信息表 |
| T_QUY_INVITEMINFO_SUBSET | TQuyInvItemInfoSubsetDo | 发票项目信息子集表 |
| T_RMBS_ACCRUED_REL | TRmbsAccruedRelDo | 预提关联表 |
| T_RMBS_AR_AMT_REMAIN | TRmbsArAmtRemainDo | 应收金额余额表 |
| T_RMBS_RECEIPT_SUB_INFO | TRmbsReceiptSubInfoDo | 收据分项信息表 |
| T_RMBS_RECEIPT_SUB_VENDOR_INFO | TRmbsReceiptSubVendorInfoDo | 收据分项供应商信息表 |
| T_RMBS_REMARK_TEMPLATE | TRmbsRemarkTemplateDo | 备注模板表 |
| T_RMBS_ESTIMATION_OFFSET | TRmbsEstimationOffsetDo | 预估冲抵表 |
| T_RMBS_MILK_DE_VENDOR_CONF | TRmbsMilkDeVendorConfDo | 牛奶扣除供应商配置表 |
| T_RMBS_MOBILEFEE_QUOTA | TRmbsMobilefeeQuotaDo | 话费额度表 |
| T_RMBS_UNIFORMITY_CONFIG | TRmbsUniformityConfigDo | 统一性配置表 |
| T_RMBS_UNIFORMITY_CONFIG_YR | TRmbsUniformityConfigYrDo | 统一性配置年度表 |
| T_RMBS_VENDOR_FREEZE | TRmbsVendorFreezeDo | 供应商冻结表 |
| T_RMBS_VERIFICATION_SENDBACK | TRmbsVerificationSendbackDo | 验证退回表 |
| T_RMBS_DELAY_IMPORT_FAILLOG | TRmbsDelayImportFaillogDo | 延迟导入失败日志表 |
| T_RMBS_DELAY_IMPORT_FAILLOGYR | TRmbsDelayImportFaillogyrDo | 延迟导入失败日志年度表 |
| T_RMBS_SYNC_YRDATA_LOG | TRmbsSyncYrdataLogDo | 同步年度数据日志表 |
| T_RMBS_TAX_TRANSFER_CONTROL | TRmbsTaxTransferControlDo | 税务转移控制表 |
| T_ERP_SECURITY_VERIFI_RULES | TErpSecurityVerifiRulesDo | ERP安全验证规则表 |
| T_ERP_SECURITY_VERI_ASSIGNRESP | TErpSecurityVeriAssignrespDo | ERP安全验证分配响应表 |
| T_SPECIAL_BANK_INFO | TSpecialBankInfoDo | 特殊银行信息表 |
| T_SYS_MODIFYDATABYHAND_LOG | TSysModifyDataByHandLogDo | 手动修改数据日志表 |
| T_SYS_TAX_PARM | TSysTaxParmDo | 税务参数表 |
| T_COM_SEND_EMAIL_DATA | TComSendEmailDataDo | 邮件发送数据表 |
| T_CLAIM_PROJECT_FEE_PUSH_OA | TClaimProjectFeePushOaDo | 报账项目费用推OA表 |
| T_RMBS_PO_CLAIM | TRmbsPoClaimDo | 采购报账表 |
| T_RMBS_PO_LINE | TRmbsPoLineDo | 采购行表 |
| T_RMBS_PO_LINE_SEGCODE_CONFIG | TRmbsPoLineSegcodeConfigDo | 采购行分段编码配置表 |
| T_RMBS_PO_PAYLIST | TRmbsPoPaylistDo | 采购支付单表 |
| T_RMBS_PO_TAXLINE | TRmbsPoTaxlineDo | 采购税行表 |
| T_RMBS_POLINESREL | TRmbsPolinesrelDo | 采购行关联表 |
| LEDGER_PAYEE_OU_CONFIG | LedgerPayeeOuConfigDo | 总账收款方组织配置表 |
| LEDGER_PAYEE_OU_NB_CONFIG | LedgerPayeeOuNbConfigDo | 总账收款方内部配置表 |
| LEDGER_PAYEE_OU_TS_CONFIG | LedgerPayeeOuTsConfigDo | 总账收款方特殊配置表 |
| LEDGER_PAYEE_OU_XJLL_CONFIG | LedgerPayeeOuXjllConfigDo | 总账收款方现金流配置表 |
| ABM_WORKBENCH | AbmWorkbenchDo | ABM工作台表 |
| ABM_BILL_CLAIM_LINE | AbmBillClaimLineDo | ABM账单报账行表 |
| HANDLE_MEDDLE_EMAIL | HandleMeddleEmailDo | 人工干预邮件表 |
| ATTACHMENT_PROMPT | AttachmentPromptDo | 附件提示表 |
| ACPTBILL_ICBC_WAITACPT | AcptbillIcbcWaitacptDo | 工行待接受账单表 |
| T007_CALL_BACK_LOAN_STATUS_JOB | T007CallBackLoanStatusJobDo | T007借款状态回调任务表 |
| T008_CALL_BACK_CXSTATUS_JOB | T008CallBackCxstatusJobDo | T008营销状态回调任务表 |
| WORK_DAY | WorkDayDo | 工作日表 |
| WORK_TIME | WorkTimeDo | 工作时间表 |

### 3.2 OTC 相关 (claim-otc) — 14 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_QUY_AR_AMT_REMAIN | TQuyArAmtRemainDo | 应收金额余额表 |
| T_QUY_AR_AMT_MARGIN | TQuyArAmtMarginDo | 应收金额差额表 |
| T_QUY_AR_RECEIVCE_PAYMENT | TQuyArReceivePaymentDo | 应收收款支付表 |
| T_AR_AMT_REMAIN_CONFIG | TArAmtRemainConfigDo | 应收金额余额配置表 |
| T_QUY_AR_AMT_REMAIN_TR_NEW | TQuyArAmtRemainTrNewDo | 应收金额余额转账新表 |
| T_OTC_ITEM3_PRODUCT_CONFIG | TOtcItem3ProductConfigDo | OTC三级产品配置表 |
| T_OTC_INVOICE_RATE_CONFIG | TOtcInvoiceRateConfigDo | OTC发票费率配置表 |
| T_MANUAL_INVOICE_CONF | TManualInvoiceConfDo | 手动发票配置表 |
| T_QUY_INV_UOM_CODE | QuyInvUomCodeDo | 发票单位代码表 |
| T_QUY_RA_CUST_TRX_TYPE | QuyRaCustTrxTypeDo | 客户交易类型表 |
| T_RMBS_RECEIPT_SUB_INFO | ReceiptSubInfoDo | 收据分项信息表 |
| T_RMBS_RECEIPT_SUB_VENDOR_INFO | ReceiptSubVendorInfoDo | 收据分项供应商信息表 |
| T_RETURN_REMAIN_ITEM2_CONFIG | ReturnRemainItem2ConfigDo | 返回余额二级配置表 |
| T_RMBS_OTCSUBMISSIONAREA | TRmbsOtcsubmissionareaDo | OTC提交区域表 |

### 3.3 差旅报销 (claim-tr) — 1 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_CLAIM_T064_T065_T066 | ClaimT064T065T066Do | 差旅报销T064-T066表 |

### 3.4 差旅审核 (claim-eer) — 24 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_CLAIM_OA | TRmbsClaimOaDo | 报账单OA关联表 |
| T_RMBS_CLAIM_OA_PROCESS | TRmbsClaimOaProcessDo | 报账单OA流程表 |
| T_RMBS_CLAIM_TRAVEL_LINE | TRmbsClaimTravelLineDo | 差旅行程行表 |
| T_RMBS_CLAIM_TRAVEL_LINE_OA | TRmbsClaimTravelLineOaDo | 差旅行程行OA表 |
| T_RMBS_CLAIM_TRAVEL_BEDLINE_OA | TRmbsClaimTravelBedlineOaDo | 差旅住宿行OA表 |
| T_RMBS_CLAIM_TRAVEL_CAR | TRmbsClaimTravelCarDo | 差旅用车表 |
| T_RMBS_CLAIM_TRAVEL_FILE | TRmbsClaimTravelFileDo | 差旅文件表 |
| T_RMBS_CLAIM_TRAVEL_TAX | TRmbsClaimTravelTaxDo | 差旅税务表 |
| T_RMBS_CLAIM_TRAVEL_TRAIN_OA | TRmbsClaimTravelTrainOaDo | 差旅火车OA表 |
| T_RMBS_CLAIM_TRAVEL_VENDOR_OA | TRmbsClaimTravelVendorOaDo | 差旅供应商OA表 |
| T_RMBS_CLAIM_TRAVEL_RELLINE_OA | TRmbsClaimTravelRellineOaDo | 差旅关联行OA表 |
| T_RMBS_CLAIM_TRAVEL_XCLINE_OA | TRmbsClaimTravelXclineOaDo | 差旅行程线OA表 |
| T_RMBS_CLAIM_TRAVEL_OA_LOCK | TRmbsClaimTravelOaLockDo | 差旅OA锁定表 |
| T_CC_QA | TCcQaDo | 差旅审核问答表 |
| T_CC_QA_YR | TCcQaYrDo | 差旅审核问答年度表 |
| T_CC_TYPE | TCcTypeDo | 差旅审核类型表 |
| T_CC_SUB_TYPE | TCcSubTypeDo | 差旅审核子类型表 |
| T_CC_TYPE_RELATION | TCcTypeRelationDo | 类型关联表 |
| T_CC_RELATION | TCcRelationDo | 差旅审核关联表 |
| T_CC_USER | TCcUserDo | 差旅审核用户表 |
| T_CC_IT_USER | TCcItUserDo | IT用户表 |
| T_CC_ATTACHMENT | TCcAttachmentDo | 差旅审核附件表 |
| T_CC_LIMITTIME | TCcLimittimeDo | 限时配置表 |
| TRAVEL_BZ_VIEW | TravelBzViewDo | 差旅报账视图 |

### 3.5 BASE 相关 (claim-base) — 33 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_PROC_PROVINCE_BIZDEPT_058 | TProcProvinceBizdept058Do | 058省业务部门表 |
| T_PROC_PROVINCE_BIZDEPT_058SRC | TProcProvinceBizdept058srcDo | 058省业务部门源表 |
| T_PROC_DEPT_DIRECTOR_058 | TProcDeptDirector058Do | 058部门主管表 |
| T_PROC_DEPT_DIRECTOR_058_SRC | TProcDeptDirector058SrcDo | 058部门主管源表 |
| T_PROC_DIRECTOR_058 | TProcDirector058Do | 058主管表 |
| T_PROC_DIRECTOR_058_SOURCE | TProcDirector058SourceDo | 058主管源表 |
| T_PROC_BIZ_ACCOUNT_058 | TProcBizAccount058Do | 058业务账户表 |
| T_PROC_BIZ_ACCOUNT_058_SOURCE | TProcBizAccount058SourceDo | 058业务账户源表 |
| T_CO_ITEMLEVEL2_058 | TCoItemlevel2058Do | 058会计项目二级表 |
| T_CO_ITEMLEVEL2_058_SOURCE | TCoItemlevel2058SourceDo | 058会计项目二级源表 |
| T_CO_COMSEG_CODE_058 | TCoComsegCode058Do | 058通用分段编码表 |
| T_CO_COMSEG_CODE_058_SOURCE | TCoComsegCode058SourceDo | 058通用分段编码源表 |
| AUTO_IMPORT_NO_PROCESS_CLAIM | AutoImportNoProcessClaimDo | 自动导入未处理报账表 |
| AUTO_POST | AutoPostDo | 自动过账表 |
| AUTO_POST_BOX | AutoPostBoxDo | 自动过账箱表 |
| AUTO_POST_BOX_HIS | AutoPostBoxHisDo | 自动过账箱历史表 |
| AUTO_POST_LOGIN | AutoPostLoginDo | 自动过账登录表 |
| BATCH_APPROVE_CONFIG | BatchApproveConfigDo | 批量审批配置表 |
| T_CLAIM_INVOICE_RECORD_LIBRARY | TClaimInvoiceRecordLibrary | 报账单发票记录库表 |
| T_CLAIM_REPORTS_DOWNLOAD | TClaimReportsDownloadDo | 报账报告下载表 |
| T_RMBS_BW_JOB_EXECUT_LOG | TRmbsBwJobExecutLog | 百望任务执行日志表 |
| T_RMBS_BW_JOB_EXECUT_DETAIL_LOG | TRmbsBwJobExecutDetailLog | 百望任务执行详情日志表 |
| T_RMBS_CLAIM_DEL_REQ | TRmbsClaimDelReqDo | 报账单删除请求表 |
| T_RMBS_ITEM2ID_REDUCETYPE | TRmbsItem2idReducetypeDo | 二级项目减少类型表 |
| T_TAX_RATE_SET | TTaxRateSetDo | 税率设置表 |
| T_V2_DATA | TV2DataDo | V2数据表 |
| T_V2_DATA_BACKUP | TV2DataBackupDo | V2数据备份表 |
| T_V2_DATA_LINE | TV2DataLineDo | V2数据行表 |
| T_V2_DATA_LINE_BACKUP | TV2DataLineBackupDo | V2数据行备份表 |
| ODM_DOCUMENT_LOG | OdmDocumentLogDo | ODM文档日志表 |
| ODM_PACKAGE | OdmPackageDo | ODM包表 |
| ODM_PACKAGE_LINE | OdmPackageLineDo | ODM包行表 |
| ODM_PACKAGE_LOG | OdmPackageLogDo | ODM包日志表 |

### 3.6 固定资产 (claim-fa) — 2 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_OA_REQ_ASSET | TRmbsOaReqAssetDo | OA资产请求表 |
| T_RMBS_OA_REQ_CLAIM | TRmbsOaReqClaimDo | OA报账请求表 |

### 3.7 PTP采购 (claim-ptp) — 5 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_CUSTOMS_CLEARANCE_VOUCHER | TCustomsClearanceVoucherDo | 海关清关凭证表 |
| T_RMBS_MILK_DATA_POOL | TRmbsMilkDataPoolDo | 牛奶数据池表 |
| T_RMBS_MILK_DATA_POOL_LINE | TRmbsMilkDataPoolLineDo | 牛奶数据池行表 |
| T_RMBS_PO_AGRI_PRO_CONFIG | RmbsPoAgriProConfigDo | 采购农业产品配置表 |
| T_RMBS_PURCHASE_OU_CONFIG | TRmbsPurchaseOuConfigDo | 采购组织配置表 |

---

## 4. 资金服务 (fssc-fund-service) — 18 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_RMBS_PAYLIST_DELEGATION | FundRmbsPaylistDelegationDo | 支付单委托表 |
| T_RMBS_PAYLIST_FAULT | TRmbsPaylistFaultDo | 支付单故障表 |
| T_RMBS_PAYLIST_FOREIGNTURNLOG | TRmbsPaylistForeignturnlogDo | 外币转账日志表 |
| T_RMBS_LC_LINE | TRmbsLcLineDo | 信用证额度行表 |
| IS_FREEZE_PAYMENTLIST | IsFreezePaymentlistDo | 冻结支付单表 |
| DELAY_PAYMENT_PAYLIST | DelayPaymentPaylistDo | 延迟支付单表 |
| T_AUTO_AUDIT_CONFIG | TAutoAuditConfigDo | 自动审计配置表 |
| T_AUTO_AUDIT_BASE | TAutoAuditBaseDo | 自动审计基础表 |
| T_AUTO_AUDIT_LOG | TAutoAuditLogDo | 自动审计日志表 |
| T_AUTO_AUDIT_RECONCILIATION | TAutoAuditReconciliationDo | 自动审计对账表 |
| T_AUTO_AUDIT_FUNDS_BANK | TAutoAuditFundsBankDo | 自动审计资金银行表 |
| T_AUTO_AUDIT_CBS_BANK | TAutoAuditCbsBankDo | 自动审计CBS银行表 |
| T_AUTO_AUDIT_ERP_BANK | TAutoAuditErpBankDo | 自动审计ERP银行表 |
| T_FUND_ACCOUNT_TRANS_FLOW | TFundAccountTransFlowDo | 账户交易流水表 |
| T_FUND_ACCOUNT_TRANS_FLOW_TMP | TFundAccountTransFlowTmpDo | 账户交易流水临时表 |
| T_FUND_ACCOUNT_TRANS_LOCK | TFundAccountTransLockDo | 账户交易锁定表 |
| T_FUND_ACCOUNT_TRANS_HANDLELOG | TFundAccountTransHandlelogDo | 账户交易处理日志表 |
| T_FUND_HR_APPOVE_LOG | TFundHrAppoveLogDo | 人力资源审批日志表 |

---

## 5. 集成服务 (fssc-integration-service) — 50 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_ACPT_BILL | TAcptBillDo | 接受账单表 |
| T_ACPT_BILL_LINE_FRONT | TAcptBillLineFrontDo | 接受账单行前端表 |
| T_ACPT_BILL_LINE_BACK | TAcptBillLineBack | 接受账单行后端表 |
| T_FA_ASSETS_COST_INFO | TFaAssetsCostInfoDo | 固定资产成本信息表 |
| T_FA_ASSETS_DEPRN_INFO | TFaAssetsDeprnInfoDo | 固定资产折旧信息表 |
| T_FA_ASSETS_DISTRIBUT_INFO | TFaAssetsDistributInfoDo | 固定资产分配信息表 |
| T_FA_ASSETS_CATEGORY_INFO | TFaAssetsCategoryInfoDo | 固定资产分类信息表 |
| T_QUY_INVITEMINFO_SUBSET | TQuyInviteminfoSubsetDo | 发票项目信息子集表 |
| T_QUY_INV_ITEM_INFO_BAK | TQuyInvItemInfoBakDo | 发票项目信息备份表 |
| BW_IINVOICE_LIB_ORIGIN | BwIinvoiceLibOriginDo | BI发票库源表 |
| T_PAYMENT_VOUCHER | TPaymentVoucherDo | 支付凭证表 |
| T_CUSTOMS_CLEARANCE_VOUCHER | TCustomsClearanceVoucherDo | 海关清关凭证表 |
| T_VOUCHER_SPILIT | TVoucherSpilitDo | 凭证分割表 |
| T_FUNDS_TRANSFER_CLAIM_JOB | TFundsTransferClaimJobDo | 资金转账报账任务表 |
| T_DIRECTORY_VENDOR_CONFIG | TDirectoryVendorConfigDo | 目录供应商配置表 |
| T_SYS_ERP_PARAM | TSysErpParamDo | 系统ERP参数表 |
| T_QUY_AR_RECEIPT_ACTIVITY | TQuyArReceiptActivityDo | 应收收据活动表 |
| T_RMBS_PO_AGRI_PRO_CONFIG | TRmbsPoAgriProConfigDo | 采购农业产品配置表 |
| T_RMBS_CUSTOMER_STALE | TRmbsCustomerStaleDo | 客户陈旧数据表 |
| T_AUTOARCHIVE_USER | TAutoarchiveUserDo | 自动归档用户表 |
| BW_ASYNC_RECORDS | BwAsyncRecordsDo | BI异步记录表 |
| T_FUND_ACCOUNTS | TFundAccountsDo | 资金账户表 |
| TPM_CX_EXEC_EMP_INT | TpmCxExecEmpIntDo | TPM执行员工集成表 |
| INTERFACE_LOG | InterfaceLogDo | 接口日志表 |
| T_RMBS_TEMPLATE | TRmbsTemplateDo | 模板表 |
| T_RMBS_BAOLI023CLAIM_REMIND | TRmbsBaoli023claimRemindDo | 保利023报账提醒表 |
| T_RMBS_BAOLICLAIM_CREATE023 | TRmbsBaoliclaimCreate023Do | 保利报账创建023表 |
| T_RMBS_WEBSERVICEXML | TRmbsWebservicexmlDo | WebService XML表 |
| EBS_INVOICE_PAY_GL | EbsInvoicePayGlDo | EBS发票支付总账表 |
| FUND_PLAN_CUSTOMER_ACCOUNT | FundPlanCustomerAccountDo | 资金计划客户账户表 |
| SOAP_LOG_INFO | SoapLogInfoDo | SOAP日志信息表 |
| T_BANK_LOG | BankLogDo | 银行日志表 |
| T_CATALOGUE_DELETE_FLAG | TCatalogueDeleteFlagDo | 目录删除标志表 |
| T_FSSC_GROUPINFO_SEND_EHR | TFsscGroupinfoSendEhrDo | 集团信息发送EHR表 |
| T_HR_POSITION_COLLECT_INFO | THrPositionCollectInfoDo | 人力职位采集信息表 |
| T_LEASE_CONTRACT_INTEREST | TLeaseContractInterestDo | 租赁合同利息表 |
| T_MIS_ALL_PEOPLE | TMisAllPeopleDo | 全员信息表 |
| T_MIS_GL_CODE_COMBINATION | TMisGlCodeCombinationDo | 总账编码组合表 |
| T_MIS_GL_VOUCHERINFO | TMisGlVoucherinfoDo | 总账凭证信息表 |
| T_MIS_HRORG_MAP_ERPORG | TMisHrorgMapErporgDo | HR组织映射ERP组织表 |
| T_QUY_AR_AMT_REMAIN | TQuyArAmtRemainDo | 应收金额余额表 |
| T_QUY_AR_AMT_REMAIN_TR_NEW | TQuyArAmtRemainTrNewDo | 应收转账余额新表 |
| T_QUY_AR_BATCH_SOURCE | TQuyArBatchSourceDo | 应收批次来源表 |
| T_QUY_INV_UOM_CODE | TQuyInvUomCodeDo | 发票单位代码表 |
| T_QUY_RA_CUST_TRX_TYPE | TQuyRaCustTrxTypeDo | 客户交易类型表 |
| T_SEGMENT1SRV | TSegment1srvDo | 段1服务表 |
| T_SEGMENT2SRV | TSegment2srvDo | 段2服务表 |
| T_SEGMENT3SRV | TSegment3srvDo | 段3服务表 |
| T_UPDATE_CLAIM_STATE_INFO | TUpdateClaimStateInfoDo | 更新报账状态信息表 |
| T_AUTO_AUDIT_FUNDS_BANK | TAutoAuditFundsBankDo | 自动审计资金银行表 |

---

## 6. 发票服务 (fssc-invoice-service) — 18 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| BW_IINVOICE_LIB_HEAD | BwIinvoiceLibHeadDo | 百望发票头信息表 |
| BW_IINVOICE_LIB_LINE | BwIinvoiceLibLineDo | 百望发票行信息表 |
| BW_INVOICE_SYNC_RECORD | BwIinvoiceSyncRecordDo | 百望发票同步记录表 |
| T_CLAIM_INVOICE_RECORD_LIBRARY | TClaimInvoiceRecordLibraryDo | 报账发票记录库表 |
| T_CLAIM_INVOICE_ERP | TClaimInvoiceErp | 报账发票ERP表 |
| INVOICE_RECORD_LIBRARY_TODO | InvoiceRecordLibraryTodoDo | 发票记录库待办表 |
| T_INVOICE_APPLY_OU | TInvoiceApplyOuDo | 发票申请组织表 |
| T_CXINVOICE_QX_AUTHENTICATION | TCxinvoiceQxAuthenticationDo | 发票权限认证表 |
| T_RMBS_FINANCEPREREVIEW_FALG | TRmbsFinanceprereviewFalgDo | 财务预审标记表 |
| T_RMBS_CLAIM_IVOICE_CANCEL_LOG | TRmbsClaimInvoiceCancelLogDo | 报账发票取消日志表 |
| T_APP_INVOICE_FOLDER_HIS | TAppInvoiceFolderHisDo | 发票夹历史表 |
| T_APP_INVOICE_FOLDER_OCRREQHIS | TAppInvoiceFolderOcrreqhisDo | 发票夹OCR请求历史表 |
| T_BW_INPUT_TAX_PERIOD | TBwInputTaxPeriodDo | 百望进项税期间表 |
| SYS_LOG | SysLogDo | 系统日志表 |
| OCR_INVOICE_LIBRARY | OcrInvoiceLibraryDo | OCR发票库表 |
| OCR_RECOG_REPORT | OcrRecogReportDo | OCR识别报告表 |
| OCR_SWITCH_OFF_CLAIM | OcrSwitchOffClaimDo | OCR关闭报账表 |
| ocr_repeat_report_view | OcrRepeatReportViewDo | OCR重复报告视图 |

---

## 7. CAC审核服务 (fssc-cac-service) — 42 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_CAC_TASK | TCacTaskDo | CAC任务表 |
| T_CAC_TASK_DETL | TCacTaskDetlDo | CAC任务明细表 |
| T_CAC_TASK_DETL_HIS | TCacTaskDetlHisDo | CAC任务明细历史表 |
| T_CAC_TASK_DEPT | TCacTaskDeptDo | CAC任务部门表 |
| T_CAC_TASK_ROLE | TCacTaskRoleDo | CAC任务角色表 |
| T_CAC_TASK_ROLE_INITCONFIG | TCacTaskRoleInitconfigDo | CAC任务角色初始配置表 |
| T_CAC_TASK_SETTING | TCacTaskSettingDo | CAC任务设置表 |
| T_CAC_TASK_RELATION | TCacTaskRelationDo | CAC任务关联表 |
| T_CAC_TASK_REJECT | TCacTaskRejectDo | CAC任务驳回表 |
| T_CAC_TASK_REJECT_RELATION | TCacTaskRejectRelationDo | CAC任务驳回关联表 |
| T_CAC_TASK_COMMENT_TYPE | TCacTaskCommentTypeDo | CAC任务评论类型表 |
| T_CAC_RULE | TCacRuleDo | CAC规则表 |
| T_CAC_RULE_TASK | TCacRuleTaskDo | CAC规则任务表 |
| T_CAC_RULE_SETTING_1 | TCacRuleSetting1Do | CAC规则设置1表 |
| T_CAC_RULE_SETTING2 | TCacRuleSetting2Do | CAC规则设置2表 |
| T_CAC_RULE_SETTING3 | TCacRuleSetting3Do | CAC规则设置3表 |
| T_CAC_RULE_SETTING4 | TCacRuleSetting4Do | CAC规则设置4表 |
| T_CAC_RULE10_EXPORTCOMPREPORT | TCacRule10ExportcompreportDo | CAC规则10导出报告表 |
| T_CAC_PROCESS_RECORD | TCacProcessRecordDo | CAC流程记录表 |
| T_CAC_PROCESS_TASK_RECORD | TCacProcessTaskRecordDo | CAC流程任务记录表 |
| T_CAC_PROCESS_TASK_APPROVER | TCacProcessTaskApproverDo | CAC流程任务审批人表 |
| T_CAC_PROCESS_REJECT_APPROVER | TCacProcessRejectApproverDo | CAC流程驳回审批人表 |
| T_CAC_OU_ITEM | TCacOuItemDo | CAC组织项目表 |
| T_CAC_OU_ITEM2 | TCacOuItem2Do | CAC组织项目2表 |
| T_CAC_OU_RELATION | TCacOuRelationDo | CAC组织关联表 |
| T_CAC_BALANCE | TCacBalanceDo | CAC余额表 |
| T_CAC_STORE | TCacStoreDo | CAC存储表 |
| T_CAC_VALUE | TCacValueDo | CAC值表 |
| T_CAC_REPORT | TCacReportDo | CAC报告表 |
| T_CAC_ALERT | TCacAlertDo | CAC预警表 |
| T_CAC_ERP_PROCESS | TCacErpProcessDo | CAC ERP流程表 |
| T_CAC_INTERACTIVE_TYPE | TCacInteractiveTypeDo | CAC交互类型表 |
| T_CAC_INVOKERULE8_DETLS | TCacInvokerule8DetlsDo | CAC调用规则8明细表 |
| T_ALERT_CONTROL | TAlertControlDo | 预警控制表 |
| T_RMBS_ERP_AUTO_CLAIM_JOB | TRmbsErpAutoClaimJobDo | ERP自动报账任务表 |
| T_RMBS_ERP_CLAIM_RULE | TRmbsErpClaimRuleDo | ERP报账规则表 |
| T_RMBS_ERP_CLAIM_RULE_CHILD | TRmbsErpClaimRuleChildDo | ERP报账规则子表 |
| T_RMBS_ERP_GLRTBD | TRmbsErpGlrtbdDo | ERP总账RTBD表 |
| T_RMBS_ERP_GLRTBD_HIS | TRmbsErpGlrtbdHisDo | ERP总账RTBD历史表 |
| T_CLAIM_INVOICE_ERP | TClaimInvoiceErpDo | 报账发票ERP表 |
| T_CLAIM_INVOICE_RECORD_LIBRARY | TClaimInvoiceRecordLibraryDo | 报账发票记录库表 |
| T_PI_LOG | TPiLogDo | PI日志表 |

---

## 8. 档案管理服务 (fssc-aam-service) — 21 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| AAM_ARCHIVE | AamArchiveDo | 档案主表 |
| AAM_ARCHIVE_LINE | AamArchiveLineDo | 档案行表 |
| AAM_ARCHIVE_DRAFT | AamArchiveDraftDo | 档案草稿表 |
| AAM_ARCHIVE_DRAFT_LINE | AamArchiveDraftLineDo | 档案草稿行表 |
| AAM_BORROWING_REQ | AamBorrowingReqDo | 借阅请求表 |
| AAM_BORROWING_RULES | AamBorrowingRulesDo | 借阅规则表 |
| AAM_BORROWING_WAITDEAL | AamBorrowingWaitdealDo | 借阅待办表 |
| AAM_BORROWING_ARCHIVE_WAITDEAL | AamBorrowingArchiveWaitdealDo | 借阅归档待办表 |
| AAM_TRANSFER_REQ | AamTransferReqDo | 移交请求表 |
| AAM_TRANSFER_REQ_LINE | AamTransferReqLineDo | 移交请求行表 |
| AAM_TRANSFER_WAITDEAL | AamTransferWaitdealDo | 移交待办表 |
| AAM_RELATION_CHANGE_LOG | AamRelationChangeLogDo | 关联变更日志表 |
| AAM_WAREHOUSE | AamWarehouseDo | 仓库表 |
| AAM_WAREHOUSE_LOCATION | AamWarehouseLocationDo | 仓库位置表 |
| ODM_DOCUMENT_LOG | OdmDocumentLogDo | ODM文档日志表 |
| ODM_PACKAGE | OdmPackageDo | ODM包表 |
| ODM_PACKAGE_LINE | OdmPackageLineDo | ODM包行表 |
| ODM_PACKAGE_LOG | OdmPackageLogDo | ODM包日志表 |
| EBS_INVOICE_PAY_GL | EbsInvoicePayGlDo | EBS发票支付总账表 |
| SHARED_MAILING_ADDRESS | SharedMailingAddressDo | 共享邮寄地址表 |
| t_ebs_logs | TEbsLogsDo | EBS日志表 |

---

## 9. BPM流程服务 (fssc-bpm-service) — 2 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| T_PROCESS_WI_HISTORY | TProcessWiHistoryDo | 流程工作项历史表 |
| T_PROCESS_WI_RECORD_QUEUE | TProcessWiRecordQueueDo | 流程工作项记录队列表 |

---

## 10. 绩效服务 (fssc-pi-service) — 24 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| PERFORMANCE_INDICATOR | PerformanceIndicatorDo | 绩效指标表 |
| PERFORMANCE_SETTING | PerformanceSettingDo | 绩效设置表 |
| PI_INDEX1_CONFIG | PiIndex1ConfigDo | 绩效指标1配置表 |
| T_PI_LOG | TPiLogDo | PI日志表 |
| T_PI_SETTING | TPiSettingDo | PI设置表 |
| T_PI_ELEMENTS | TPiElementsDo | PI元素表 |
| T_PI_FORMULA | TPiFormulaDo | PI公式表 |
| T_PI_FIXED_INDEX | TPiFixedIndexDo | PI固定指标表 |
| T_PI_DEPT_USER | TPiDeptUserDo | PI部门用户表 |
| T_PI_MONTHLY_REPORT | TPiMonthlyReportDo | PI月度报告表 |
| T_PI_PER_CLAIMDEAL | TPiPerClaimdealDo | PI报账处理表 |
| T_PI_PER_VOUCHER | TPiPerVoucherDo | PI凭证表 |
| T_PI_CLAIM_ACCURACY | TPiClaimAccuracyDo | PI报账准确率表 |
| T_PI_ONCE_REPLY_RATIO | TPiOnceReplyRatioDo | PI一次回复率表 |
| T_PI_ORDER_DEALTIME | TPiOrderDealtimeDo | PI订单处理时间表 |
| T_PI_PAY_TIMELY | TPiPayTimelyDo | PI付款及时率表 |
| T_PI_APPRLHOURS_AVG | TPiApprlhoursAvgDo | PI平均审批时长表 |
| T_PI_AUDIT_CONTRACT_TIMELY | TPiAuditContractTimelyDo | PI审计合同及时率表 |
| T_PI_SURRENDER_CREDIT_ACCURACY | TPiSurrenderCreditAccuracyDo | PI退保信用准确率表 |
| T_PI_VIRTUAL_CLAIM_NUMBER | TPiVirtualClaimNumberDo | PI虚拟报账单号表 |
| T_PI_FREIGHT_CLAIM_NUMBER | TPiFreightClaimNumberDo | PI运费报账单号表 |
| T_PI_WRONG_VOUCHER | TPiWrongVoucherDo | PI错误凭证表 |
| T_PI_WRONG_VOUCHER_SET | TPiWrongVoucherSetDo | PI错误凭证设置表 |
| WORK_DAY | WorkDayDo | 工作日表 |

---

## 11. 凭证服务 (fssc-voucher-service) — 8 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| EBS_IMPORT_ASSEMBLY | EbsImportAssemblyDo | EBS导入装配表 |
| EBS_IMPORT_CALLIF | EbsImportCallifDo | EBS导入调用接口表 |
| EBS_IMPORT_MODULE | EbsImportModuleDo | EBS导入模块表 |
| EBS_IMPORT_PROXY | EbsImportProxyDo | EBS导入代理表 |
| EBS_IMPORT_STRUCTURE | EbsImportStructureDo | EBS导入结构表 |
| T_ERP_IMPORT_MQ_JOB | TErpImportMqJobDo | ERP导入MQ任务表 |
| T_MISPROC_CLAIM | TMisprocClaimDo | 异常处理报账表 |
| T_MIS_GL_CODE_COMBINATION | TMisGlCodeCombinationDo | 总账编码组合表 |

---

## 12. 影像服务 (fssc-image-service) — 17 表

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| EIM_IMAGE | EimImageDo | 影像主表 |
| EIM_IMAGE_FILE | EimImageFileDo | 影像文件表 |
| EIM_IMAGE_FILE_OPERATION_LOG | EimImageFileOperationLogDo | 影像文件操作日志表 |
| EIM_IMAGE_DELETE_JOB | EimImageDeleteJobDo | 影像删除任务表 |
| T_ATTACHMENT | TAttachmentDo | 附件表 |
| T_FILE_DETAIL | TFileDetailDo | 文件详情表 |
| T_FILE_PROCESS | TFileProcessDo | 文件处理表 |
| T_FILE_PROCESS_DETAIL | TFileProcessDetailDo | 文件处理详情表 |
| T_APP_INVOICE_FOLDER_OCR_REQ | TAppInvoiceFolderOcrReqDo | 发票夹OCR请求表 |
| T_RMBS_JDR_INVOICE_FOLDER | TRmbsJdrInvoiceFolderDo | 金蝶发票夹表 |
| T_EVENT_EXEC_LOG | TEventExecLogDo | 事件执行日志表 |
| OCR_CALLBACK_OCRINVOICE | OcrCallbackOcrinvoiceDo | OCR回调发票表 |
| OCR_CALLBACK_OCRINVOICE_HIS | OcrCallbackOcrinvoiceHisDo | OCR回调发票历史表 |
| OCR_WEBSERVICE_REQUEST | OcrWebserviceRequestDo | OCR WebService请求表 |
| OCR_WEBSERVICE_REQUEST_HIS | OcrWebserviceRequestHisDo | OCR WebService请求历史表 |
| SYN_TAX_IMAGE_INFO | SynTaxImageInfoDo | 同步税务影像信息表 |
| BACK_TO_TRAVEL_LOG | BackToTravelLogDo | 回退差旅日志表 |

---

## 13. 定时任务服务 (fssc-xxl-job-service) — 90+ 表

> xxl-job 服务复用了大量其他模块的 DO（用于定时任务操作），以下仅列出该模块**独有**的表：

| 表名 | DO 类名 | 说明 |
|------|---------|------|
| BW_IINVOICE_FORMAT_FILE | BwIinvoiceFormatFileDo | 百望发票格式文件表 |
| BW_IINVOICE_FORMAT_FILE_HIS | BwIinvoiceFormatFileHisDo | 百望发票格式文件历史表 |
| BW_IINVOICE_SEND_LOG | BwIinvoiceSendLogDo | 百望发票发送日志表 |
| AAM_AUTO_ARCHIVE_CHECK_POOL | AamAutoArchiveCheckPoolDo | 自动归档检查池表 |
| CLAIM_NO_SEND_MAIL | ClaimNoSendMailDo | 报账单发送邮件表 |
| COM_UNIQ_KEY | ComUniqKeyDo | 公共唯一键表 |
| EBS_FAIL_INVOICE | EbsFailInvoiceDo | EBS失败发票表 |
| EIM_IMAGE_FILE_OCR_LOG | EimImageFileOcrLogDo | 影像文件OCR日志表 |
| HIS_BUSINESS_TRANSACTION_TEMP | HisBusinessTransactionTempDo | 历史业务交易临时表 |
| OCR_CALLBACK_HEAD | OcrCallbackHeadDo | OCR回调头表 |
| OCR_CALLBACK_INVOICEDETAIL | OcrCallbackInvoicedetailDo | OCR回调发票明细表 |
| OCR_CALLBACK_INVOICEMAIN | OcrCallbackInvoicemainDo | OCR回调发票主表 |
| OCR_CALLBACK_INVOICEMAIN_HIS | OcrCallbackInvoicemainHisDo | OCR回调发票主历史表 |
| T_BANK_SYC_DETAIL_CMBC | TBankSycDetailCmbcDo | 银行同步详情招商表 |
| T_FUND_ACCOUNT_INFO | TFundAccountInfoDo | 资金账户信息表 |
| T_FUND_CURRENCY_INFO | TFundCurrencyInfoDo | 资金币种信息表 |
| T_FUND_OFFICE_INFO | TFundOfficeInfoDo | 资金办公信息表 |
| T_FUND_REFUSE_FLOW_SENDMAILLOG | TFundRefuseFlowSendmaillogDo | 资金拒绝流程发邮件日志表 |
| T_MIS_SOA_FSSC_PDFLOG | TMisSoaFsscPdflogDo | SOA FSSC PDF日志表 |
| T_MIS_TERMS | TMisTermsDo | 条款表 |
| T_OFD_INVOICE_REQ | TOfdInvoiceReqDo | OFD发票请求表 |
| T_OVERTIME_UNSETTLED_CLAIM | TOvertimeUnsettledClaimDo | 超时未结报账表 |
| T_RMBS_CLAIM_NOTEND | TRmbsClaimNotendDo | 报账单未结束表 |
| T_RMBS_CLAIM_VOUCHER_REPORT | TRmbsClaimVoucherReportDo | 报账单凭证报告表 |
| T_RMBS_DELAY_IMPORT_CONDITION | TRmbsDelayImportConditionDo | 延迟导入条件表 |
| T_RMBS_PAYLIST_APPOVE | TRmbsPaylistAppoveDo | 支付单审批表 |
| T_DOWN_REPORT_SET | TDownReportSetDo | 下载报告设置表 |
| T_DOWN_REPORT_SET_ISALLOU | TDownReportSetIsAllOuDo | 下载报告全组织设置表 |
| T_CLAIM_INVOICE_RECORD_LIBRARY | Fssc2TaxInvoiceDataDto | 报账发票记录库(定时任务) |
| t_bank_pay | TBankPayDo | 银行支付表 |
| T_RMBS_CLAIM_FPGL_JOB | TRmbsClaimFpglJobDo | 报账单发票管理任务表 |

---

## 快速查表指南

根据 Bug 类型快速定位要查哪个表:

| Bug 场景 | 建议查的表 |
|----------|-----------|
| 报账单保存/提交异常 | T_RMBS_CLAIM + T_RMBS_CLAIM_LINE |
| 支付状态异常 | T_RMBS_PAYLIST + T_RMBS_PAYLIST_FAULT + T_RMBS_PAYLIST_LOCK |
| 会计分组/座席问题 | T_PROC_ACCOUNTANTTEAM + T_PROC_ACCOUNTANTTEAM_USER |
| 会计项目配置问题 | T_CO_ITEMLEVEL2 + T_CO_ITEMLEVEL3 |
| 用户权限问题 | SYS_USER + SYS_USER_ROLE + SYS_ROLEFUNC |
| 字典/参数配置 | T_RMBS_DICT + T_SYS_PARAMETER |
| 接受验收问题 | T_ACPT_BILL + T_ACPT_BILL_LINE_FRONT + T_ACPT_BILL_LINE_BACK |
| 固定资产问题 | T_FA_ASSETS_COST_INFO + T_FA_ASSETS_DEPRN_INFO + T_RMBS_ASSET |
| 发票问题 | BW_IINVOICE_LIB_HEAD + BW_IINVOICE_LIB_LINE + ITM_INVOICE |
| 凭证问题 | T_PAYMENT_VOUCHER + T_VOUCHER_SPILIT |
| 汇率问题 | T_MIS_EXCHANGE_RATE |
| 接口日志 | INTERFACE_LOG + SOAP_LOG_INFO |
| 审批流程问题 | T_PROCESS_WI_RECORD + T_PROCESS_WI_HISTORY |
| 合同问题 | CM_CONTRACT + CM_CONTRACT_TERM + T_LEASE_CONTRACT |
| 差旅问题 | T_RMBS_CLAIM_TRAVEL_LINE + T_CC_QA + SYS_USER_TRAVEL_INFO |
| 规则引擎问题 | T_ENGINE_FORM + T_ENGINE_FORM_RULE + T_ENGINE_CATEGORY |
| CAC审核问题 | T_CAC_TASK + T_CAC_TASK_DETL + T_CAC_RULE |
| OCR识别问题 | OCR_INVOICE_LIBRARY + OCR_RECOG_REPORT + OCR_CALLBACK_OCRINVOICE |
| 影像/附件问题 | EIM_IMAGE + EIM_IMAGE_FILE + T_ATTACHMENT |
| 档案管理问题 | AAM_ARCHIVE + AAM_BORROWING_REQ + AAM_WAREHOUSE |
| 定时任务异常 | T_SCHEDULED_TASKS + T_SCHEDULED_TASKS_LOG |
| 绩效统计问题 | PERFORMANCE_INDICATOR + T_PI_MONTHLY_REPORT |
| 保理/保利问题 | T_FACTOR_DETAIL_INFO + T_RMBS_BAOLICLAIM_CREATE023 |
| 供应商问题 | t_mis_inqvendor + t_mis_inqvendorbank + T_BLACKLIST |
| TPM报账问题 | TPM_CLAIM_AMOUNT + TPM_CLAIM_LINE + TPM_CX_EXEC_INT |
| V2自动报账 | T_V2_AUTO_CLAIM_JOB + T_V2_CREATE_REQ + T_V2_DATA |
| ERP集成问题 | T_SYS_ERP_PARAM + T_RMBS_ERP_CLAIM_RULE + EBS_IMPORT_MODULE |
