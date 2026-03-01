package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.impl;

import com.yili.claim.common.api.param.claim.dto.TRmbsClaimBaseDto;
import com.yili.claim.common.service.line.dto.TRmbsClaimLineDto;
import com.yili.claim.common.service.line.service.impl.BaseNewClaimLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}NewClaimLineService;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-新建明细行服务实现
 *
 * 迁移自: NewT{{templateNum}}ClaimLineService.java
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/NewT{{templateNum}}ClaimLineService.java
 *
 * 基类 BaseNewClaimLineService 已实现:
 * - newClaimLine(Long claimId): 创建明细行主流程
 *   └ 查报账单 → 初始化DTO → 设币种/汇率/公司 → preExecute → 费用部门 → BU段 → 部门属性 → 项目段 → 默认字段
 * - preExecute(claimLineDto, claim): 空钩子，供子类重写个性化初始化
 *
 * 子类需在 preExecute() 中实现 T{{templateNum}} 特有的明细行初始化逻辑
 *
 * @author {{author}}
 * @since {{date}}
 */
@Service
public class T{{templateNum}}NewClaimLineServiceImpl extends BaseNewClaimLineService implements IT{{templateNum}}NewClaimLineService {

    /**
     * T{{templateNum}}新建明细行-预处理（个性化逻辑）
     *
     * 原代码对应: NewT{{templateNum}}ClaimLineService.java 第xx-xx行
     *
     * 迁移指引：
     * 1. 查看老代码 NewT{{templateNum}}ClaimLineService 的 execute() 方法
     * 2. 基类已处理的逻辑（币种、汇率、费用部门、BU段、部门属性、项目段）直接跳过
     * 3. T{{templateNum}}特有的明细行字段初始化写在此方法中
     * 4. 注释中标注原来代码对应行数
     */
    @Override
    public TRmbsClaimLineDto preExecute(TRmbsClaimLineDto claimLineDto, TRmbsClaimBaseDto claim) {

        // ============================================================
        // TODO: 从老代码 NewT{{templateNum}}ClaimLineService 迁移特有逻辑
        // ============================================================

        // 示例：设置T{{templateNum}}特有的默认值
        // 原代码对应: NewT{{templateNum}}ClaimLineService.java 第xx行
        // claimLineDto.setXxx("defaultValue");

        return claimLineDto;
    }
}
