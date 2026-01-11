# MyBatis-Plus CRUD 代码生成提示词

## 概述

本文档基于 `RmbsPoAgriProConfigController` 作为模板，详细说明如何生成完整的 MyBatis-Plus CRUD 功能代码。该模板遵循标准的多层架构设计，包含 Controller、Service、Mapper、DO、DTO 等完整调用链路。

---

## 架构层次说明

### 分层结构
```
fssc-claim-service/claim-[服务名]/
├── claim-[服务名]-web/          # Web层 - Controller
├── claim-[服务名]-service/      # 服务层 - Service接口、实现、DTO、Converter
└── claim-[服务名]-do/           # 数据对象层 - DO实体类
```

### 模块依赖关系
```
claim-[服务名]-web 
  ↓ 依赖
claim-[服务名]-service 
  ↓ 依赖
claim-[服务名]-do
```

---

## 第一步：创建数据库实体类 (DO)

### 位置
`claim-[服务名]-do/src/main/java/com/yili/claim/[服务名]/[模块名]/entity/[实体名]Do.java`

### 提示词模板

````
请在 claim-[服务名]-do 模块中创建实体类 [实体名]Do，要求如下：

**包路径**：`com.yili.claim.[服务名].[模块名].entity`

**类信息**：
- 类名：[实体名]Do
- 表名：[数据库表名]
- 继承：TenantBaseDO（包含租户、创建人、修改人等公共字段）
- 注解：
  - @Getter、@Setter、@ToString（使用Lombok）
  - @TableName("[数据库表名]")
  - @Schema(name = "[实体名]Do", description = "[业务描述]")

**字段定义**:
[列出所有字段,格式如下]
- 字段名:id
  - 类型:Long（主键统一使用Long类型）
  - 数据库列:ID
  - 注解:@TableId("ID")、@Schema(description = "主键")
  - 说明:主键

- 字段名:[字段名]
  - 类型:[Java类型]
  - 数据库列:[数据库列名]
  - 注解:@TableField("[数据库列名]")、@Schema(description = "[字段说明]")
  - 说明:[业务说明]

**字段命名规范**:
- **Java字段名必须严格遵循驼峰命名法(camelCase)**
- 数据库列名转Java字段名规则:
  - 下划线分隔的大写列名 → 驼峰命名:USER_NAME → userName, TEAM_ID → teamId, COMP_ID → compId
  - 全大写无下划线的列名 → 首字母小写驼峰:ISENABLE → isEnable, SEATSTATE → seatState, GROUPLEADER → groupLeader
  - 特殊前缀处理:IS_开头的布尔字段保持is前缀,如IS_REVIEW_ACCOUNT → isReviewAccount
- **重要:每个继承TenantBaseDO的实体类必须显式定义COMP_ID字段**
- **TENANT_CODE已在TenantBaseDO中定义,不需要在子类中重复定义**
- **BaseDO是空基类,没有任何字段定义**
- MyBatis-Plus会自动处理驼峰命名与下划线命名的转换,但必须确保@TableField注解中的列名与数据库完全一致

**DO类开发约束**:
- **严禁在DO类中新增字段** (这是强制规定)
- DO类只能映射数据库表中已存在的字段
- 如需扩展字段,必须在对应的DTO类中添加

**示例参考**:RmbsPoAgriProConfigDo
```

### 代码模板

```java
package com.yili.claim.[服务名].[模块名].entity;

import com.yili.common.db.base.DO.TenantBaseDO;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * <p>
 * [业务描述]
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Getter
@Setter
@ToString
@TableName("[数据库表名]")
@Schema(name = "[实体名]Do", description = "[业务描述]")
public class [实体名]Do extends TenantBaseDO {

    /**
     * 主键
     */
    @TableId("ID")
    @Schema(description = "主键")
    private Long id;

    /**
     * [字段说明]
     */
    @TableField("[数据库列名]")
    @Schema(description = "[字段说明]")
    private [类型] [字段名];

