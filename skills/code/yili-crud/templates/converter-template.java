package com.yili.[服务名].service.[模块名].converter;

import com.yili.common.db.mybatis.pojo.BaseMapperConverter;
import com.yili.[服务名].entity.[模块名].[实体名]Do;
import com.yili.[服务名].service.[模块名].dto.[实体名]Dto;
import org.mapstruct.Mapper;

/**
 * [实体名]DtoConverter：DO ↔ DTO 双向转换
 *
 * BaseMapperConverter 提供：
 * - convert(Source) → Target
 * - convertList(List<Source>) → List<Target>
 * - reverseConvert(Target) → Source
 * - reverseConvertList(List<Target>) → List<Source>
 *
 * @author sevenxiao
 * @since [日期]
 */
@Mapper(componentModel = "spring")
public interface [实体名]DtoConverter extends BaseMapperConverter<[实体名]Do, [实体名]Dto> {
}
