package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.impl;

import com.yili.claim.common.service.pay.dto.ClaimClaimPayLineReqDto;
import com.yili.claim.common.service.pay.service.impl.BaseSaveClaimPayLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.IT{{templateNum}}SaveClaimPayLineService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-发票核销明细行保存服务实现
 * 
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}SaveClaimPayLineServiceImpl extends BaseSaveClaimPayLineService implements IT{{templateNum}}SaveClaimPayLineService {

}
