package com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.impl;

import com.yili.claim.common.service.pay.dto.ClaimClaimPayLineReqDto;
import com.yili.claim.common.service.pay.dto.TRmbsPaylistDto;
import com.yili.claim.common.service.pay.service.impl.BaseNewClaimPayLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.IT{{templateNum}}NewClaimPayLineService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * T{{templateNum}}{{businessDesc}}-发票核销明细行新建服务实现
 * 
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@Service
public class T{{templateNum}}NewClaimPayLineServiceImpl extends BaseNewClaimPayLineService implements IT{{templateNum}}NewClaimPayLineService {


}
