package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.impl;

import com.yili.claim.common.service.claim.dto.TRmbsClaimPageDto;
import com.yili.claim.common.service.claim.service.impl.BaseDeleteClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}DeleteClaimService;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-删除服务实现
 *
 * 迁移自: DeleteT{{templateNum}}ClaimService.java
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/DeleteT{{templateNum}}ClaimService.java
 *
 * 基类 BaseDeleteClaimService 已实现:
 * - delete(Long claimId): 删除主流程（查单据 → preExecute → 校验 → 删除关联数据 → 删除主表）
 * - preExecute(): 删除前个性化逻辑（子类可重写）
 * - validataClaim(): 删除前校验
 * - 关联数据删除: 付款计划、明细行、税金、发票关联、影像、OCR等
 *
 * 如果T{{templateNum}}有特殊的删除校验或关联删除逻辑，可重写 preExecute()
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}DeleteClaimServiceImpl extends BaseDeleteClaimService implements IT{{templateNum}}DeleteClaimService {

    // ============================================================
    // TODO: 分析老代码 DeleteT{{templateNum}}ClaimService
    // 如果无特殊逻辑，直接使用基类实现即可（空类）
    // ============================================================

    // 如需自定义删除前逻辑，重写 preExecute:
    //
    // /**
    //  * 删除前个性化逻辑
    //  * 原代码对应: DeleteT{{templateNum}}ClaimService.java 第xx行
    //  */
    // @Override
    // protected void preExecute(TRmbsClaimPageDto claimDto, UserObjectFullDto user) {
    //     // T{{templateNum}} 特有删除逻辑
    // }

}

