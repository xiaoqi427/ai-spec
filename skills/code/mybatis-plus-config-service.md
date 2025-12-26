# MyBatis-Plus CRUD 代码生成提示词 (fssc-config-service)

## 概述

本文档基于 `TRmbsInvoiceAuthenticationController` 作为模板，详细说明如何生成完整的 MyBatis-Plus CRUD 功能代码。该模板遵循标准的多层架构设计，包含 Controller、Service、Mapper、DO、DTO 等完整调用链路。

---

## 架构层次说明

### 分层结构
```
fssc-config-service/
├── fssc-config-web/          # Web层 - Controller
├── fssc-config-service/      # 服务层 - Service接口和实现
├── fssc-config-do/           # 数据对象层 - DO实体类
├── fssc-config-api-param/    # 参数层 - DTO和Converter
└── fssc-config-api/          # API层 - Feign接口
```

### 模块依赖关系
```
fssc-config-web 
  ↓ 依赖
fssc-config-service 
  ↓ 依赖
fssc-config-do + fssc-config-api-param
```

---

## 第一步：创建数据库实体类 (DO)

### 位置
`fssc-config-do/src/main/java/com/yili/config/[模块名]/DO/[实体名]Do.java`

### 提示词模板

````
请在 fssc-config-do 模块中创建实体类 [实体名]Do，要求如下：

**包路径**：`com.yili.config.[模块名].DO`

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

**示例参考**:TRmbsInvoiceAuthenticationDo
```

### 代码模板

```java
package com.yili.config.[模块名].DO;

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
`fssc-config-service/src/main/java/com/yili/config/[模块名]/mapper/[实体名]DoMapper.java`

### 提示词模板

````
请在 fssc-config-service 模块中创建 Mapper 接口 [实体名]DoMapper，要求如下：

**包路径**：`com.yili.config.[模块名].mapper`

**接口信息**：
- 接口名：[实体名]DoMapper
- 继承：BaseMapperX<[实体名]Do>
- 说明：BaseMapperX 是项目封装的 MyBatis-Plus Mapper，提供基础 CRUD 方法

**示例参考**：TRmbsInvoiceAuthenticationDoMapper
```

### 代码模板

```java
package com.yili.config.[模块名].mapper;

import com.yili.common.db.mybatis.mapper.BaseMapperX;
import com.yili.config.[模块名].DO.[实体名]Do;

