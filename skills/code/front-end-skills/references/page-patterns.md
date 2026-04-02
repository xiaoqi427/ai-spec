# 页面模式

## 搜索页最小模式

参考：

- `fssc-web/src/page/accountingDoc/autoArchiveCheckPool`
- `fssc-web/src/page/accountingManage/confirmPaymentList4CDHP`
- `fssc-web/src/page/kpi/operationalAnalysis/itemReport`

典型职责拆分：

- `index.vue` 负责组装 `fssc-search-page`
- `service.js` 负责列表、导出、详情接口封装
- `tableSchemaFile.js` 负责列顺序与列级 `ui:options`

常用技巧：

- 用 `$getSchemaByApiKey` 取后端 bean schema
- 用 `SchemaUtils.replaceSchemaLabels` 改标题
- 用 `SchemaUtils.schemaFiledCustomAppend` 补日期、金额格式
- 用 `SchemaUiUtils.getStartDateOptions/getEndDateOptions` 处理时间区间

## 报账单详情页最小模式

参考：

- `fssc-web/src/page/claim/fund/T065`
- `fssc-web/src/page/claim/fund/T066`

典型职责拆分：

- `index.vue` 装配详情页容器、header、footer、workflow submitter
- `service.js` 统一暴露头信息与行信息 API
- `header/` 放头部卡片或表单
- `table/` 放明细表、礼盒页签、行编辑
- `other/` 放备注、扩展说明、只读区块

常用技巧：

- 尽量复用 `BaseMixin`、`WorkflowMixin`
- itemId 固定后，优先走 `commonApiLoadClaim/commonApiSaveOrUpateData`
- 明细行格式处理优先走 `SchemaUtils + SchemaUiUtils`

## 框架组件模式

参考：

- `fssc-web-framework/src/install.js`
- `fssc-web-framework/src/lib.js`
- `fssc-web-framework/doc/demo/*.md`

落地规则：

- 新组件通常需要“实现 + 注册 + 导出 + demo”
- 文档 demo 直接描述组件用法，不要把业务逻辑写进框架
- 公共能力优先沉到 framework，业务拼装留在 `fssc-web`
