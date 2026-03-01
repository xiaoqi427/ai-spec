package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.impl;

import com.yili.claim.common.service.claim.dto.TRmbsClaimPageDto;
import com.yili.claim.common.service.claim.dto.TRmbsClaimPageFullDto;
import com.yili.claim.common.service.claim.service.impl.BaseLoadClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}LoadClaimService;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-加载服务实现
 *
 * 迁移自（多个合并）:
 * - LoadAllT{{templateNum}}Service.java
 * - ViewT{{templateNum}}ClaimService.java
 * - ViewT{{templateNum}}ClaimLineService.java
 * - ViewT{{templateNum}}ClaimBankReceiptService.java (如有)
 * - ViewT{{templateNum}}ClaimBankReceiptVendorService.java (如有)
 * - ViewT{{templateNum}}ClaimBankReceiptOneVendorService.java (如有)
 * 原代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/
 *
 * 基类 BaseLoadClaimService 已实现:
 * - load(): 加载主流程（查询 → 权限 → 公共信息 → preResult → 黑名单 → 数据补偿 → 记录审批时间）
 * - loadCommonInfo(): 大类/小类/合同/行信息/银行/附件/电子影像/按钮权限
 * - loadAllLine(): 明细行/税金/付款行/借款核销/发票核销
 * - permissionValidation(): 权限校验
 * - viewBrCrInfoLine/viewCrInfo/viewBrInfo(): 借贷8段值
 * - loadBankList/loadBankLineList(): 银行信息
 *
 * 子类主要通过 preResult() 钩子实现个性化逻辑
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}LoadClaimServiceImpl extends BaseLoadClaimService implements IT{{templateNum}}LoadClaimService {

    /**
     * 个性数据加载
     *
     * 原代码对应: LoadAllT{{templateNum}}Service.java
     *
     * 迁移指引:
     * 1. 分析 LoadAllT{{templateNum}}Service 的 execute()/preResult() 方法
     * 2. 分析 ViewT{{templateNum}}ClaimService/ViewT{{templateNum}}ClaimLineService 的逻辑
     * 3. 基类已处理的（公共信息加载、明细行、附件等）直接跳过
     * 4. T{{templateNum}}特有的加载逻辑写在此方法中
     * 5. 注释中标注原来代码对应行数
     */
    @Override
    protected TRmbsClaimPageFullDto preResult(TRmbsClaimPageFullDto claimPageFull, UserObjectFullDto user) {
        log.info("T{{templateNum}}LoadClaimServiceImpl.preResult开始，claimId={}", claimPageFull.getClaimId());

        // 调用父类默认处理
        super.preResult(claimPageFull, user);

        TRmbsClaimPageDto claim = claimPageFull.getClaim();

        // ============================================================
        // TODO: 从老代码迁移 T{{templateNum}} 特有加载逻辑
        // ============================================================

        // 示例：设置影像池状态
        // 原代码对应: LoadAllT{{templateNum}}Service.java 第xx行
        // claim.setIsImagePool(super.isImagePool(claimPageFull.getClaimId()));

        // 示例：加载借贷8段值
        // 原代码对应: ViewT{{templateNum}}ClaimLineService.java 第xx行
        // viewBrCrInfoLine(claimPageFull, user);
        // viewCrInfo(claimPageFull, user);

        // 示例：加载黑名单
        // loadAllBlacklist(claimPageFull);

        // 示例：加载银行信息
        // loadClaimBankInfo(claimPageFull);

        // 示例：T{{templateNum}}特有金额计算
        // calculateT{{templateNum}}Amount(claimPageFull);

        log.info("T{{templateNum}}LoadClaimServiceImpl.preResult完成，claimId={}", claimPageFull.getClaimId());
        return claimPageFull;
    }
}