/**
 * <p>
 * [业务描述] Mapper 接口
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
public interface [实体名]DoMapper extends BaseMapperX<[实体名]Do> {
}
```

---

## 第二步（补充）：创建 Mapper XML 文件

### 位置
`fssc-config-service/src/main/resources/mapper/com/yili/config/[模块名]/[实体名]DoMapper.xml`

### 提示词模板

```
请在 fssc-config-service 模块的 resources 目录下创建 Mapper XML 文件 [实体名]DoMapper.xml，要求如下：

**文件路径**：`fssc-config-service/src/main/resources/mapper/com/yili/config/[模块名]/[实体名]DoMapper.xml`

**XML 配置**：
- namespace：com.yili.config.[模块名].mapper.[实体名]DoMapper
- 说明：基础 CRUD 由 MyBatis-Plus 提供，XML 文件用于自定义 SQL（如需要）

**示例参考**：TRmbsInvoiceAuthenticationDoMapper.xml
```

### 代码模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.yili.config.[模块名].mapper.[实体名]DoMapper">

</mapper>
```

### 说明

1. **目录结构**：
   - Mapper XML 文件必须放在 `resources/mapper/com/yili/config/[模块名]/` 目录下
   - 目录结构与 Java 包结构保持一致

2. **namespace**：
   - 必须与 Mapper 接口的完全限定名一致
   - 格式：`com.yili.config.[模块名].mapper.[实体名]DoMapper`

3. **自定义 SQL**：
   - 如果需要复杂查询，可以在此文件中添加自定义 SQL
   - MyBatis-Plus 的基础 CRUD 方法不需要在 XML 中定义

4. **示例（带自定义查询）**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.yili.config.[模块名].mapper.[实体名]DoMapper">

    <!-- 自定义查询示例 -->
    <select id="selectByCustomCondition" resultType="com.yili.config.[模块名].DO.[实体名]Do">
        SELECT * FROM [表名]
        WHERE 1=1
        <if test="param1 != null">
            AND COLUMN1 = #{param1}
        </if>
    </select>

</mapper>
```

---

## 第三步：创建 DTO 类

### 位置
`fssc-config-api-param/src/main/java/com/yili/config/api/param/[模块名]/dto/`

### 提示词模板

```
请在 fssc-config-api-param 模块中创建以下 DTO 类：

### 3.1 主 DTO - [实体名]Dto

**包路径**：`com.yili.config.api.param.[模块名].dto`

**类信息**：
- 类名：[实体名]Dto
- 继承：[实体名]Do（继承DO，复用字段定义）
- 注解：
  - @Data
  - @Schema(name = "[实体名]", description = "[业务描述]")

**额外字段**（如需要）：
[列出DTO中额外的查询或展示字段]

### 3.2 删除 DTO - [实体名]DelDto

**类信息**：
- 类名：[实体名]DelDto
- 继承：[实体名]Do
- 注解：@Data、@Schema

**字段**：
- ids: List<Long>
  - 注解：@NotEmpty、@Schema(description = "ids")
  - 说明：批量删除的ID列表

### 3.3 导出 DTO - [实体名]ExportDto

**类信息**：
- 类名：[实体名]ExportDto
- 不继承DO（独立定义需要导出的字段）
- 注解：@Data、@Schema

**字段**（每个需要导出的字段）：
- 注解：@ExcelProperty("[Excel列名]")
- 不需要导出的字段：@ExcelIgnore

**示例参考**：
- TRmbsInvoiceAuthenticationDto
- TRmbsInvoiceAuthenticationDelDto
- TRmbsInvoiceAuthenticationExportDto
```

### 代码模板

#### 主 DTO
```java
package com.yili.config.api.param.[模块名].dto;

import com.yili.config.[模块名].DO.[实体名]Do;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * <p>
 * [业务描述] DTO
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Data
@Schema(name = "[实体名]Dto", description = "[业务描述]")
public class [实体名]Dto extends [实体名]Do {
    
    // 可以添加额外的查询字段或展示字段
}
```

#### 删除 DTO
```java
package com.yili.config.api.param.[模块名].dto;

import com.yili.config.[模块名].DO.[实体名]Do;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

import java.util.List;

/**
 * <p>
 * [业务描述] 删除 DTO
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Data
@Schema(name = "[实体名]DelDto", description = "[业务描述]")
public class [实体名]DelDto extends [实体名]Do {

    @NotEmpty
    @Schema(description = "ids")
    private List<Long> ids;
}
```

#### 导出 DTO
```java
package com.yili.config.api.param.[模块名].dto;

import com.alibaba.excel.annotation.ExcelIgnore;
import com.alibaba.excel.annotation.ExcelProperty;
import com.alibaba.excel.annotation.format.DateTimeFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * <p>
 * [业务描述] 导出 DTO
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Data
@Schema(name = "[实体名]ExportDto", description = "[业务描述]")
public class [实体名]ExportDto {

    @ExcelProperty("[Excel列名]")
    @Schema(description = "[字段说明]")
    private [类型] [字段名];

    @ExcelIgnore
    @Schema(description = "主键")
    private Long id;

    @ExcelProperty("[Excel列名]")
    @DateTimeFormat("yyyy-MM-dd HH:mm:ss")
    @Schema(description = "[日期字段说明]")
    private LocalDateTime [日期字段];

    // ... 其他需要导出的字段
}
```

---

## 第四步：创建 Converter 转换器

### 位置
`fssc-config-api-param/src/main/java/com/yili/config/api/param/[模块名]/converter/`

### 提示词模板

```
请在 fssc-config-api-param 模块中创建以下 Converter 接口，使用 MapStruct 进行对象转换：


### 4.2 DtoConverter - [实体名]DtoConverter

**接口信息**：
- 接口名：[实体名]DtoConverter
- 继承：BaseMapperConverter<[实体名]Do, [实体名]Dto>
- 注解：@Mapper(componentModel = "spring")
- 说明：Do 转 Dto

**示例参考**：
- TRmbsInvoiceAuthenticationDoConverter
- TRmbsInvoiceAuthenticationDtoConverter
```

### 代码模板

#### DoConverter (Dto → Do)
```java
package com.yili.config.api.param.[模块名].converter;

import com.yili.common.db.mybatis.pojo.BaseMapperConverter;
import com.yili.config.[模块名].DO.[实体名]Do;
import com.yili.config.api.param.[模块名].dto.[实体名]Dto;
import org.mapstruct.Mapper;

/**
 * [实体名]DoConverter：将 [实体名]Dto（DTO）转换为 [实体名]Do（DO）的 MapStruct Converter 接口
 *
 * @author Generator
 * @since [日期]
 */
