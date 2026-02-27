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
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}LoadClaimServiceImpl extends BaseLoadClaimService implements IT{{templateNum}}LoadClaimService {

    @Override
    protected TRmbsClaimPageFullDto postExecute(TRmbsClaimPageFullDto claimPageFullDto, TRmbsClaimPageDto param, UserObjectFullDto user) {
        log.debug("T{{templateNum}}LoadClaimServiceImpl.postExecute开始");
        
        // TODO: 添加T{{templateNum}}加载后的特定处理逻辑
        
        log.debug("T{{templateNum}}LoadClaimServiceImpl.postExecute完成");
        return claimPageFullDto;
    }
}
