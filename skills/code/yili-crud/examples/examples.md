# 完整示例：认证权限配置 CRUD

> 基于 `fssc-config-service` 项目中 `TRmbsInvoiceAuthentication` 模块的真实代码。

## 基本信息

| 项目 | 值 |
|------|------|
| 目标服务 | `fssc-config-service` |
| 模块名 | `common` |
| 实体名 | `TRmbsInvoiceAuthentication` |
| 数据库表名 | `T_RMBS_INVOICE_AUTHENTICATION` |
| 序列名 | `SEQ_INVOICE_AUTHENTICATION` |
| 业务描述 | 发票税号认证权限配置 |
| 菜单路径 | 系统运维/基础数据配置/通用/认证权限配置 |

---

## 文件清单

```
fssc-config-do/
└── src/main/java/com/yili/config/entity/common/
    └── TRmbsInvoiceAuthenticationDo.java

fssc-config-service/
├── src/main/java/com/yili/config/service/common/
│   ├── mapper/
│   │   └── TRmbsInvoiceAuthenticationDoMapper.java
│   ├── dto/
│   │   ├── TRmbsInvoiceAuthenticationDto.java
│   │   ├── TRmbsInvoiceAuthenticationDelDto.java
│   │   └── TRmbsInvoiceAuthenticationExportDto.java
│   ├── converter/
│   │   └── TRmbsInvoiceAuthenticationDtoConverter.java
│   ├── facade/
│   │   ├── ITRmbsInvoiceAuthenticationDoService.java
│   │   └── impl/
│   │       └── TRmbsInvoiceAuthenticationDoServiceImpl.java
│   └── service/
│       ├── TRmbsInvoiceAuthenticationService.java
│       └── impl/
│           └── TRmbsInvoiceAuthenticationServiceImpl.java
└── src/main/resources/mapper/com/yili/config/common/
    └── TRmbsInvoiceAuthenticationDoMapper.xml

fssc-config-web/
└── src/main/java/com/yili/config/web/controller/common/
    └── TRmbsInvoiceAuthenticationController.java
```

---

## 1. DO 实体类

```java
package com.yili.config.entity.common;

import com.baomidou.mybatisplus.annotation.KeySequence;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.yili.common.db.base.DO.TenantBaseDO;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;

/**
 * 发票税号认证权限配置
 *
 * @author sevenxiao
 * @since 2025-12-15
 */
@Getter
@Setter
@ToString
@TableName("T_RMBS_INVOICE_AUTHENTICATION")
@Schema(name = "TRmbsInvoiceAuthenticationDo", description = "发票税号")
@KeySequence("SEQ_INVOICE_AUTHENTICATION")
public class TRmbsInvoiceAuthenticationDo extends TenantBaseDO {

    @TableId("ID")
    @Schema(description = "主键")
    private Long id;

    @TableField("TAX_NUMBER")
    @Schema(description = "税号")
    private String taxNumber;

    @Schema(description = "入账OU")
    @TableField("RUZHANG_ORG_ID")
    private Long ruzhangOrgId;

    @Schema(description = "入账OU名称")
    @TableField("RUZHANG_ORG_NAME")
    private String ruzhangOrgName;

    @TableField("CHOICE_USER_ID")
    @Schema(description = "勾选人信息")
    private Long choiceUserId;

    @TableField("CHOICE_USER_NAME")
    @Schema(description = "勾选人编码")
    private String choiceUserName;

    @TableField("CHOICE_FULL_NAME")
    @Schema(description = "勾选人名称")
    private String choiceFullName;

    @TableField("COMP_ID")
    @Schema(description = "公司ID")
    private Long compId;

    @TableField("UPD_DATE")
    @Schema(description = "修改时间")
    private LocalDateTime updDate;

    @TableField("UPD_USER_ID")
    @Schema(description = "修改人ID")
    private String updUserId;

    @TableField("UPD_USER_NAME")
    @Schema(description = "修改人")
    private String updUserName;

    @TableField("UPD_FULL_NAME")
    @Schema(description = "修改人姓名")
    private String updFullName;
}
```

## 2. Mapper

```java
package com.yili.config.service.common.mapper;

import com.yili.common.db.mybatis.mapper.BaseMapperX;
import com.yili.config.entity.common.TRmbsInvoiceAuthenticationDo;

/**
 * 发票税号认证权限配置 Mapper
 *
 * @author sevenxiao
 * @since 2025-12-15
 */
public interface TRmbsInvoiceAuthenticationDoMapper
        extends BaseMapperX<TRmbsInvoiceAuthenticationDo> {
}
```

## 3. DTO

```java
package com.yili.config.service.common.dto;

import com.yili.config.entity.common.TRmbsInvoiceAuthenticationDo;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(name = "TRmbsInvoiceAuthenticationDto", description = "发票税号")
public class TRmbsInvoiceAuthenticationDto extends TRmbsInvoiceAuthenticationDo {
    // DTO 可以覆盖 DO 字段并添加校验注解
    // 也可以添加数据库中不存在的扩展字段
}
```