    // ... 其他字段
}

/**
 * 字段类型规范：
 * - 主键ID：统一使用 Long 类型
 * - 外键ID：统一使用 Long 类型
 * - 数值型：Short → Long（推荐使用Long以避免溢出）
 * - 日期时间：使用 LocalDateTime（包含时分秒）
 * - 年月日：使用 LocalDate（仅年月日）
 */
```

---

## 第二步：创建 Mapper 接口

### 位置
`claim-[服务名]-service/src/main/java/com/yili/claim/[服务名]/[模块名]/mapper/[实体名]DoMapper.java`

### 提示词模板

````
请在 claim-[服务名]-service 模块中创建 Mapper 接口 [实体名]DoMapper，要求如下：

**包路径**：`com.yili.claim.[服务名].[模块名].mapper`

**接口信息**：
- 接口名：[实体名]DoMapper
- 继承：BaseMapper<[实体名]Do>
- 注解：@Mapper
- 说明：BaseMapper 是 MyBatis-Plus 提供的基础 CRUD 接口

**示例参考**：RmbsPoAgriProConfigDoMapper
```

### 代码模板

```java
package com.yili.claim.[服务名].[模块名].mapper;

import com.yili.common.db.mybatis.mapper.BaseMapperX;
import com.yili.claim.[服务名].[模块名].entity.[实体名]Do;
import org.apache.ibatis.annotations.Mapper;

/**
 * <p>
 * [业务描述] Mapper 接口
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Mapper
public interface [实体名]DoMapper extends BaseMapperX<[实体名]Do> {
}
```

---

## 第三步：创建 DTO 类

### 位置
`claim-[服务名]-service/src/main/java/com/yili/claim/[服务名]/[模块名]/dto/`

### 提示词模板

```
请在 claim-[服务名]-service 模块中创建以下 DTO 类：

### 3.1 主 DTO - [实体名]Dto

**包路径**：`com.yili.claim.[服务名].[模块名].dto`

**类信息**：
- 类名：[实体名]Dto
- 继承：[实体名]Do（继承DO，复用字段定义）
- 注解：
  - @Getter、@Setter、@ToString
  - @Schema(name = "[实体名]Dto",description = "[业务描述]")

**额外字段**（如需要）：
[列出DTO中额外的查询或展示字段]

### 3.2 删除 DTO - [实体名]DelDto

**类信息**：
- 类名：[实体名]DelDto
- 继承：[实体名]Do
- 注解：@Getter、@Setter、@ToString、@Schema

**字段**：
- ids: List<Long>
  - 注解：@NotEmpty、@Schema(description = "ids")
  - 说明：批量删除的ID列表

### 3.3 导出 DTO - [实体名]ExportDto

**包路径**：`com.yili.claim.[服务名].[模块名].dto`（注意：导出DTO放在service模块下）

**类信息**：
- 类名：[实体名]ExportDto
- 不继承DO（独立定义需要导出的字段）
- 注解：@Data、@Schema

**字段**（每个需要导出的字段）：
- 注解：@ExcelProperty("[Excel列名]", index = [序号])
- 不需要导出的字段：@ExcelIgnore

**示例参考**：
- RmbsPoAgriProConfigDto
- RmbsPoAgriProConfigDelDto
- RmbsPoAgriProConfigExportDto
```

### 代码模板

#### 主 DTO
```java
package com.yili.claim.[服务名].[模块名].dto;

import com.yili.claim.[服务名].[模块名].entity.[实体名]Do;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * <p>
 * [业务描述] DTO
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Getter
@Setter
@ToString
@Schema(name = "[实体名]Dto",description = "[业务描述]")
public class [实体名]Dto extends [实体名]Do {
    
    /**
     * 申请开始日期（查询参数）
     */
    @Schema(description = "申请开始日期")
    private LocalDateTime applyStartDate;
    
    /**
     * 申请结束日期（查询参数）
     */
    @Schema(description = "申请结束日期")
    private LocalDateTime applyEndDate;
}
```

