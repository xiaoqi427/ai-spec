# 包路径规则

## 模板变量说明

模板文件中只有一个服务相关变量 `[服务名]`，生成代码时替换为目标服务名：

| 目标服务 | `[服务名]` 替换为 |
|----------|-------------------|
| fssc-config-service | `config` |
| fssc-claim-service/claim-ptp | `claim.ptp` |
| fssc-fund-service | `fund` |
| fssc-invoice-service | `invoice` |
| fssc-cac-service | `cac` |

替换后包路径示例（以 config 为例）：
- DO: `com.yili.config.entity.[模块名]`
- 业务层: `com.yili.config.service.[模块名].mapper/dto/facade/service`
- Controller: `com.yili.config.web.controller.[模块名]`

> **注意**：`com.yili.config.sys.api.*` 是公共模块（来自 `fssc-config-sys`），所有服务共用，不需要替换。

## fssc-config-service

```
fssc-config-do/        com.yili.config.entity.[模块名]          → DO
fssc-config-service/   com.yili.config.service.[模块名].mapper   → Mapper
                       com.yili.config.service.[模块名].dto      → DTO
                       com.yili.config.service.[模块名].converter → Converter
                       com.yili.config.service.[模块名].facade    → Facade接口
                       com.yili.config.service.[模块名].facade.impl → Facade实现
                       com.yili.config.service.[模块名].service   → Service接口
                       com.yili.config.service.[模块名].service.impl → Service实现
fssc-config-web/       com.yili.config.web.controller.[模块名]   → Controller
resources/mapper/com/yili/config/[模块名]/                       → Mapper XML
```

## fssc-claim-service（如 claim-ptp）

```
claim-ptp-do/          com.yili.claim.ptp.entity.[模块名]       → DO
claim-ptp-service/     com.yili.claim.ptp.service.[模块名].mapper   → Mapper
                       com.yili.claim.ptp.service.[模块名].dto      → DTO
                       com.yili.claim.ptp.service.[模块名].converter → Converter
                       com.yili.claim.ptp.service.[模块名].facade    → Facade接口
                       com.yili.claim.ptp.service.[模块名].facade.impl → Facade实现
                       com.yili.claim.ptp.service.[模块名].service   → Service接口
                       com.yili.claim.ptp.service.[模块名].service.impl → Service实现
claim-web/             com.yili.claim.ptp.web.controller.[模块名] → Controller
resources/mapper/com/yili/claim/ptp/[模块名]/                    → Mapper XML
```

## 其他服务（fssc-fund-service 等）

包路径模式参考上方变量对照表，以目标服务中已有代码确认实际路径。

## 文件位置速查（以 fssc-config-service 为例）

| 层级 | 文件路径 |
|------|----------|
| DO | `fssc-config-do/src/main/java/com/yili/config/entity/[模块名]/[实体名]Do.java` |
| Mapper | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/mapper/[实体名]DoMapper.java` |
| Mapper XML | `fssc-config-service/src/main/resources/mapper/com/yili/config/[模块名]/[实体名]DoMapper.xml` |
| DTO | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/dto/[实体名]Dto.java` |
| DelDTO | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/dto/[实体名]DelDto.java` |
| ExportDTO | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/dto/[实体名]ExportDto.java` |
| Converter | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/converter/[实体名]DtoConverter.java` |
| Facade接口 | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/facade/I[实体名]DoService.java` |
| Facade实现 | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/facade/impl/[实体名]DoServiceImpl.java` |
| Service接口 | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/service/[实体名]Service.java` |
| Service实现 | `fssc-config-service/src/main/java/com/yili/config/service/[模块名]/service/impl/[实体名]ServiceImpl.java` |
| Controller | `fssc-config-web/src/main/java/com/yili/config/web/controller/[模块名]/[实体名]Controller.java` |
