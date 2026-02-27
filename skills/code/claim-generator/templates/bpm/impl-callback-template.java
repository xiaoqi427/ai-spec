package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.bpm.impl;

import com.yili.claim.common.service.claim.service.impl.BaseCallBackClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.bpm.IT{{templateNum}}CallBackClaimService;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-BPM回调服务实现
 * 
 * 用于处理BPM流程回调事件，如：
 * - 流程提交后回调
 * - 流程审批通过回调
 * - 流程驳回回调
 * - 流程撤回回调
 *
 * @author {{author}}
 * @since {{date}}
 */
@Service
public class T{{templateNum}}CallBackClaimServiceImpl extends BaseCallBackClaimService implements IT{{templateNum}}CallBackClaimService {
    
    // 如需自定义回调逻辑，可以重写BaseCallBackClaimService中的方法
    // 例如：
    // @Override
    // protected void afterSubmit(Long claimId) {
    //     log.debug("T{{templateNum}}CallBackClaimServiceImpl.afterSubmit - claimId: {}", claimId);
    //     // TODO: 添加T{{templateNum}}提交后的特定处理逻辑
    // }
}
