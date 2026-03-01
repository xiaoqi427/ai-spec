package com.yili.[服务名].service.[模块名].dto;

import com.yili.[服务名].entity.[模块名].[实体名]Do;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

import java.util.List;

/**
 * [业务描述] 删除 DTO
 *
 * @author sevenxiao
 * @since [日期]
 */
@Data
@Schema(name = "[实体名]DelDto", description = "[业务描述] 删除")
public class [实体名]DelDto extends [实体名]Do {

    @NotEmpty
    @Schema(description = "ids")
    private List<Long> ids;
}