#### 删除 DTO
```java
package com.yili.claim.[服务名].[模块名].dto;

import com.yili.claim.[服务名].[模块名].entity.[实体名]Do;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.List;

/**
 * <p>
 * [业务描述] 删除 DTO
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Getter
@Setter
@ToString
@Schema(name = "[实体名]DelDto",description = "[业务描述]")
public class [实体名]DelDto extends [实体名]Do {

    @NotEmpty
    @Schema(description = "ids")
    private List<Long> ids;
}
```

#### 导出 DTO
```java
package com.yili.claim.[服务名].[模块名].dto;

import com.alibaba.excel.annotation.ExcelIgnore;
import com.alibaba.excel.annotation.ExcelProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * <p>
 * [业务描述] 导出 DTO
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Data
@Schema(name = "[实体名]ExportDto",description = "[业务描述]")
public class [实体名]ExportDto {

    @ExcelIgnore
    @Schema(description = "主键")
    private Long id;

    @ExcelProperty(value = "[Excel列名]", index = 0)
    @Schema(description = "[字段说明]")
    private [类型] [字段名];

    // ... 其他需要导出的字段
}
```

---

## 第四步：创建 Converter 转换器

### 位置
`claim-[服务名]-service/src/main/java/com/yili/claim/[服务名]/[模块名]/converter/`

### 提示词模板

```
请在 claim-[服务名]-service 模块中创建 Converter 接口，使用 MapStruct 进行对象转换：

**包路径**：`com.yili.claim.[服务名].[模块名].converter`

**接口信息**：
- 接口名：[实体名]DtoConverter
- 继承：BaseConverter<[实体名]Dto, [实体名]Do>
- 注解：@Mapper(componentModel = "spring")
- 说明：提供 Dto 与 Do 之间的双向转换

**自定义方法**：
- toExportDtoList：将 DO 列表转换为导出 DTO 列表

**示例参考**：RmbsPoAgriProConfigDtoConverter
```

### 代码模板

```java
package com.yili.claim.[服务名].[模块名].converter;

import com.yili.claim.[服务名].[模块名].dto.[实体名]Dto;
import com.yili.claim.[服务名].[模块名].entity.[实体名]Do;
import com.yili.claim.[服务名].[模块名].dto.[实体名]ExportDto;
import com.yili.common.db.mybatis.pojo.BaseMapperConverter;
import org.mapstruct.Mapper;

import java.util.List;

/**
 * [实体名]DtoConverter：DTO 与 DO 之间的 MapStruct 转换器接口
 *
 * @author Generator
 * @since [日期]
 */
@Mapper(componentModel = "spring")
public interface [实体名]DtoConverter extends BaseMapperConverter<[实体名]Do, [实体名]Dto> {
    
    /**
     * 将 DO 列表转换为导出 DTO 列表
     *
     * @param list DO 列表
     * @return 导出 DTO 列表
     */
    List<[实体名]ExportDto> toExportDtoList(List<[实体名]Do> list);
}
```

---

## 第五步：创建 Facade 服务层

### 位置
`claim-[服务名]-service/src/main/java/com/yili/claim/[服务名]/[模块名]/facade/`

### 提示词模板