@Mapper(componentModel = "spring")
public interface [实体名]DoConverter extends BaseMapperConverter<[实体名]Dto, [实体名]Do> {
}
```

#### DtoConverter (Do → Dto)
```java
package com.yili.config.api.param.[模块名].converter;

import com.yili.config.api.param.[模块名].dto.[实体名]Dto;
import com.yili.config.[模块名].DO.[实体名]Do;
import com.yili.common.db.mybatis.pojo.BaseMapperConverter;
import org.mapstruct.Mapper;

/**
 * [实体名]DtoConverter：将 [实体名]Do（DO）转换为 [实体名]Dto（DTO）的 MapStruct Converter 接口
 *
 * @author Generator
 * @since [日期]
 */
@Mapper(componentModel = "spring")
public interface [实体名]DtoConverter extends BaseMapperConverter<[实体名]Do, [实体名]Dto> {
}
```

---

## 第五步：创建 Service 接口

### 位置
`fssc-config-service/src/main/java/com/yili/config/[模块名]/service/I[实体名]DoService.java`

### 提示词模板

```
请在 fssc-config-service 模块中创建 Service 接口 I[实体名]DoService，要求如下：

**包路径**：`com.yili.config.[模块名].service`

**接口信息**：
- 接口名：I[实体名]DoService
- 继承：IBaseDoService<[实体名]Do>
- 说明：IBaseDoService 提供基础的 CRUD 方法（save、selectById、update等）

**自定义方法**（根据业务需要）：
1. page - 分页查询
   - 参数：UserObjectFullDto user, PageParam<[实体名]Dto, [实体名]Dto> param
   - 返回：Page<[实体名]Dto>
   - 说明：直接返回DTO分页结果
   
2. deleteByIds - 批量删除
   - 参数：List<Long> ids
   - 返回：int

3. selectById - 根据ID查询
   - 参数：Long id
   - 返回：[实体名]Dto
   - 说明：直接返回DTO对象

4. save - 新增或更新
   - 参数：[实体名]Dto dto
   - 返回：[实体名]Dto
   - 说明：接收DTO，返回DTO

5. export - 导出
   - 参数：PageParam<[实体名]Dto, [实体名]Dto> params, UserObjectFullDto user, HttpServletResponse response
   - 返回：void

**示例参考**：ITRmbsInvoiceAuthenticationDoService
```

### 代码模板

```java
package com.yili.config.[模块名].service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.api.param.[模块名].dto.[实体名]Dto;
import com.yili.config.[模块名].DO.[实体名]Do;
import com.yili.common.db.base.service.IBaseDoService;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;

import java.util.List;

