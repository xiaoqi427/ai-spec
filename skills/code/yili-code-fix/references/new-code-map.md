# 新代码目录结构映射

## 后端根目录

```
fssc-claim-service/
├── claim-base/                             # 公共基础模块
│   └── claim-base-service/
│       └── src/main/java/com/yili/claim/base/
│           ├── claim/                      # 报账单公共逻辑
│           │   ├── head/                   # 头逻辑
│           │   │   ├── business/           # Business 层
│           │   │   ├── service/            # DO Service 层
│           │   │   └── impl/
│           │   └── line/                   # 行逻辑
│           ├── common/                     # 通用服务
│           └── config/                     # 配置
├── claim-common/                           # 通用工具模块
├── claim-tr/                               # 差旅报账模块 (T001-T009, T065)
│   └── claim-tr-service/
│       └── src/main/java/com/yili/claim/tr/claim/
│           ├── t001/
│           │   ├── head/
│           │   │   ├── IT001NewClaimService.java
│           │   │   ├── IT001SaveClaimService.java
│           │   │   ├── IT001DeleteClaimService.java
│           │   │   ├── IT001LoadClaimService.java
│           │   │   ├── IT001SubmitClaimService.java
│           │   │   ├── IT001CallBackClaimService.java
│           │   │   └── impl/
│           │   │       ├── T001NewClaimServiceImpl.java
│           │   │       ├── T001SaveClaimServiceImpl.java
│           │   │       └── ...
│           │   └── line/
│           │       ├── IT001NewClaimLineService.java
│           │       └── impl/
│           └── t065/
├── claim-otc/                              # 杂项报账模块 (T044-T046, T051-T052)
│   └── claim-otc-service/
│       └── src/main/java/com/yili/claim/otc/claim/
│           ├── t044/
│           ├── t045/
│           ├── t046/
│           ├── t051/
│           └── t052/
├── claim-ptp/                              # 采购报账模块 (T010-T019)
│   └── claim-ptp-service/
│       └── src/main/java/com/yili/claim/ptp/claim/
│           └── t010/
├── claim-eer/                              # 费用报账模块 (T047-T050)
│   └── claim-eer-service/
│       └── src/main/java/com/yili/claim/eer/claim/
│           ├── t047/
│           ├── t048/
│           ├── t049/
│           └── t050/
├── claim-fa/                               # 资产报账模块 (T061-T069)
│   └── claim-fa-service/
│       └── src/main/java/com/yili/claim/fa/claim/
│           ├── t061/
│           └── ...
└── claim-rtr/                              # 应收报账模块 (T060)
    └── claim-rtr-service/
        └── src/main/java/com/yili/claim/rtr/claim/
            └── t060/
```

## 每个模板目录下的标准文件结构

```
t{xxx}/
├── head/                                   # 报账单头逻辑
│   ├── IT{XXX}NewClaimService.java         # 新建头接口
│   ├── IT{XXX}SaveClaimService.java        # 保存头接口
│   ├── IT{XXX}DeleteClaimService.java      # 删除头接口
│   ├── IT{XXX}LoadClaimService.java        # 加载头接口
│   ├── IT{XXX}SubmitClaimService.java      # 提交接口
│   ├── IT{XXX}CallBackClaimService.java    # 回调接口
│   └── impl/                              # 实现类
│       ├── T{XXX}NewClaimServiceImpl.java
│       ├── T{XXX}SaveClaimServiceImpl.java
│       ├── T{XXX}DeleteClaimServiceImpl.java
│       ├── T{XXX}LoadClaimServiceImpl.java
│       ├── T{XXX}SubmitClaimServiceImpl.java
│       └── T{XXX}CallBackClaimServiceImpl.java
└── line/                                   # 报账单行逻辑
    ├── IT{XXX}NewClaimLineService.java
    ├── IT{XXX}SaveClaimLineService.java
    ├── IT{XXX}UpdateClaimLineService.java
    ├── IT{XXX}DeleteClaimLineService.java
    ├── IT{XXX}LoadClaimLineService.java
    └── impl/
        └── ...
```

## 前端目录

```
fssc-web/
├── src/
│   ├── page/
│   │   └── claim/
│   │       ├── base/                       # 报账单公共组件
│   │       │   └── service.js
│   │       ├── T001/                       # 差旅报账
│   │       │   ├── index.vue
│   │       │   ├── service.js
│   │       │   ├── header/
│   │       │   └── table/
│   │       ├── T044/                       # 杂项采购
│   │       └── ...
│   ├── config/
│   │   └── route/                          # 路由配置
│   └── json-schema/                        # Schema 文件
```

## 新老代码类名对照速查

| 步骤 | 老代码类名 | 新代码类名 | 基类 |
|------|-----------|-----------|------|
| New头 | `NewT{XXX}ClaimService` | `T{XXX}NewClaimServiceImpl` | `BaseNewClaimService` |
| New行 | `NewT{XXX}ClaimLineService` | `T{XXX}NewClaimLineServiceImpl` | `BaseNewClaimLineService` |
| Save头 | `Insert/UpdateT{XXX}ClaimService` | `T{XXX}SaveClaimServiceImpl` | `BaseSaveOrUpdateClaimService` |
| Save行 | `Insert/UpdateT{XXX}ClaimLineService` | `T{XXX}SaveClaimLineServiceImpl` | `BaseSave/UpdateClaimLineService` |
| Delete头 | `DeleteT{XXX}ClaimService` | `T{XXX}DeleteClaimServiceImpl` | `BaseDeleteClaimService` |
| Delete行 | `DeleteT{XXX}ClaimLinesService` | `T{XXX}DeleteClaimLineServiceImpl` | `BaseDeleteClaimLineService` |
| Load | `LoadAllT{XXX}Service` + `ViewT{XXX}*` | `T{XXX}LoadClaimServiceImpl` | `BaseLoadClaimService` |
| Callback | `CallBackT{XXX}Service` | `T{XXX}CallBackClaimServiceImpl` | `BaseCallBackClaimService` |
| Submit | `SubmitT{XXX}Service` | `T{XXX}SubmitClaimServiceImpl` | `BaseSubmitClaimService` |
| Load行 | `ListAllT{XXX}ClaimLinesService` | `T{XXX}LoadClaimLineService` | `BaseLoadClaimLineService` |

## 快速定位技巧

- 用模板编号定位: `find fssc-claim-service -type d -name "t044"`
- 用类名搜索: `grep -r "T044SaveClaimServiceImpl" fssc-claim-service/`
- 前端页面定位: `find fssc-web/src/page/claim -type d -name "T044"`