```
请在 claim-[服务名]-service 模块中创建 Facade 层接口和实现类：

### 5.1 接口 - I[实体名]DoService

**包路径**：`com.yili.claim.[服务名].[模块名].facade`

**接口信息**：
- 接口名：I[实体名]DoService
- 继承：IService<[实体名]Do>
- 说明：IService 是 MyBatis-Plus 提供的基础服务接口

**自定义方法**：
1. page - 分页查询
   - 参数：UserObjectFullDto user, PageParam<[实体名]Dto, [实体名]Dto> param
   - 返回：Page<[实体名]Dto>
   
2. export - 导出
   - 参数：PageParam<[实体名]Dto, [实体名]Dto> params, UserObjectFullDto user, HttpServletResponse response
   - 返回：void

### 5.2 实现类 - [实体名]DoServiceImpl

**包路径**：`com.yili.claim.[服务名].[模块名].facade.impl`

**类信息**：
- 类名：[实体名]DoServiceImpl
- 继承：BaseDoXService<[实体名]Dto, [实体名]Do, [实体名]DoMapper, [实体名]DtoConverter>
- 实现：I[实体名]DoService
- 注解：@Service

**示例参考**：
- IRmbsPoAgriProConfigDoService
- RmbsPoAgriProConfigDoServiceImpl
```

### 代码模板

#### 接口
```java
package com.yili.claim.[服务名].[模块名].facade;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.claim.[服务名].[模块名].dto.[实体名]Dto;
import com.yili.common.db.base.service.IBaseDoXService;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.claim.[服务名].[模块名].entity.[实体名]Do;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;

/**
 * <p>
 * [业务描述] Facade 服务类
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
public interface I[实体名]DoService extends IBaseDoXService<[实体名]Dto, [实体名]Do> {

    /**
     * 分页查询
     *
     * @param user  当前用户
     * @param param 查询参数
     * @return 分页结果
     */
    Page<[实体名]Dto> page(UserObjectFullDto user, PageParam<[实体名]Dto, [实体名]Dto> param);

    /**
     * 导出
     *
     * @param params   查询参数
     * @param user     当前用户
     * @param response HTTP响应
     */
    void export(PageParam<[实体名]Dto, [实体名]Dto> params, UserObjectFullDto user, HttpServletResponse response);
}
```

#### 实现类
```java
package com.yili.claim.[服务名].[模块名].facade.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.claim.[服务名].[模块名].dto.[实体名]Dto;
import com.yili.claim.[服务名].[模块名].entity.[实体名]Do;
import com.yili.claim.[服务名].[模块名].converter.[实体名]DtoConverter;
import com.yili.claim.[服务名].[模块名].dto.[实体名]ExportDto;
import com.yili.claim.[服务名].[模块名].facade.I[实体名]DoService;
import com.yili.claim.[服务名].[模块名].mapper.[实体名]DoMapper;
import com.yili.common.db.base.service.BaseDoXService;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import com.yili.fssc.util.excel.EasyExcelWriteUtil;
import jakarta.servlet.http.HttpServletResponse;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;

import jakarta.annotation.Resource;
import java.util.Collections;
import java.util.List;

/**
 * <p>
 * [业务描述] Facade 服务实现类
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Service
public class [实体名]DoServiceImpl extends BaseDoXService<[实体名]Dto, [实体名]Do, [实体名]DoMapper, [实体名]DtoConverter> implements I[实体名]DoService {

    @Resource
    private [实体名]DtoConverter [实体名小写]DtoConverter;


    @Override
    public Page<[实体名]Dto> page(UserObjectFullDto user, PageParam<[实体名]Dto, [实体名]Dto> param) {
        // 权限控制逻辑（根据实际需求调整）
        if (user == null) {
            user = new UserObjectFullDto();
        }
        
        // TODO: 添加数据权限过滤
        // if (!user.isAdmin()) {
        //     param.getParams().setCompId(user.getCurCompId().toString());
        // }

        return mapper.page([实体名小写]DtoConverter, param);
    }

    @Override
    @SneakyThrows
    public void export(PageParam<[实体名]Dto, [实体名]Dto> params, UserObjectFullDto user, HttpServletResponse response) {
        PageParam<[实体名]Dto, [实体名]Dto> pageParam = params == null ? new PageParam<>() : params;
        if (pageParam.getParams() == null) {
            pageParam.setParams(new [实体名]Dto());
        }
        pageParam.setPageNum(1);
        pageParam.setPageSize(Long.MAX_VALUE);

        Page<[实体名]Dto> page = page(user, pageParam);

        List<[实体名]ExportDto> records = page == null ? Collections.emptyList() : [实体名小写]DtoConverter.toExportDtoList(page.getRecords());
        EasyExcelWriteUtil.fileName("[业务名称]")
                .sheet("[业务名称]", 0, records, [实体名]ExportDto.class)
                .doWrite(response);
    }
}
```

