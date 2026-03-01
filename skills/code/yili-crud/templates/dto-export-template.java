package com.yili.[服务名].service.[模块名].dto;

import com.alibaba.excel.annotation.ExcelIgnore;
import com.alibaba.excel.annotation.ExcelProperty;
import com.alibaba.excel.annotation.format.DateTimeFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * [业务描述] 导出 DTO
 *
 * @author sevenxiao
 * @since [日期]
 */
@Data
@Schema(name = "[实体名]ExportDto", description = "[业务描述] 导出")
public class [实体名]ExportDto {

    @ExcelIgnore
    @Schema(description = "主键")
    private Long id;

    @ExcelProperty("[Excel列名]")
    @Schema(description = "[字段说明]")
    private [类型] [字段名];

    @ExcelProperty("[日期列名]")
    @DateTimeFormat("yyyy-MM-dd HH:mm:ss")
    @Schema(description = "[日期字段说明]")
    private LocalDateTime [日期字段名];
}
