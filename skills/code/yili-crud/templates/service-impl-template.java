package com.yili.[服务名].service.[模块名].service.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.[服务名].service.[模块名].dto.[实体名]Dto;
import com.yili.[服务名].service.[模块名].facade.I[实体名]DoService;
import com.yili.[服务名].service.[模块名].service.[实体名]Service;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import jakarta.annotation.Resource;
import java.util.List;

/**
 * [业务描述] 业务服务实现
 *
 * 说明: 简单 CRUD 场景下 Service 层直接委托给 Facade。
 *      复杂业务逻辑在 Service 层编排。
 *
 * @author sevenxiao
 * @since [日期]
 */
@Slf4j
@Service
public class [实体名]ServiceImpl implements [实体名]Service {

    @Resource
    private I[实体名]DoService [实体名小写首字母]DoService;

    @Override
    public Page<[实体名]Dto> page(UserObjectFullDto user,
                                   PageParam<[实体名]Dto, [实体名]Dto> param) {
        return [实体名小写首字母]DoService.page(user, param);
    }

    @Override
    public [实体名]Dto selectById(Long id) {
        return [实体名小写首字母]DoService.selectById(id);
    }

    @Override
    public [实体名]Dto save([实体名]Dto dto) {
        return [实体名小写首字母]DoService.save(dto);
    }

    @Override
    public int deleteByIds(List<Long> ids) {
        return [实体名小写首字母]DoService.deleteByIds(ids);
    }

    @Override
    public void export(PageParam<[实体名]Dto, [实体名]Dto> params,
                       UserObjectFullDto user, HttpServletResponse response) {
        [实体名小写首字母]DoService.export(params, user, response);
    }
}