---

## 第六步：创建 Service 业务层

### 位置
`claim-[服务名]-service/src/main/java/com/yili/claim/[服务名]/[模块名]/service/`

### 提示词模板

```
请在 claim-[服务名]-service 模块中创建 Service 业务层接口和实现类：

### 6.1 接口 - [实体名]Service

**包路径**：`com.yili.claim.[服务名].[模块名].service`

**接口信息**：
- 接口名：[实体名]Service
- 不继承任何接口
- 说明：定义业务方法

**方法定义**：
1. page - 分页查询
2. deleteByIds - 批量删除
3. selectById - 根据ID查询
4. save - 新增或更新
5. export - 导出

### 6.2 实现类 - [实体名]ServiceImpl

**包路径**：`com.yili.claim.[服务名].[模块名].service.impl`

**类信息**：
- 类名：[实体名]ServiceImpl
- 继承：BaseDoXService<[实体名]Dto, [实体名]Do, [实体名]DoMapper, [实体名]DtoConverter>
- 实现：[实体名]Service
- 注解：@Service

**依赖注入**：
- I[实体名]DoService（Facade层）
- [实体名]DoMapper

**示例参考**：
- RmbsPoAgriProConfigService
- RmbsPoAgriProConfigServiceImpl
```

### 代码模板

#### 接口
```java
package com.yili.claim.[服务名].[模块名].service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.claim.[服务名].[模块名].dto.[实体名]Dto;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;

import java.util.List;

/**
 * <p>
 * [业务描述] 业务服务类
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
public interface [实体名]Service {

    /**
     * 分页查询
     *
     * @param user  当前用户
     * @param param 查询参数
     * @return 分页结果
     */
    Page<[实体名]Dto> page(UserObjectFullDto user, PageParam<[实体名]Dto, [实体名]Dto> param);

    /**
     * 批量删除
     *
     * @param ids ID列表
     * @return 删除数量
     */
    int deleteByIds(List<Long> ids);

    /**
     * 根据ID查询
     *
     * @param id 主键ID
     * @return DTO对象
     */
    [实体名]Dto selectById(Long id);

    /**
     * 新增或更新
     *
     * @param dto DTO对象
     * @return 保存后的DTO对象
     */
    [实体名]Dto save([实体名]Dto dto);

    /**
     * 导出
     *
     * @param params   查询参数
     * @param user     当前用户
     * @param response HTTP响应
     */
    void export(PageParam<[实体名]Dto, [实体名]Dto> params, UserObjectFullDto user, HttpServletResponse response);
}
```

