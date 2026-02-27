package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.impl;

import com.yili.claim.common.service.line.dto.TRmbsClaimLineDto;
import com.yili.claim.common.service.line.service.impl.BaseNewClaimLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}NewClaimLineService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-明细行新建服务实现
 * 
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}NewClaimLineServiceImpl extends BaseNewClaimLineService implements IT{{templateNum}}NewClaimLineService {


}
