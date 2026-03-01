package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head;

import com.yili.claim.common.service.claim.service.IBaseLoadClaimService;

/**
 * T{{templateNum}}{{businessDesc}}-加载服务接口
 *
 * 对应旧代码（合并多个）:
 * - LoadAllT{{templateNum}}Service.java (加载全部)
 * - ViewT{{templateNum}}ClaimService.java (查看报账单头)
 * - ViewT{{templateNum}}ClaimLineService.java (查看报账单行)
 * - ViewT{{templateNum}}ClaimBankReceiptService.java (银行回单，如有)
 * - ViewT{{templateNum}}ClaimBankReceiptVendorService.java (银行回单供应商，如有)
 * - ViewT{{templateNum}}ClaimBankReceiptOneVendorService.java (银行回单单供应商，如有)
 * 旧代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/
 *
 * @author {{author}}
 * @since {{date}}
 */
public interface IT{{templateNum}}LoadClaimService extends IBaseLoadClaimService {

}