#### 实现类
```java
package com.yili.claim.[服务名].[模块名].service.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.claim.[服务名].[模块名].dto.[实体名]Dto;
import com.yili.claim.[服务名].[模块名].entity.[实体名]Do;
import com.yili.claim.[服务名].[模块名].converter.[实体名]DtoConverter;
import com.yili.claim.[服务名].[模块名].facade.I[实体名]DoService;
import com.yili.claim.[服务名].[模块名].mapper.[实体名]DoMapper;
import com.yili.claim.[服务名].[模块名].service.[实体名]Service;
import com.yili.common.db.base.service.BaseDoXService;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jakarta.annotation.Resource;
import java.util.List;

/**
 * <p>
 * [业务描述] 业务服务实现类
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Service
public class [实体名]ServiceImpl extends BaseDoXService<[实体名]Dto, [实体名]Do, [实体名]DoMapper, [实体名]DtoConverter> implements [实体名]Service {

    @Autowired
    I[实体名]DoService i[实体名]DoService;

    @Resource
    [实体名]DoMapper [实体名小写]DoMapper;

    @Override
    public Page<[实体名]Dto> page(UserObjectFullDto user, PageParam<[实体名]Dto, [实体名]Dto> param) {
        return i[实体名]DoService.page(user, param);
    }

    @Override
    public int deleteByIds(List<Long> ids) {
        return [实体名小写]DoMapper.deleteBatchIds(ids);
    }

    @Override
    public [实体名]Dto selectById(Long id) {
        [实体名]Do entity = [实体名小写]DoMapper.selectById(id);
        return converter.toDto(entity);
    }

    @Override
    public [实体名]Dto save([实体名]Dto dto) {
        [实体名]Do entity = converter.toDo(dto);
        if (entity.getId() == null) {
            // 新增
            [实体名小写]DoMapper.insert(entity);
        } else {
            // 更新
            [实体名小写]DoMapper.updateById(entity);
        }
        return converter.toDto(entity);
    }

    @Override
    public void export(PageParam<[实体名]Dto, [实体名]Dto> params, UserObjectFullDto user, HttpServletResponse response) {
        i[实体名]DoService.export(params, user, response);
    }
}
```

---

## 第七步：创建 Controller

### 位置
`claim-[服务名]-web/src/main/java/com/yili/claim/[服务名]/web/controller/[模块名]/[实体名]Controller.java`

### 提示词模板

```
请在 claim-[服务名]-web 模块中创建 Controller 类 [实体名]Controller，要求如下：

**包路径**：`com.yili.claim.[服务名].web.controller.[模块名]`

**类信息**：
- 类名：[实体名]Controller
- 注解：
  - @Controller
  - @RequestMapping("/[实体小写名称]-do")
  - @Tag(name = "([服务名])[菜单路径]")
  - @Schema(description = "[业务描述]")

**依赖注入**：
- [实体名]Service（注解：@Autowired）

**接口方法**：

### 1. page - 分页查询
- 路径：POST /page
- 参数：PageParam<[实体名]Dto, [实体名]Dto>
- 返回：Page<[实体名]Dto>

### 2. deleteByIds - 批量删除
- 路径：POST /delete-by-ids
- 参数：[实体名]DelDto（包含 ids 列表）
- 返回：int
- 校验：@Validated

### 3. getById - 根据ID查询
- 路径：POST /get-by-id
- 参数：[实体名]Dto（包含 id: Long）
- 返回：[实体名]Dto
- 校验：@Validated

### 4. save - 新增或更新
- 路径：POST /save
- 参数：[实体名]Dto
- 返回：[实体名]Dto
- 校验：@Validated

### 5. export - 导出
- 路径：POST /export
- 参数：PageParam<[实体名]Dto, [实体名]Dto>、HttpServletResponse
- 返回：void

**注解说明**：
- @Operation：Swagger接口文档注解（summary、description）
- @ResponseBody：返回JSON
- @RequestBody：接收JSON请求体
- @Validated：参数校验

**示例参考**：RmbsPoAgriProConfigController
```

### 代码模板

