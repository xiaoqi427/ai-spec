package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.impl;

import com.yili.claim.common.api.param.claim.dto.TRmbsClaimBaseDto;
import com.yili.claim.common.entity.claim.TRmbsClaimDo;
import com.yili.claim.common.service.claim.dto.TRmbsClaimPageDto;
import com.yili.claim.common.service.claim.dto.TRmbsClaimPageFullDto;
import com.yili.claim.common.service.claim.service.impl.BaseSaveOrUpdateClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}SaveClaimService;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-保存服务实现
 *
 * 迁移自（合并）:
 * - InsertT{{templateNum}}ClaimService.java (新增逻辑)
 * - UpdateT{{templateNum}}ClaimService.java (修改逻辑)
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/
 *
 * 基类 BaseSaveOrUpdateClaimService 已实现:
 * - save(): 根据claimId判断新增/修改，新增调用super.save()，修改调用update()
 * - validation(): 基础数据校验（单据存在性、模板校验、版本号校验）
 * - before() -> preResult(): updateByUi → fillValue → preExecute
 * - after(): insertClaimLineFromClaim + cascadeUpdate
 * - update(): 修改流程（查老数据 → 标记修改 → 校验 → before → 保存 → updateClaimLine → after）
 *
 * 可重写的钩子方法:
 * - preExecute(): 保存前个性化逻辑
 * - insertClaimLineFromClaim(): 新增后自动创建明细行
 * - updateClaimLineFromClaim(): 更新后级联更新明细行
 * - processClaimAmount(): 处理金额（T015专用）
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}SaveClaimServiceImpl extends BaseSaveOrUpdateClaimService implements IT{{templateNum}}SaveClaimService {

    // ============================================================
    // TODO: 从老代码迁移特有逻辑
    // ============================================================

    // 如需自定义保存前逻辑，重写 preExecute:
    //
    // /**
    //  * 保存前个性化逻辑
    //  * 原代码对应: InsertT{{templateNum}}ClaimService.java 第xx行 / UpdateT{{templateNum}}ClaimService.java 第xx行
    //  */
    // @Override
    // public void preExecute(TRmbsClaimPageFullDto full,
    //                        TRmbsClaimDo claim,
    //                        TRmbsClaimBaseDto oldClaim,
    //                        TRmbsClaimPageDto params,
    //                        UserObjectFullDto user) {
    //     // T{{templateNum}} 特有保存逻辑
    // }

    // 如需新增后自动创建明细行，重写 insertClaimLineFromClaim:
    //
    // @Override
    // public void insertClaimLineFromClaim(TRmbsClaimPageFullDto full, TRmbsClaimDo claim, UserObjectFullDto user) {
    //     // 原代码对应: InsertT{{templateNum}}ClaimService.java 第xx行
    // }

}
