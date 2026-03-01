package com.yili.[服务名].service.[模块名].facade.impl;

import cn.hutool.core.bean.BeanUtil;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.base.service.BaseDoXService;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.[服务名].entity.[模块名].[实体名]Do;
import com.yili.[服务名].service.[模块名].converter.[实体名]DtoConverter;
import com.yili.[服务名].service.[模块名].dto.[实体名]Dto;
import com.yili.[服务名].service.[模块名].dto.[实体名]ExportDto;
import com.yili.[服务名].service.[模块名].facade.I[实体名]DoService;
import com.yili.[服务名].service.[模块名].mapper.[实体名]DoMapper;
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

/**
 * [业务描述] Facade 实现
 *
 * 关键说明:
 * - BaseDoXService 自动注入 mapper 和 converter
 * - super.save(bean) 会自动处理新增/更新逻辑
 * - mapper.page(converter, param) 自动完成 DO→DTO 转换和分页
 *
 * @author sevenxiao
 * @since [日期]
 */
@Service
public class [实体名]DoServiceImpl
        extends BaseDoXService<[实体名]Dto, [实体名]Do, [实体名]DoMapper, [实体名]DtoConverter>
        implements I[实体名]DoService {

    @Override
    public Page<[实体名]Dto> page(UserObjectFullDto user,
                                   PageParam<[实体名]Dto, [实体名]Dto> param) {
        if (!user.isAdmin()) {
            // 非管理员权限过滤（按需调整）
            // param.getParams().setCompId(user.getCurCompId().toString());
        }
        return mapper.page(converter, param);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public [实体名]Dto save([实体名]Dto bean) {
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
    public void export(PageParam<[实体名]Dto, [实体名]Dto> params,
                       UserObjectFullDto user, HttpServletResponse response) {
        PageParam<[实体名]Dto, [实体名]Dto> pageParam =
                params == null ? new PageParam<>() : params;
        if (pageParam.getParams() == null) {
            pageParam.setParams(new [实体名]Dto());
        }
        pageParam.setPageNum(1);
        pageParam.setPageSize(Long.MAX_VALUE);

        Page<[实体名]Dto> page = page(user, pageParam);
        List<[实体名]ExportDto> records = page == null
                ? Collections.emptyList()
                : BeanUtil.copyToList(page.getRecords(), [实体名]ExportDto.class);

        EasyExcelWriteUtil.fileName("[业务名称]")
                .sheet("[业务名称]", 0, records, [实体名]ExportDto.class)
                .doWrite(response);
    }
}