/**
 * <p>
 * [业务描述] 服务类
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
public interface I[实体名]DoService extends IBaseDoService<[实体名]Do> {

    /**
     * 分页查询
     *
     * @param user  当前用户
     * @param param 查询参数
     * @return 分页结果（直接返回DTO）
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

---

## 第六步：创建 Service 实现类

### 位置
`fssc-config-service/src/main/java/com/yili/config/[模块名]/service/impl/[实体名]DoServiceImpl.java`

### 提示词模板

```
请在 fssc-config-service 模块中创建 Service 实现类 [实体名]DoServiceImpl，要求如下：

**包路径**：`com.yili.config.[模块名].service.impl`

**类信息**：
- 类名：[实体名]DoServiceImpl
- 继承：BaseDoService<[实体名]Do, [实体名]DoMapper>
- 实现：I[实体名]DoService
- 注解：@Service

**依赖注入**：
- [实体名]DtoConverter（Do → Dto 转换器）
- [实体名]DoConverter（Dto → Do 转换器）
- 注解：@Resource

**方法实现**：

### 1. page 方法
- 权限控制：根据用户角色过滤数据（admin、proAdmin等）
- 调用：mapper.page(converter, param)
- 返回：Page<DTO>（直接返回DTO分页结果）
- 说明：BaseMapperX 提供的分页方法，自动转换DO到DTO

### 2. save 方法
- 接收：DTO参数
- 转换：使用DoConverter将DTO转换为DO
- 设置审计字段：updDate、updUserId、updUserName
- 新增时设置：crtDate、crtUserId、crtUserName
- 调用：super.save(do)
- 返回：使用DtoConverter将保存后的DO转换为DTO返回

### 3. selectById 方法
- 调用：super.selectById(id) 获取DO
- 转换：使用DtoConverter将DO转换为DTO
- 返回：DTO对象

### 4. deleteByIds 方法
- 批量删除：mapper.deleteByIds(ids)

### 5. export 方法
- 查询所有数据（设置 pageSize 为 Long.MAX_VALUE）
- 转换为 ExportDto
- 使用 EasyExcelWriteUtil 导出

**示例参考**：TRmbsInvoiceAuthenticationDoServiceImpl
```

### 代码模板

```java
package com.yili.config.[模块名].service.impl;

import cn.hutool.core.bean.BeanUtil;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.api.param.[模块名].converter.[实体名]DoConverter;
import com.yili.config.api.param.[模块名].converter.[实体名]DtoConverter;
import com.yili.config.api.param.[模块名].dto.[实体名]Dto;
import com.yili.config.api.param.[模块名].dto.[实体名]ExportDto;
import com.yili.config.[模块名].DO.[实体名]Do;
import com.yili.common.db.base.service.BaseDoService;
import com.yili.config.[模块名].mapper.[实体名]DoMapper;
import com.yili.config.[模块名].service.I[实体名]DoService;
import com.yili.config.sys.api.config.UserThreadLocal;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import com.yili.fssc.util.excel.EasyExcelWriteUtil;
import jakarta.servlet.http.HttpServletResponse;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;

import jakarta.annotation.Resource;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

/**
 * <p>
 * [业务描述] 服务实现类
 * </p>
 *
 * @author Generator
 * @since [日期]
 */
@Service
public class [实体名]DoServiceImpl extends BaseDoService<[实体名]Do, [实体名]DoMapper> implements I[实体名]DoService {

    @Resource
    private [实体名]DtoConverter [实体名小写]DtoConverter;

    @Resource
    private [实体名]DoConverter [实体名小写]DoConverter;


