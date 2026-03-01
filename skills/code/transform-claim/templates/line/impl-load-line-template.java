package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.impl;

import com.yili.claim.common.service.line.service.IBaseLoadClaimLineService;
import com.yili.claim.common.service.line.service.impl.BaseLoadClaimLineService;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-加载明细行服务实现
 *
 * 迁移自: ViewT{{templateNum}}ClaimLineService.java (老代码中多个View*合并)
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/service/TBaseService/ViewClaimLineService.java
 *
 * 基类 BaseLoadClaimLineService 已实现:
 * - load(full): 加载明细行主流程
 *   └ 判断是否已加载 → loadData（查行数据） → processClaimLines（逐行处理事件链） → preResult
 * - loadData(full): 查询claimId对应的所有行，调用processClaimLines
 * - processClaimLines(pageLine, full): 逐行处理，包含:
 *   └ amount（总计）→ adjustAmount（调整金额）→ loanAmount（借贷金额）→ foreignApplyAmount（外币合计）
 *   └ addCvtLineIds（计提单勾选）→ dcType（借贷方向）→ isEditMatter → addPreLine（个性化事件）
 * - preResult(pageLine, full): 空钩子，供子类重写个性化设置
 * - addPreLine(pageLine, full, loadParams): 空钩子，返回额外的行处理事件
 * - viewBrCrInfoLine/viewBrInfo/viewCrInfo/viewClaimBrInfo: 借贷方科目段信息查询
 *
 * 注意: @Service 的 value 命名规则为 "listAllT{XXX}ClaimLinesService"
 *
 * 可重写的钩子方法:
 * - preResult(pageLine, full): 行数据加载后的个性化设置（如合计金额、借贷方信息等）
 * - addPreLine(pageLine, full, loadParams): 添加额外的行处理事件（每行都会执行）
 *
 * @author {{author}}
 * @since {{date}}
 */
@Service(value = "listAllT{{templateNum}}ClaimLinesService")
public class T{{templateNum}}LoadClaimLineService extends BaseLoadClaimLineService implements IBaseLoadClaimLineService {

    // ============================================================
    // TODO: 从老代码迁移特有逻辑
    // ============================================================

    // 大多数单据类型不需要重写，直接继承基类即可。
    // 如果 T{{templateNum}} 有特殊的行加载后处理，可重写:
    //
    // /**
    //  * 行数据加载后的个性化设置
    //  * 原代码对应: ViewT{{templateNum}}ClaimLineService.java 第xx行
    //  */
    // @Override
    // public void preResult(TRmbsClaimLinePageDto pageLine, TRmbsClaimPageFullDto full) {
    //     // T{{templateNum}}特有处理
    // }

    // 如需为每行添加额外处理事件:
    //
    // @Override
    // protected List<Consumer<TRmbsClaimLineDto>> addPreLine(TRmbsClaimLinePageDto pageLine,
    //         TRmbsClaimPageFullDto full, LineLoadParams loadParams) {
    //     List<Consumer<TRmbsClaimLineDto>> events = new ArrayList<>();
    //     // events.add(line -> { /* T{{templateNum}}特有的行处理 */ });
    //     return events;
    // }

}