## 4. DtoConverter

```java
package com.yili.config.service.common.converter;

import com.yili.common.db.mybatis.pojo.BaseMapperConverter;
import com.yili.config.entity.common.TRmbsInvoiceAuthenticationDo;
import com.yili.config.service.common.dto.TRmbsInvoiceAuthenticationDto;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface TRmbsInvoiceAuthenticationDtoConverter
        extends BaseMapperConverter<TRmbsInvoiceAuthenticationDo, TRmbsInvoiceAuthenticationDto> {
}
```

## 5. Facade 接口

```java
package com.yili.config.service.common.facade;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.base.service.IBaseDoXService;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.entity.common.TRmbsInvoiceAuthenticationDo;
import com.yili.config.service.common.dto.TRmbsInvoiceAuthenticationDto;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;

import java.util.List;

public interface ITRmbsInvoiceAuthenticationDoService
        extends IBaseDoXService<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDo> {

    Page<TRmbsInvoiceAuthenticationDto> page(UserObjectFullDto user,
            PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> param);

    int deleteByIds(List<Long> ids);

    void export(PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> params,
                UserObjectFullDto user, HttpServletResponse response);
}
```

## 6. Facade 实现

```java
package com.yili.config.service.common.facade.impl;

import cn.hutool.core.bean.BeanUtil;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.base.service.BaseDoXService;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.entity.common.TRmbsInvoiceAuthenticationDo;
import com.yili.config.service.common.converter.TRmbsInvoiceAuthenticationDtoConverter;
import com.yili.config.service.common.dto.TRmbsInvoiceAuthenticationDto;
import com.yili.config.service.common.dto.TRmbsInvoiceAuthenticationExportDto;
import com.yili.config.service.common.facade.ITRmbsInvoiceAuthenticationDoService;
import com.yili.config.service.common.mapper.TRmbsInvoiceAuthenticationDoMapper;
import com.yili.config.sys.api.config.UserThreadLocal;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import com.yili.fssc.util.excel.EasyExcelWriteUtil;
import jakarta.servlet.http.HttpServletResponse;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

@Service
public class TRmbsInvoiceAuthenticationDoServiceImpl
        extends BaseDoXService<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDo,
                TRmbsInvoiceAuthenticationDoMapper, TRmbsInvoiceAuthenticationDtoConverter>
        implements ITRmbsInvoiceAuthenticationDoService {

    @Override
    public Page<TRmbsInvoiceAuthenticationDto> page(UserObjectFullDto user,
            PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> param) {
        if (!user.isAdmin()) {
            // 权限过滤逻辑
        }
        return mapper.page(converter, param);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public TRmbsInvoiceAuthenticationDto save(TRmbsInvoiceAuthenticationDto bean) {
        UserObjectFullDto user = UserThreadLocal.get();
        LocalDateTime now = LocalDateTime.now();
        bean.setUpdDate(now);
        bean.setUpdUserId(user.getUserid());
        bean.setUpdUserName(user.getUsername());
        return super.save(bean);
    }

    @Override
    public int deleteByIds(List<Long> ids) {
        return mapper.deleteByIds(ids);
    }

    @Override
    @SneakyThrows
    public void export(PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> params,
                       UserObjectFullDto user, HttpServletResponse response) {
        PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> pageParam =
                params == null ? new PageParam<>() : params;
        if (pageParam.getParams() == null) {
            pageParam.setParams(new TRmbsInvoiceAuthenticationDto());
        }
        pageParam.setPageNum(1);
        pageParam.setPageSize(Long.MAX_VALUE);

        Page<TRmbsInvoiceAuthenticationDto> page = page(user, pageParam);
        List<TRmbsInvoiceAuthenticationExportDto> records = page == null
                ? Collections.emptyList()
                : BeanUtil.copyToList(page.getRecords(), TRmbsInvoiceAuthenticationExportDto.class);

        EasyExcelWriteUtil.fileName("认证权限配置")
                .sheet("认证权限配置", 0, records, TRmbsInvoiceAuthenticationExportDto.class)
                .doWrite(response);
    }
}
```

## 7. Service 接口

```java
package com.yili.config.service.common.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.service.common.dto.TRmbsInvoiceAuthenticationDto;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;

import java.util.List;

public interface TRmbsInvoiceAuthenticationService {

    Page<TRmbsInvoiceAuthenticationDto> page(UserObjectFullDto user,
            PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> param);

    TRmbsInvoiceAuthenticationDto selectById(Long id);

    TRmbsInvoiceAuthenticationDto save(TRmbsInvoiceAuthenticationDto dto);

    int deleteByIds(List<Long> ids);

    void export(PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> params,
                UserObjectFullDto user, HttpServletResponse response);
}
```

## 8. Service 实现

