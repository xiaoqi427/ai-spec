package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.impl;

import com.yili.claim.common.api.param.claim.dto.TRmbsClaimBaseDto;
import com.yili.claim.common.service.line.dto.TRmbsClaimLineDto;
import com.yili.claim.common.service.line.service.impl.BaseUpdateClaimLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}UpdateClaimLineService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-更新明细行服务实现
 *
 * 迁移自: UpdateT{{templateNum}}ClaimLineService.java
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/UpdateT{{templateNum}}ClaimLineService.java
 *
 * 基类 BaseUpdateClaimLineService 已实现:
 * - updateClaimLine(claimLineDto): 更新明细行主流程
 *   └ 查报账单 → 查旧行数据 → 金额/item3Id校验 → T027校验 → T049/T069校验 → preExecute →
 *     设币种/汇率 → 质保金校验 → 智能报账金额拆分 → T012计提处理 → T051清除 → 项目段查询 →
 *     T049/T069处理 → 发票关联更新 → T049/T069交易流水更新 → save → after
 * - preExecute(claim, claimLineDto): 调用 clearCrDrSegCode + super.preExecute（八段信息处理）
 * - after(claim, claimLineDto): 默认调用 processAmount
 * - processAmount(claimLineDto, preProcess, afterProcess): 汇总头部金额
 * - clearCrDrSegCode(claim, claimLineDto): 清除借贷方科目段（特定单据类型+草稿状态时）
 * - processLedgerPayList4ClaimLine(claim, claimLineDto): 处理总账付款计划行
 *
 * 可重写的钩子方法:
 * - preExecute(claim, claimLineDto): 更新前个性化逻辑
 *   注意: 父类 preExecute 会先 clearCrDrSegCode 再调 super.preExecute（八段处理），
 *         子类重写时需考虑是否调用 super.preExecute
 * - after(claim, claimLineDto): 更新后个性化逻辑
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}UpdateClaimLineServiceImpl extends BaseUpdateClaimLineService implements IT{{templateNum}}UpdateClaimLineService {

    // ============================================================
    // TODO: 从老代码迁移特有逻辑
    // ============================================================

    // 如需自定义更新前逻辑，重写 preExecute:
    //
    // /**
    //  * 更新前个性化逻辑
    //  * 原代码对应: UpdateT{{templateNum}}ClaimLineService.java 第xx-xx行
    //  *
    //  * 常见迁移逻辑:
    //  * 1. 发票校验（发票号码+代码重复检查）
    //  * 2. 调用 super.preExecute(claim, claimLineDto) 处理借贷科目段清除 + 八段信息
    //  * 3. 金额字段处理、特殊字段赋值
    //  */
    // @Override
    // public void preExecute(TRmbsClaimBaseDto claim, TRmbsClaimLineDto claimLineDto) {
    //     // 1. 调用父类（clearCrDrSegCode + 八段信息处理）
    //     super.preExecute(claim, claimLineDto);
    //     // 2. T{{templateNum}}特有逻辑
    // }

    // 如需自定义更新后逻辑，重写 after:
    //
    // /**
    //  * 更新后个性化逻辑
    //  * 原代码对应: UpdateT{{templateNum}}ClaimLineService.java 第xx行
    //  */
    // @Override
    // protected void after(TRmbsClaimBaseDto claim, TRmbsClaimLineDto claimLineDto) {
    //     super.after(claim, claimLineDto);
    //     // T{{templateNum}}特有后处理
    // }

}
