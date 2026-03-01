package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.impl;

import com.yili.claim.common.api.param.claim.dto.TRmbsClaimBaseDto;
import com.yili.claim.common.service.line.dto.TRmbsClaimLineDto;
import com.yili.claim.common.service.line.service.impl.BaseSaveClaimLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}SaveClaimLineService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-保存明细行服务实现
 *
 * 迁移自: InsertT{{templateNum}}ClaimLineService.java
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/InsertT{{templateNum}}ClaimLineService.java
 *
 * 基类 BaseSaveClaimLineService 已实现:
 * - saveClaimLine(claimLineDto): 保存明细行主流程
 *   └ 查报账单 → 设币种/汇率 → preExecute → 智能报账金额拆分 → T049/T069校验 → 项目段查询 →
 *     科目段校验 → T020/T035子目段处理 → T014承兑台账 → save → 手机费额度 → after
 * - preExecute(claim, claimLineDto): 空钩子(继承自ClaimLineBaseService)，供子类重写保存前逻辑
 * - after(claim, claimLineDto): 默认调用 processAmount，供子类重写保存后逻辑
 * - processAmount(claimLineDto, preProcess, afterProcess): 汇总头部金额（含钩子函数前/后置修改）
 *
 * 可重写的钩子方法:
 * - preExecute(claim, claimLineDto): 保存前个性化逻辑（发票校验、金额处理、特殊字段赋值等）
 * - after(claim, claimLineDto): 保存后个性化逻辑（关联数据更新、金额重算等）
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}SaveClaimLineServiceImpl extends BaseSaveClaimLineService implements IT{{templateNum}}SaveClaimLineService {

    // ============================================================
    // TODO: 从老代码迁移特有逻辑
    // ============================================================

    // 如需自定义保存前逻辑，重写 preExecute:
    //
    // /**
    //  * 保存前个性化逻辑
    //  * 原代码对应: InsertT{{templateNum}}ClaimLineService.java 第xx-xx行
    //  *
    //  * 常见迁移逻辑:
    //  * 1. 发票校验（发票号码+代码重复检查）
    //  * 2. 调用 super.preExecute(claim, claimLineDto) 处理基础八段信息
    //  * 3. 金额字段处理（applyAmount = foreignApplyAmount 等）
    //  * 4. 特殊字段赋值（flexOu、vmilineId等）
    //  */
    // @Override
    // public void preExecute(TRmbsClaimBaseDto claim, TRmbsClaimLineDto claimLineDto) {
    //     // 1. 调用父类（含八段信息处理）
    //     super.preExecute(claim, claimLineDto);
    //     // 2. T{{templateNum}}特有逻辑
    // }

    // 如需自定义保存后逻辑，重写 after:
    //
    // /**
    //  * 保存后个性化逻辑
    //  * 原代码对应: InsertT{{templateNum}}ClaimLineService.java 第xx行
    //  */
    // @Override
    // protected void after(TRmbsClaimBaseDto claim, TRmbsClaimLineDto claimLineDto) {
    //     // 先调用父类（默认processAmount）
    //     super.after(claim, claimLineDto);
    //     // T{{templateNum}}特有后处理
    // }

}