```java
package com.yili.claim.[服务名].web.controller.[模块名];

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.claim.[服务名].[模块名].dto.[实体名]DelDto;
import com.yili.claim.[服务名].[模块名].dto.[实体名]Dto;
import com.yili.claim.[服务名].[模块名].service.[实体名]Service;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.sys.api.config.UserThreadLocal;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

/**
 * <p>
 * [业务描述] 前端控制器
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Controller
@Schema(description = "[业务描述]")
@Tag(name = "([服务名])[菜单路径]")
@RequestMapping("/[实体小写名称]-do")
public class [实体名]Controller {
    
    @Autowired
    [实体名]Service [实体名小写]Service;

    /**
     * 分页查询
     */
    @PostMapping("/page")
    @Operation(summary = "查询[业务名称]", description = "查询[业务名称]")
    @ResponseBody
    public Page<[实体名]Dto> page(@RequestBody PageParam<[实体名]Dto, [实体名]Dto> param) {
        UserObjectFullDto user = UserThreadLocal.get();
        return [实体名小写]Service.page(user, param);
    }

    /**
     * 批量删除
     */
    @PostMapping("/delete-by-ids")
    @Operation(summary = "删除[业务名称]", description = "删除[业务名称]")
    @ResponseBody
    public int deleteByIds(@RequestBody @Validated [实体名]DelDto param) {
        List<Long> ids = param.getIds();
        return [实体名小写]Service.deleteByIds(ids);
    }

    /**
     * 根据ID查询
     */
    @ResponseBody
    @Operation(summary = "获取[业务名称]", description = "获取[业务名称]")
    @PostMapping(value = "/get-by-id")
    public [实体名]Dto getById(@RequestBody @Validated [实体名]Dto dto) {
        Long id = dto.getId();
        return [实体名小写]Service.selectById(id);
    }

    /**
     * 新增或更新
     */
    @ResponseBody
    @Operation(summary = "保存[业务名称]", description = "保存[业务名称]")
    @PostMapping(value = "/save")
    public [实体名]Dto save(@RequestBody @Validated [实体名]Dto dto) {
        return [实体名小写]Service.save(dto);
    }

    /**
     * 导出
     */
    @ResponseBody
    @PostMapping("/export")
    @Operation(summary = "导出", description = "依据查询条件导出")
    public void export(@RequestBody PageParam<[实体名]Dto, [实体名]Dto> params,
                       @Schema(hidden = true) UserObjectFullDto user,
                       HttpServletResponse response) {
        [实体名小写]Service.export(params, user, response);
    }
}
```

---

## 完整调用链路说明

### 请求流程
```
HTTP 请求
  ↓
Controller (claim-[服务名]-web)
  - 接收请求参数（DTO）
  - 参数校验 (@Validated)
  - 调用 Service
  ↓
Service (claim-[服务名]-service/service)
  - 业务逻辑处理
  - 调用 Facade
  ↓
Facade (claim-[服务名]-service/facade)
  - 数据访问逻辑
  - 权限控制
  - 数据转换（DTO ↔ DO）
  - 调用 Mapper
  ↓
Mapper (claim-[服务名]-service/mapper)
  - MyBatis-Plus 基础方法
  ↓
Database
```

### 数据转换流程
```
前端 JSON
  ↓ Jackson
Controller: DTO
  ↓ (直接传递)
Service: DTO
  ↓ (直接传递)
Facade: DTO
  ↓ Converter
Facade: DO
  ↓ Mapper
Database
  ↓ MyBatis
Facade: DO
  ↓ Converter
Facade: DTO
  ↓ (直接返回)
Service: DTO
  ↓ (直接返回)
Controller: DTO
  ↓ Jackson
前端 JSON
```

---

## 关键技术点说明

### 1. BaseDoXService 基础服务
- 提供通用 CRUD 方法
- 自动处理类型转换

### 2. BaseMapper
- MyBatis-Plus 的基础 Mapper
- 提供基础 CRUD 方法

### 3. BaseConverter 对象转换
- MapStruct 转换器基类
- 提供 toDto 和 toDo 方法

### 4. 分页查询
- PageParam<P, R>：查询参数
- Page<T>：分页结果

### 5. Excel 导出
- EasyExcelWriteUtil：导出工具
- @ExcelProperty：定义导出列

### 6. 参数校验
- @Validated：启用校验
- @NotEmpty：非空集合
- @NotNull：非空对象

---

## 代码生成步骤总结

### 按顺序执行以下步骤：

1. **创建 DO 实体类**（claim-[服务名]-do）
   - 定义数据库表映射
   - 添加字段注解
   - **严禁新增字段**

