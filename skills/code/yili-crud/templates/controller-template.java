package com.yili.[服务名].web.controller.[模块名];

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yili.common.db.mybatis.pojo.PageParam;
import com.yili.[服务名].service.[模块名].dto.[实体名]DelDto;
import com.yili.[服务名].service.[模块名].dto.[实体名]Dto;
import com.yili.[服务名].service.[模块名].service.[实体名]Service;
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

/**
 * [业务描述] 前端控制器
 *
 * @author sevenxiao
 * @since [日期]
 */
@Controller
@Schema(description = "[业务描述]")
@Tag(name = "[菜单路径]")
@RequestMapping("/[请求路径前缀]-do")
public class [实体名]Controller {

    @Autowired
    [实体名]Service [实体名小写首字母]Service;

    /** 分页查询 */
    @PostMapping("/page")
    @Operation(summary = "查询[业务名称]", description = "查询[业务名称]")
    @ResponseBody
    public Page<[实体名]Dto> page(
            @RequestBody PageParam<[实体名]Dto, [实体名]Dto> param) {
        UserObjectFullDto user = UserThreadLocal.get();
        return [实体名小写首字母]Service.page(user, param);
    }

    /** 批量删除 */
    @PostMapping("/delete-by-ids")
    @Operation(summary = "删除[业务名称]", description = "删除[业务名称]")
    @ResponseBody
    public int deleteByIds(
            @RequestBody @Validated [实体名]DelDto param) {
        List<Long> ids = param.getIds();
        return [实体名小写首字母]Service.deleteByIds(ids);
    }

    /** 根据ID查询 */
    @PostMapping("/get-by-id")
    @Operation(summary = "获取[业务名称]", description = "获取[业务名称]")
    @ResponseBody
    public [实体名]Dto getById(
            @RequestBody @Validated [实体名]Dto dto) {
        Long id = dto.getId();
        return [实体名小写首字母]Service.selectById(id);
    }

    /** 新增或更新 */
    @PostMapping("/save")
    @Operation(summary = "保存[业务名称]", description = "保存[业务名称]")
    @ResponseBody
    public [实体名]Dto save(
            @RequestBody @Validated [实体名]Dto dto) {
        return [实体名小写首字母]Service.save(dto);
    }

    /** 导出 */
    @PostMapping("/export")
    @Operation(summary = "导出", description = "依据查询条件导出")
    @ResponseBody
    public void export(
            @RequestBody PageParam<[实体名]Dto, [实体名]Dto> params,
            HttpServletResponse response) {
        UserObjectFullDto user = UserThreadLocal.get();
        [实体名小写首字母]Service.export(params, user, response);
    }
}
