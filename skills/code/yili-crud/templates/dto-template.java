package com.yili.[服务名].service.[模块名].dto;

import com.yili.[服务名].entity.[模块名].[实体名]Do;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * [业务描述] DTO
 *
 * @author sevenxiao
 * @since [日期]
 */
@Data
@Schema(name = "[实体名]Dto", description = "[业务描述]")
public class [实体名]Dto extends [实体名]Do {

    // 可添加额外的查询/展示字段（数据库中不存在的字段在此定义）
}
