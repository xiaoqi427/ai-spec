package com.yili.[服务名].entity.[模块名];

import com.baomidou.mybatisplus.annotation.KeySequence;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.yili.common.db.base.DO.TenantBaseDO;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;

/**
 * [业务描述]
 *
 * @author sevenxiao
 * @since [日期]
 */
@Getter
@Setter
@ToString
@TableName("[数据库表名]")
@Schema(name = "[实体名]Do", description = "[业务描述]")
@KeySequence("[序列名]")
public class [实体名]Do extends TenantBaseDO {

    /** 主键 */
    @TableId("ID")
    @Schema(description = "主键")
    private Long id;

    /** 公司ID（必须显式定义） */
    @TableField("COMP_ID")
    @Schema(description = "公司ID")
    private Long compId;

    /** [字段说明] */
    @TableField("[DB_COLUMN]")
    @Schema(description = "[字段说明]")
    private [类型] [字段名];

    // 审计字段（如数据库表中存在则定义）
    @TableField("CRT_DATE")
    @Schema(description = "创建时间")
    private LocalDateTime crtDate;

    @TableField("CRT_USER_ID")
    @Schema(description = "创建人ID")
    private String crtUserId;

    @TableField("CRT_USER_NAME")
    @Schema(description = "创建人")
    private String crtUserName;

    @TableField("UPD_DATE")
    @Schema(description = "修改时间")
    private LocalDateTime updDate;

    @TableField("UPD_USER_ID")
    @Schema(description = "修改人ID")
    private String updUserId;

    @TableField("UPD_USER_NAME")
    @Schema(description = "修改人")
    private String updUserName;
}
