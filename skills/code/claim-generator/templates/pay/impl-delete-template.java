package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.impl;

import com.yili.claim.common.service.pay.dto.ClaimClaimPayLineReqDto;
import com.yili.claim.common.service.pay.service.impl.BaseDeleteClaimPayLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.IT{{templateNum}}DeleteClaimPayLineService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * T{{templateNum}}{{businessDesc}}-发票核销明细行删除服务实现
 * 
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}DeleteClaimPayLineServiceImpl extends BaseDeleteClaimPayLineService implements IT{{templateNum}}DeleteClaimPayLineService {


}