2. **创建 Mapper 接口**（claim-[服务名]-service/mapper）
   - 继承 BaseMapper

3. **创建 DTO 类**（claim-[服务名]-api-param + claim-[服务名]-service）
   - 主 DTO（继承 DO）
   - 删除 DTO（包含 ids）
   - 导出 DTO（Excel 注解，放在 service 模块）

4. **创建 Converter 接口**（claim-[服务名]-service/converter）
   - 继承 BaseConverter
   - 添加导出转换方法

5. **创建 Facade 层**（claim-[服务名]-service/facade）
   - 接口：继承 IService
   - 实现：继承 BaseDoXService

6. **创建 Service 层**（claim-[服务名]-service/service）
   - 接口：定义业务方法
   - 实现：继承 BaseDoXService，调用 Facade

7. **创建 Controller**（claim-[服务名]-web）
   - 定义接口路由
   - 参数校验
   - 调用 Service

---

## 常见问题和注意事项

### 1. 包命名规范 (farmproduce 模块)
- DO：`com.yili.claim.[服务名].farmproduce.entity`
- Mapper：`com.yili.claim.[服务名].farmproduce.mapper`
- Facade：`com.yili.claim.[服务名].farmproduce.facade`
- Service：`com.yili.claim.[服务名].farmproduce.service`
- DTO：`com.yili.claim.[服务名].farmproduce.dto`
- Converter：`com.yili.claim.[服务名].farmproduce.converter`
- Controller：`com.yili.claim.[服务名].web.controller.farmproduce`

### 2. 命名规范
- DO 类：[实体名]Do
- DTO 类：[实体名]Dto
- Mapper 接口：[实体名]DoMapper
- Facade 接口：I[实体名]DoService
- Facade 实现：[实体名]DoServiceImpl
- Service 接口：[实体名]Service
- Service 实现：[实体名]ServiceImpl
- Controller：[实体名]Controller

### 3. 注解使用
- DO：@Getter、@Setter、@ToString（Lombok）
- DTO：@Getter、@Setter、@ToString 或 @Data（Lombok）
- Service/Facade：@Service
- Controller：@Controller
- Converter：@Mapper(componentModel = "spring")
- Mapper：@Mapper

### 4. 依赖注入
- Service 注入 Facade：@Autowired 或 @Resource
- Service 注入 Mapper：@Resource
- Converter 注入：自动注入

### 5. 数据库字段映射
- @TableName:表名
- @TableId:主键（统一使用 Long）
- @TableField:普通字段
- **字段名映射规则(严格遵循)**:
  - 数据库列名统一使用大写+下划线格式
  - Java字段名统一使用驼峰命名法
  - MyBatis-Plus 自动处理驼峰↔下划线转换

### 6. DO 类约束
- **严禁在 DO 类中新增字段**
- DO 只映射数据库表字段
- 扩展字段必须在 DTO 中添加

### 7. 新增/修改判断
- 通过 `id == null` 判断新增
- 通过 `id != null` 判断修改

### 8. 日期类型规范
- 完整时间戳(年月日时分秒)：`LocalDateTime`
- 仅年月日：`LocalDate`

---

## 总结

本文档提供了完整的 MyBatis-Plus CRUD 代码生成指南，涵盖从数据库实体到前端接口的所有层次。使用本模板可以快速生成标准化、规范化的业务代码，提高开发效率并保证代码质量。

**核心要点**：
1. 严格遵循分层架构（Controller → Service → Facade → Mapper）
2. 统一的命名规范
3. DO 类禁止新增字段
4. 主键统一使用 Long 类型
5. 日期类型规范（LocalDateTime/LocalDate）
6. 完整的类型转换
7. 规范的接口文档

**建议**：
- 先理解调用链路，再进行代码生成
- 保持各层职责单一
- 合理使用基类方法
- 注重代码复用性
- 先确认模块名和包结构
- DO 字段必须与数据库表字段一致
- 确认后再创建文件
