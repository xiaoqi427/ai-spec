package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.bpm.impl;

import com.yili.bpm.api.param.process.dto.CallBackBusinessDataDto;
import com.yili.claim.common.service.claim.dto.TRmbsClaimPageDto;
import com.yili.claim.common.service.claim.dto.TRmbsClaimPageFullDto;
import com.yili.claim.common.service.claim.service.impl.BaseCallBackClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.bpm.IT{{templateNum}}CallBackClaimService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-工作流回调服务实现
 *
 * 迁移自: CallBackT{{templateNum}}ClaimService.java
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/CallBackT{{templateNum}}ClaimService.java
 *
 * 基类 BaseCallBackClaimService 已实现:
 * - execute(data, consumer): 统一回调入口 → integrateBusinessData(加载full) → 执行个性方法
 * - integrateBusinessData(data): 根据claimId加载完整报账单数据
 * - executeExecuteRoot(full, data): 起草提交 → writeClaimData
 * - executeExecute(full, data): 常规节点 → writeClaimData + 预算冻结 + 营销写入 + 影像模式补偿 + T023/T050收款
 * - executeDrawBack(full, data): 撤回 → writeClaimData + 预算解冻 + 调减回滚 + 承兑汇票解除 + T023/T050 + T001出行 + TPM删除 + 保理
 * - executeUndo(full, data): 退回 → 如退到起草人则走executeDrawBack + 清理（营销/收款/合并付款/面单/资产变更/导入错误），否则走executeExecute
 * - executeEnd(full, data): 办结 → writeClaimData + moveClaimToHis
 * - executeDelete(full, data): 删除 → status="1" + writeClaimData + 预算解冻 + 营销状态 + 金德瑞 + 发票核销 + OCR + 发票池 + T054联动T055 + 保理 + moveClaimToHis
 * - executeTrun(full, data): 转办 → writeClaimData + 初核时清GL日期
 * - executeTesong(full, data): 特送 → 如办结走executeEnd，否则writeClaimData
 * - executeAgent/executeSuspend/executeResume/executeTerminate/executeByChaCuo/executeStart/executeLingqu/executeAutoStart/executeExecuteRenwuchi: 其他回调操作
 *
 * 子类按需重写特定的流程方法，大部分单据类型仅需重写 executeExecute 和 executeEnd
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}CallBackClaimServiceImpl extends BaseCallBackClaimService implements IT{{templateNum}}CallBackClaimService {

    // ============================================================
    // TODO: 从老代码迁移特有逻辑
    // ============================================================

    // 如需自定义常规节点回调:
    //
    // /**
    //  * 常规节点流程回调
    //  * 原代码对应: CallBackT{{templateNum}}ClaimService.java 第xx-xx行 executeExecute方法
    //  */
    // @Override
    // protected void executeExecute(TRmbsClaimPageFullDto full, CallBackBusinessDataDto callBackBusinessData) {
    //     // 先调用父类处理公共逻辑
    //     super.executeExecute(full, callBackBusinessData);
    //     // T{{templateNum}}特有逻辑
    //     TRmbsClaimPageDto claim = full.getClaim();
    // }

    // 如需自定义办结回调:
    //
    // /**
    //  * 流程办结回调
    //  * 原代码对应: CallBackT{{templateNum}}ClaimService.java 第xx-xx行 executeEnd方法
    //  */
    // @Override
    // protected void executeEnd(TRmbsClaimPageFullDto full, CallBackBusinessDataDto callBackBusinessData) {
    //     // T{{templateNum}}特有的办结前处理
    //     // ...
    //     // 调用父类处理公共逻辑（writeClaimData + moveClaimToHis）
    //     super.executeEnd(full, callBackBusinessData);
    // }

    // 如需自定义撤回回调:
    //
    // /**
    //  * 流程撤回回调
    //  * 原代码对应: CallBackT{{templateNum}}ClaimService.java 第xx-xx行 executeDrawBack方法
    //  */
    // @Override
    // protected void executeDrawBack(TRmbsClaimPageFullDto full, CallBackBusinessDataDto callBackBusinessData) {
    //     super.executeDrawBack(full, callBackBusinessData);
    //     // T{{templateNum}}特有的撤回逻辑
    // }

    // 如需自定义退回回调:
    //
    // /**
    //  * 流程退回回调
    //  * 原代码对应: CallBackT{{templateNum}}ClaimService.java 第xx-xx行 executeUndo方法
    //  */
    // @Override
    // protected void executeUndo(TRmbsClaimPageFullDto full, CallBackBusinessDataDto callBackBusinessData) {
    //     super.executeUndo(full, callBackBusinessData);
    //     // T{{templateNum}}特有的退回逻辑
    // }

}