    @Override
    public Page<[实体名]Dto> page(UserObjectFullDto user, PageParam<[实体名]Dto, [实体名]Dto> param) {

        if (user == null) {
            user = new UserObjectFullDto();
        }
        if (!user.isAdmin()) {
            //param.getParams().setCompId(user.getCurCompId().toString());

            if (!user.isProAdmin()) {
                //String secondaryCompId = mapper.getSecondaryCompIdsAsString(user.getCurCompId(), user.getUsername());
                //param.getParams().setSecondaryCompId(secondaryCompId);
            }
        }


       return mapper.page([实体名小写]DtoConverter,param);

    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public [实体名]Dto save([实体名]Dto dto) {
        UserObjectFullDto user = UserThreadLocal.get();
        
        // DTO转DO
        [实体名]Do bean = [实体名小写]DoConverter.convert(dto);

        LocalDateTime now = LocalDateTime.now();
        bean.setUpdDate(now);
        bean.setUpdUserId(user.getUserid());
        bean.setUpdUserName(user.getUsername());
        
        // 保存DO
        [实体名]Do saved = super.save(bean);
        
        // DO转DTO返回
        return [实体名小写]DtoConverter.convert(saved);
    }

    @Override
    public [实体名]Dto selectById(Long id) {
        [实体名]Do entity = super.selectById(id);
        return [实体名小写]DtoConverter.convert(entity);
    }

    @Override
    public int deleteByIds(List<Long> ids) {
        return mapper.deleteByIds(ids);
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

        Page<[实体名]Dto> page = page(user,pageParam);

        List<[实体名]ExportDto> records = page == null ? Collections.emptyList() : BeanUtil.copyToList(page.getRecords(), [实体名]ExportDto.class);
        EasyExcelWriteUtil.fileName("[业务名称]")
                .sheet("[业务名称]", 0, records, [实体名]ExportDto.class)
                .doWrite(response);
    }

}
```

---

## 第七步：创建 Controller

### 位置
`fssc-config-web/src/main/java/com/yili/config/web/controller/[模块名]/[实体名]Controller.java`

### 提示词模板

```
请在 fssc-config-web 模块中创建 Controller 类 [实体名]Controller，要求如下：

**包路径**：`com.yili.config.web.controller.[模块名]`

**类信息**：
- 类名：[实体名]Controller
- 注解：
  - @Controller（或 @RestController）
  - @RequestMapping("/[实体小写名称]-do")
  - @Tag(name = "[菜单路径]", description = "[业务描述]")
  - @Schema(description = "[业务描述]")

**依赖注入**：
- I[实体名]DoService（注解：@Autowired）
- 说明：Service已经处理好DO和DTO的转换，Controller不需要注入Converter

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
- 说明：Service直接返回DTO，无需手动转换

### 4. save - 新增或更新
- 路径：POST /save
- 参数：[实体名]Dto
- 返回：[实体名]Dto
- 校验：@Validated
- 说明：Service接收DTO并返回DTO，无需手动转换

### 5. export - 导出
- 路径：POST /export
- 参数：PageParam<[实体名]Dto, [实体名]Dto>、HttpServletResponse
- 返回：void

**注解说明**：
- @Operation：Swagger接口文档注解（summary、description）
- @ResponseBody：返回JSON（如果使用 @Controller）
- @RequestBody：接收JSON请求体
- @Validated：参数校验

**示例参考**：TRmbsInvoiceAuthenticationController
```

### 代码模板

```java
package com.yili.config.web.controller.[模块名];

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.config.[模块名].DO.[实体名]Do;
import com.yili.config.api.param.[模块名].converter.[实体名]DoConverter;
import com.yili.config.api.param.[模块名].converter.[实体名]DtoConverter;
import com.yili.config.api.param.[模块名].dto.[实体名]DelDto;
import com.yili.config.api.param.[模块名].dto.[实体名]Dto;
import com.yili.config.[模块名].service.I[实体名]DoService;
import com.yili.config.sys.api.config.UserThreadLocal;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import org.springframework.stereotype.Controller;

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
@Tag(name = "[菜单路径]")
@RequestMapping("/[实体小写名称]-do")
public class [实体名]Controller {
    
    @Autowired
    I[实体名]DoService [实体名小写]DoService;

