package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.impl;

import com.yili.claim.common.service.claim.dto.TRmbsClaimPageDto;
import com.yili.claim.common.service.claim.service.impl.BaseNewClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}NewClaimService;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-新建服务实现
 *
 * 迁移自: NewT{{templateNum}}ClaimService.java
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/NewT{{templateNum}}ClaimService.java
 *
 * 基类 BaseNewClaimService 已实现:
 * - newClaim(): 创建报账单主流程（用户信息 → 模板 → 默认值 → preExecute）
 * - setUserInformation(): 设置用户信息
 * - preResult(): 模板信息 + 默认值 + 默认事业部
 * - setDefaultValues(): 设置默认值（版本号、紧急程度、金额等）
 * - setVendorInfo/setVendorInfoOfEMployeeVendor(): 员工供应商赋值
 *
 * 子类需在 preExecute() 中实现 T{{templateNum}} 特有逻辑
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}NewClaimServiceImpl extends BaseNewClaimService implements IT{{templateNum}}NewClaimService {

    /**
     * T{{templateNum}}新建报账单-预处理（个性化逻辑）
     *
     * 原代码对应: NewT{{templateNum}}ClaimService.java 第xx-xx行
     *
     * 迁移指引（请根据老代码实际逻辑填充）：
     * 1. 分析 NewT{{templateNum}}ClaimService 的 execute() 方法
     * 2. 基类已处理的逻辑直接跳过（如用户信息、默认值等）
     * 3. T{{templateNum}}特有的初始化逻辑写在此方法中
     * 4. 注释中标注原来代码对应行数
     */
    @Override
    protected TRmbsClaimPageDto preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
        log.debug("T{{templateNum}}NewClaimServiceImpl.preExecute开始");

        // ============================================================
        // TODO: 从老代码 NewT{{templateNum}}ClaimService 迁移特有逻辑
        // ============================================================

        // 示例：报销人信息（如果基类未处理或需要覆盖）
        // 原代码对应: NewT{{templateNum}}ClaimService.java 第xx行
        // claim.setExpenseIssuerId(user.getUserid());
        // claim.setExpenseIssuerName(user.getFullname());
        // claim.setExpenseIssuerDeptId(user.getCurGroupId());

        // 示例：退款标识
        // claim.setIsRefund("0");

        // 示例：设置单位全称和税号
        // ouTax(claim, user);

        log.debug("T{{templateNum}}NewClaimServiceImpl.preExecute完成");
        return claim;
    }
}
