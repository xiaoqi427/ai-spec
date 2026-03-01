package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.impl;

import com.yili.claim.common.service.line.dto.TRmbsClaimLineDto;
import com.yili.claim.common.service.line.service.impl.BaseDeleteClaimLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}DeleteClaimLineService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-删除明细行服务实现
 *
 * 迁移自: DeleteT{{templateNum}}ClaimLineService.java
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/DeleteT{{templateNum}}ClaimLineService.java
 *
 * 基类 BaseDeleteClaimLineService 已实现:
 * - deleteClaimLine(claimLineDto): 删除明细行主流程
 *   └ 查报账单 → 循环处理每行:
 *     → T049/T069关联删除（无票行、价格差异）→ T056税额删除 → 手机费额度删除 →
 *     → 智能报账金额回写 → 税金行联动删除
 *   └ 批量删除明细行 → after
 * - after(claimLineDto): 默认调用 processAmount
 * - processAmount(claimLineDto, preProcess, afterProcess): 汇总头部金额
 *
 * 可重写的钩子方法:
 * - deleteClaimLine(claimLineDto): 如需完全自定义删除逻辑（需调用super或自行处理）
 * - after(claimLineDto): 删除后个性化逻辑（如自定义金额重算）
 *
 * 注意: 如果T{{templateNum}}有独立的金额重算逻辑（如T047/T048），
 * 需要重写 deleteClaimLine 或 after 方法来替代基类的通用处理。
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}DeleteClaimLineServiceImpl extends BaseDeleteClaimLineService implements IT{{templateNum}}DeleteClaimLineService {

    // ============================================================
    // TODO: 从老代码迁移特有逻辑
    // ============================================================

    // 如T{{templateNum}}有独立的金额重算逻辑，重写 after 或 deleteClaimLine:
    //
    // /**
    //  * 删除后处理（重写以自定义金额重算）
    //  * 原代码对应: DeleteT{{templateNum}}ClaimLineService.java 第xx行
    //  */
    // @Override
    // protected void after(TRmbsClaimLineDto claimLineDto) {
    //     // 方式一: 调用父类通用金额处理
    //     super.after(claimLineDto);
    //
    //     // 方式二: 自定义T{{templateNum}}金额重算
    //     // processT{{templateNum}}Amount(claimLineDto.getClaimId());
    // }

    // 如需完全自定义删除逻辑:
    //
    // /**
    //  * 自定义删除明细行
    //  * 原代码对应: DeleteT{{templateNum}}ClaimLineService.java 第xx-xx行
    //  */
    // @Override
    // @Transactional(rollbackFor = Exception.class)
    // public void deleteClaimLine(TRmbsClaimLineDto claimLineDto) {
    //     // 调用父类标准删除
    //     super.deleteClaimLine(claimLineDto);
    //     // T{{templateNum}}特有处理
    // }

}
