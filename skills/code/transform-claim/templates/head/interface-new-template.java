package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head;

import com.yili.claim.common.service.claim.service.IBaseNewClaimService;

/**
 * T{{templateNum}}{{businessDesc}}-新建服务接口
 *
 * 对应旧代码: NewT{{templateNum}}ClaimService.java
 * 旧代码路径: yldc-caiwugongxiangpingtai-fsscYR-master/src/com/ibm/gbs/efinance/business/ylService/claim/T{{templateNum}}/NewT{{templateNum}}ClaimService.java
 *
 * @author {{author}}
 * @since {{date}}
 */
public interface IT{{templateNum}}NewClaimService extends IBaseNewClaimService {
    // 继承父接口 IBaseNewClaimService.newClaim() 方法
    // 具体实现见 T{{templateNum}}NewClaimServiceImpl
}
