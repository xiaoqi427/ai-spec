package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.impl;

import com.yili.claim.common.service.claim.dto.TRmbsClaimPageDto;
import com.yili.claim.common.service.claim.service.impl.BaseNewClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}NewClaimService;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-新建服务实现
 * 
 * T{{templateNum}}特点：
 * - {{businessDesc}}
 * - {{feature1}}
 * - {{feature2}}
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}NewClaimServiceImpl extends BaseNewClaimService implements IT{{templateNum}}NewClaimService {

    @Override
    protected TRmbsClaimPageDto preExecute(TRmbsClaimPageDto claim, UserObjectFullDto user) {
        log.debug("T{{templateNum}}NewClaimServiceImpl.preExecute开始");

        // 报销人Id
        claim.setExpenseIssuerId(user.getUserid());
        // 报销人名称
        claim.setExpenseIssuerName(user.getFullname());
        // 报销人所在部门
        claim.setExpenseIssuerDeptId(user.getCurGroupId());
        
        // TODO: 添加T{{templateNum}}特定的业务逻辑
        
        log.debug("T{{templateNum}}NewClaimServiceImpl.preExecute完成");
        return claim;
    }
}