    /**
     * 分页查询
     */
    @PostMapping("/page")
    @Operation(summary = "查询[业务名称]", description = "查询[业务名称]")
    @ResponseBody
    public Page<[实体名]Dto> page(@RequestBody PageParam<[实体名]Dto, [实体名]Dto> param) {
        UserObjectFullDto user = UserThreadLocal.get();
        return [实体名小写]DoService.page(user, param);
    }

    /**
     * 批量删除
     */
    @PostMapping("/delete-by-ids")
    @Operation(summary = "删除[业务名称]", description = "删除[业务名称]")
    @ResponseBody
    public int deleteByIds(@RequestBody @Validated [实体名]DelDto param) {
        List<Long> ids = param.getIds();
        return [实体名小写]DoService.deleteByIds(ids);
    }

    /**
     * 根据ID查询
     */
    @ResponseBody
    @Operation(summary = "获取[业务名称]", description = "获取[业务名称]")
    @PostMapping(value = "/get-by-id")
    public [实体名]Dto getById(@RequestBody @Validated [实体名]Dto dto) {
        Long id = dto.getId();
        return [实体名小写]DoService.selectById(id);
    }

    /**
     * 新增或更新
     */
    @ResponseBody
    @Operation(summary = "保存[业务名称]", description = "保存[业务名称]")
    @PostMapping(value = "/save")
    public [实体名]Dto save(@RequestBody @Validated [实体名]Dto dto) {
        return [实体名小写]DoService.save(dto);
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
        [实体名小写]DoService.export(params, user, response);
    }
}
```

---

## 完整调用链路说明

### 请求流程
```
HTTP 请求
  ↓
Controller (fssc-config-web)
  - 接收请求参数（DTO）
  - 参数校验 (@Validated)
  - 调用 Service
  ↓
Service (fssc-config-service)
  - 业务逻辑处理
  - 权限控制
  - 数据转换（DTO ↔ DO）
  - 调用 Mapper
  ↓
Mapper (fssc-config-service)
  - MyBatis-Plus 基础方法
  - 自定义 SQL（如需要）
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
  ↓ Converter (DoConverter)
Service: DO
  ↓ Mapper
Database
  ↓ MyBatis
Service: DO
  ↓ Converter (DtoConverter)
Service: DTO
  ↓ (直接返回)
Controller: DTO
  ↓ Jackson
前端 JSON
```

**说明**：Controller不再处理DO/DTO转换，所有转换逻辑都在Service层完成。

---

## 关键技术点说明

### 1. BaseDoService 基础服务
- 提供通用 CRUD 方法：save、update、selectById、selectList 等
- 自动处理审计字段（创建人、修改人、创建时间、修改时间）

### 2. BaseMapperX 基础 Mapper
- 继承 MyBatis-Plus 的 BaseMapper
- 扩展了 page 方法，支持自动类型转换（DO → DTO）
- 提供 deleteByIds 批量删除方法

### 3. MapStruct 对象转换
- 编译期生成转换代码，性能高
- BaseMapperConverter 提供基础转换方法：
  - convert(Source) → Target：单个对象转换
  - convert(List<Source>) → List<Target>：列表转换

### 4. 分页查询
- PageParam<P, R>：
  - P：查询参数类型
  - R：返回结果类型
  - 包含：pageNum、pageSize、params（查询条件）
- Page<T>：MyBatis-Plus 分页结果
  - 包含：records（数据列表）、total（总数）、pages（总页数）

### 5. Excel 导出
- EasyExcelWriteUtil：项目封装的 EasyExcel 工具类
- 使用 @ExcelProperty 注解定义 Excel 列名
- 支持日期格式化：@DateTimeFormat

### 6. 审计字段
TenantBaseDO 和 BaseDO 的字段说明:
- **BaseDO**: 空基类,没有任何字段
- **TenantBaseDO**: 只包含以下字段
  - tenantCode: 租户代码 (@TableField("TENANT_CODE"))

**重要**: 以下字段需要在每个实体类中显式定义:
- **compId**: 公司ID (@TableField("COMP_ID")) - **必须定义**
- crtDate: 创建时间 (由Service层处理)
- crtUserId: 创建人id (由Service层处理)
- crtUserName: 创建人姓名 (由Service层处理)
- updDate: 修改时间 (由Service层处理)
- updUserId: 修改人id (由Service层处理)
- updUserName: 修改人姓名 (由Service层处理)

注意:审计字段如果在数据库表中存在,需要在DO中定义;如果不存在,则不需要定义。Service层会自动填充这些字段的值。

### 7. 参数校验
- @Validated：启用参数校验
- @NotEmpty：非空校验（集合）
- @NotNull：非空校验（对象）
- @NotBlank：非空字符串校验

---

## 代码生成步骤总结

### 按顺序执行以下步骤：

1. **创建 DO 实体类**（claim-ptp-do）
   - 定义数据库表映射
   - 添加字段注解

2. **创建 Mapper 接口**（claim-ptp-service）
   - 继承 BaseMapperX

2（补充）. **创建 Mapper XML 文件**（claim-ptp-service/resources）
   - 位置：`resources/mapper/com/yili/claim/ptp/[模块名]/[实体名]DoMapper.xml`
   - 配置 namespace
   - 如需要，添加自定义 SQL

3. **创建 DTO 类**（claim-ptp-api-param）
   - 主 DTO（继承 DO）
   - 删除 DTO（包含 ids）
   - 导出 DTO（Excel 注解）

4. **创建 Converter 接口**（claim-ptp-api-param）
   - DoConverter（Dto → Do）
   - DtoConverter（Do → Dto）

5. **创建 DO Service 接口**（claim-ptp-service/service）
   - 继承 IBaseDoService
   - 仅定义数据访问方法

6. **创建 DO Service 实现类**（claim-ptp-service/service/impl）
   - 继承 BaseDoService
   - 仅实现数据访问逻辑
   - 禁止业务逻辑

7. **创建 Business Service 接口**（claim-ptp-service/business）
   - 定义业务方法

8. **创建 Business Service 实现类**（claim-ptp-service/business/impl）
   - 实现业务逻辑
   - 权限控制
   - 数据转换
   - 调用 DO Service

9. **创建 Controller**（claim-ptp-web）
   - 定义接口路由
   - 参数校验
   - 调用 Business Service

---

## 常见问题和注意事项

### 1. 包命名规范
- DO：`com.yili.claim.ptp.[模块名].DO`
- Mapper：`com.yili.claim.ptp.[模块名].mapper`
- Mapper XML：`resources/mapper/com/yili/claim/ptp/[模块名]/`
- DO Service：`com.yili.claim.ptp.[模块名].service`
- Business Service：`com.yili.claim.ptp.[模块名].business`
- DTO：`com.yili.claim.ptp.api.param.[模块名].dto`
- Converter：`com.yili.claim.ptp.api.param.[模块名].converter`
- Controller：`com.yili.claim.ptp.web.controller.[模块名]`

### 2. 命名规范
- DO 类：[实体名]Do
- DTO 类：[实体名]Dto
- Mapper 接口：[实体名]DoMapper
- Mapper XML：[实体名]DoMapper.xml
- Service 接口：I[实体名]DoService
- Service 实现：[实体名]DoServiceImpl
- Controller：[实体名]Controller

### 3. 注解使用
- DO：@Getter、@Setter、@ToString（Lombok）
- DTO：@Data（Lombok）
- DO Service：@Service
- Business Service：@Service
- Controller：@Controller 或 @RestController
- Converter：@Mapper(componentModel = "spring")

### 4. 依赖注入
- Business Service 注入：@Resource 或 @Autowired
- DO Service 注入：@Resource 或 @Autowired
- Converter 注入：@Resource
- Mapper 注入：自动注入（通过继承 BaseDoService）

### 5. 数据库字段映射
- @TableName:表名
- @TableId:主键
- @TableField:普通字段
- **字段名映射规则(严格遵循)**:
  - 数据库列名统一使用大写+下划线格式(如:USER_NAME、TEAM_ID)
  - Java字段名统一使用驼峰命名法(如:userName、teamId)
  - **特殊情况处理**:
    - 全大写无下划线的列名必须正确转换为驼峰:ISENABLE → isEnable(不是isenable)
    - SEATSTATE → seatState(不是seatstate)
    - GROUPLEADER → groupLeader(不是groupleader)
    - IS_开头的布尔字段保持is前缀:IS_REVIEW_ACCOUNT → isReviewAccount
  - @TableField注解中的列名必须与数据库列名完全一致(包括大小写)
  - MyBatis-Plus会自动处理驼峰↔下划线转换,但前提是Java字段名必须符合驼峰命名规范

### 6. 审计字段
TenantBaseDO 和 BaseDO 的字段说明:
- **BaseDO**: 空基类,没有任何字段
- **TenantBaseDO**: 只包含以下字段
  - tenantCode: 租户代码 (@TableField("TENANT_CODE"))

**重要**: 以下字段需要在每个实体类中显式定义:
- **compId**: 公司ID (@TableField("COMP_ID")) - **必须定义**
- crtDate: 创建时间 (由Service层处理)
- crtUserId: 创建人id (由Service层处理)
- crtUserName: 创建人姓名 (由Service层处理)
- updDate: 修改时间 (由Service层处理)
- updUserId: 修改人id (由Service层处理)
- updUserName: 修改人姓名 (由Service层处理)

注意:审计字段如果在数据库表中存在,需要在DO中定义;如果不存在,则不需要定义。Service层会自动填充这些字段的值。

### 7. 参数校验
- @Validated：启用参数校验
- @NotEmpty：非空校验（集合）
- @NotNull：非空校验（对象）
- @NotBlank：非空字符串校验

---

## 使用示例

### 示例：创建"部门管理"功能

**需求说明**：
- 表名：T_SYS_DEPARTMENT
- 实体名：Department
- 模块：sys（系统管理）
- 字段：id、deptName、parentId、sortOrder

**步骤 1：创建 DepartmentDo**

```
package com.yili.config.sys.DO;

import com.yili.common.db.base.DO.TenantBaseDO;
import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
@TableName("T_SYS_DEPARTMENT")
@Schema(name = "DepartmentDo", description = "部门信息")
public class DepartmentDo extends TenantBaseDO {

