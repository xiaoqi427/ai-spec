# SIT 环境页面路由映射

## 环境地址

| 环境 | URL |
|------|-----|
| SIT | `http://pri-fssc-web-sit.digitalyili.com` |
| UAT | `http://pri-fssc-web-uat.digitalyili.com` |
| 旧测试 | `http://10.60.137.24:8888/fssc/login.jsp` |

## 报账单页面路由

| 模板编号 | 路由路径 | 业务模块 | 说明 |
|----------|---------|---------|------|
| T001 | `/#/claim/T001` | TR | 差旅报账 |
| T002 | `/#/claim/T002` | TR | 差旅报账(变体) |
| T010 | `/#/claim/T010` | PTP | 采购报账 |
| T044 | `/#/claim/T044` | OTC | 杂项采购报账 |
| T045 | `/#/claim/T045` | OTC | 物流报账 |
| T046 | `/#/claim/T046` | OTC | 杂项报账(变体) |
| T047 | `/#/claim/T047` | EER | 费用报账 |
| T048 | `/#/claim/T048` | EER | 费用报账(变体) |
| T049 | `/#/claim/T049` | EER | 杂项费用报账 |
| T050 | `/#/claim/T050` | EER | 费用报账(变体) |
| T051 | `/#/claim/T051` | OTC | 税单报账 |
| T052 | `/#/claim/T052` | OTC | 税单报账(变体) |
| T060 | `/#/claim/T060` | RTR | 应收报账 |
| T061 | `/#/claim/T061` | FA | 资产报账 |
| T065 | `/#/claim/T065` | TR | 差旅特殊报账 |
| T071 | `/#/claim/T071` | BASE | 规则引擎配置 |

## 其他常用页面路由

| 功能 | 路由路径 | 说明 |
|------|---------|------|
| 首页 | `/#/home` | 系统首页 |
| 我的待办 | `/#/myInfo/myTodo` | 待办工作 |
| 我的已办 | `/#/myInfo/myDone` | 已办工作 |
| 凭证管理 | `/#/voucher` | 财务凭证 |
| 归档管理 | `/#/archive` | 文档归档 |

## 路由注意事项

1. SIT 环境使用 hash 路由模式 (`/#/`)
2. 报账单详情页通常需要 query 参数:
   - `claimId` - 报账单ID
   - `itemId` - 模板编号
   - `archiveId` - 归档ID (某些场景)
3. 示例完整 URL:
   ```
   http://pri-fssc-web-sit.digitalyili.com/#/claim/T044?claimId=123&itemId=T044
   ```
4. 如果路由不确定，使用路由解析脚本:
   ```bash
   python3 ai-spec/skills/code/front-end-skills/scripts/route-open.py T044
   ```

## Swagger API 文档地址 (SIT/UAT)

| 模块 | API 文档 URL |
|------|-------------|
| claim | `http://pri-fssc-api-uat.digitalyili.com/api/claim/v3/api-docs` |
| otc | `http://pri-fssc-api-uat.digitalyili.com/api/claim/otc/otc/v3/api-docs` |
| eer | `http://pri-fssc-api-uat.digitalyili.com/api/claim/eer/eer/v3/api-docs` |
| ptp | `http://pri-fssc-api-uat.digitalyili.com/api/claim/ptp/ptp/v3/api-docs` |
| rtr | `http://pri-fssc-api-uat.digitalyili.com/api/claim/rtr/rtr/v3/api-docs` |
| tr | `http://pri-fssc-api-uat.digitalyili.com/api/claim/tr/tr/v3/api-docs` |
| fa | `http://pri-fssc-api-uat.digitalyili.com/api/claim/fa/fa/v3/api-docs` |
| config | `http://pri-fssc-api-uat.digitalyili.com/api/config/v3/api-docs` |
