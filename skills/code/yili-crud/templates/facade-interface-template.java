package com.yili.[服务名].service.[模块名].facade;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.base.service.IBaseDoXService;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.[服务名].entity.[模块名].[实体名]Do;
import com.yili.[服务名].service.[模块名].dto.[实体名]Dto;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import jakarta.servlet.http.HttpServletResponse;

import java.util.List;

/**
 * [业务描述] Facade 接口
 *
 * @author sevenxiao
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
    Page<[实体名]Dto> page(UserObjectFullDto user,
                           PageParam<[实体名]Dto, [实体名]Dto> param);

    /**
     * 批量删除
     *
     * @param ids ID列表
     * @return 删除数量
     */
    int deleteByIds(List<Long> ids);

    /**
     * 导出
     *
     * @param params   查询参数
     * @param user     当前用户
     * @param response HTTP响应
     */
    void export(PageParam<[实体名]Dto, [实体名]Dto> params,
                UserObjectFullDto user, HttpServletResponse response);
}
