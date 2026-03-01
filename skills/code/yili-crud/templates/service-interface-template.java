package com.yili.[服务名].service.[模块名].service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.[服务名].service.[模块名].dto.[实体名]Dto;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;

import java.util.List;

/**
 * [业务描述] 业务服务接口
 *
 * @author sevenxiao
 * @since [日期]
 */
public interface [实体名]Service {

    Page<[实体名]Dto> page(UserObjectFullDto user,
                           PageParam<[实体名]Dto, [实体名]Dto> param);

    [实体名]Dto selectById(Long id);

    [实体名]Dto save([实体名]Dto dto);

    int deleteByIds(List<Long> ids);

    void export(PageParam<[实体名]Dto, [实体名]Dto> params,
                UserObjectFullDto user, HttpServletResponse response);
}