    @TableId("ID")
    @Schema(description = "主键")
    private Long id;

    @TableField("DEPT_NAME")
    @Schema(description = "部门名称")
    private String deptName;

    @TableField("PARENT_ID")
    @Schema(description = "父部门ID")
    private Long parentId;

    @TableField("SORT_ORDER")
    @Schema(description = "排序号")
    private Integer sortOrder;
}
```

**步骤 2-7**：按照模板创建其他文件，替换以下占位符：
- `[实体名]` → `Department`
- `[实体小写名称]` → `department`
- `[模块名]` → `sys`
- `[业务名称]` → `部门管理`
- `[业务描述]` → `部门信息管理`

---

## 总结

本文档提供了完整的 MyBatis-Plus CRUD 代码生成指南，涵盖从数据库实体到前端接口的所有层次。使用本模板可以快速生成标准化、规范化的业务代码，提高开发效率并保证代码质量。

**核心要点**：
1. 严格遵循分层架构（Business + DO Service 双层设计）
2. 业务逻辑与数据访问严格分离
3. 统一的命名规范
4. 完整的类型转换
5. 标准的权限控制
6. 规范的接口文档

**建议**：
- 先理解调用链路，再进行代码生成
- 保持各层职责单一（DO Service 绝对不包含业务逻辑）
- 合理使用基类方法
- 注重代码复用性
- 先询问我模块名，如果模块对应包没创建，先创建包
- Do里面参数一定要和提供的脚本字段类型相匹配，个数一致
- 确认后再创建文件