```java
package com.yili.config.service.common.service.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.service.common.dto.TRmbsInvoiceAuthenticationDto;
import com.yili.config.service.common.facade.ITRmbsInvoiceAuthenticationDoService;
import com.yili.config.service.common.service.TRmbsInvoiceAuthenticationService;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TRmbsInvoiceAuthenticationServiceImpl
        implements TRmbsInvoiceAuthenticationService {

    @Autowired
    private ITRmbsInvoiceAuthenticationDoService itRmbsInvoiceAuthenticationDoService;

    @Override
    public Page<TRmbsInvoiceAuthenticationDto> page(UserObjectFullDto user,
            PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> param) {
        return itRmbsInvoiceAuthenticationDoService.page(user, param);
    }

    @Override
    public TRmbsInvoiceAuthenticationDto selectById(Long id) {
        return itRmbsInvoiceAuthenticationDoService.selectById(id);
    }

    @Override
    public TRmbsInvoiceAuthenticationDto save(TRmbsInvoiceAuthenticationDto dto) {
        // 复杂业务逻辑在此处理
        return itRmbsInvoiceAuthenticationDoService.save(dto);
    }

    @Override
    public int deleteByIds(List<Long> ids) {
        return itRmbsInvoiceAuthenticationDoService.deleteByIds(ids);
    }

    @Override
    @SneakyThrows
    public void export(PageParam<TRmbsInvoiceAuthenticationDto, TRmbsInvoiceAuthenticationDto> params,
                       UserObjectFullDto user, HttpServletResponse response) {
        itRmbsInvoiceAuthenticationDoService.export(params, user, response);
    }
}
```

## 9. Controller

```java
package com.yili.config.web.controller.common;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.service.common.dto.TRmbsInvoiceAuthenticationDelDto;
import com.yili.config.service.common.dto.TRmbsInvoiceAuthenticationDto;
import com.yili.config.service.common.service.TRmbsInvoiceAuthenticationService;
import com.yili.config.sys.api.config.UserThreadLocal;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@Schema(description = "系统运维-通用-认证权限配置")
@Tag(name = "系统运维/基础数据配置/通用/认证权限配置")
@RequestMapping("/rmbs-invoice-authentication-do")
public class TRmbsInvoiceAuthenticationController {

    @Autowired
    TRmbsInvoiceAuthenticationService tRmbsInvoiceAuthenticationService;

    @PostMapping("/page")
    @Operation(summary = "查询认证权限", description = "查询认证权限")
    @ResponseBody
    public Page<TRmbsInvoiceAuthenticationDto> page(
            @RequestBody PageParam<TRmbsInvoiceAuthenticationDto,
                    TRmbsInvoiceAuthenticationDto> param) {
        UserObjectFullDto user = UserThreadLocal.get();
        return tRmbsInvoiceAuthenticationService.page(user, param);
    }

    @PostMapping("/delete-by-ids")
    @Operation(summary = "删除认证权限", description = "删除认证权限")
    @ResponseBody
    public int deleteByIds(
            @RequestBody @Validated TRmbsInvoiceAuthenticationDelDto param) {
        List<Long> ids = param.getIds();
        return tRmbsInvoiceAuthenticationService.deleteByIds(ids);
    }

    @PostMapping("/get-by-id")
    @Operation(summary = "获取认证权限", description = "获取认证权限")
    @ResponseBody
    public TRmbsInvoiceAuthenticationDto getById(
            @RequestBody @Validated TRmbsInvoiceAuthenticationDto dto) {
        Long id = dto.getId();
        return tRmbsInvoiceAuthenticationService.selectById(id);
    }

    @PostMapping("/save")
    @Operation(summary = "保存认证权限", description = "保存认证权限")
    @ResponseBody
    public TRmbsInvoiceAuthenticationDto save(
            @RequestBody @Validated TRmbsInvoiceAuthenticationDto dto) {
        return tRmbsInvoiceAuthenticationService.save(dto);
    }

    @PostMapping("/export")
    @Operation(summary = "导出", description = "依据查询条件导出")
    @ResponseBody
    public void export(
            @RequestBody PageParam<TRmbsInvoiceAuthenticationDto,
                    TRmbsInvoiceAuthenticationDto> params,
            HttpServletResponse response) {
        UserObjectFullDto user = UserThreadLocal.get();
        tRmbsInvoiceAuthenticationService.export(params, user, response);
    }
}
```

---

## 调用链路总结

```
TRmbsInvoiceAuthenticationController
  ↓ @Autowired
TRmbsInvoiceAuthenticationService (接口)
  ↓ implements
TRmbsInvoiceAuthenticationServiceImpl
  ↓ @Autowired
ITRmbsInvoiceAuthenticationDoService (Facade接口)
  ↓ implements
TRmbsInvoiceAuthenticationDoServiceImpl (extends BaseDoXService)
  ↓ 自动注入 mapper & converter
TRmbsInvoiceAuthenticationDoMapper (extends BaseMapperX)
  ↓
Database: T_RMBS_INVOICE_AUTHENTICATION
```
