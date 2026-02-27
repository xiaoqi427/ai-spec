package com.yili.claim.{{module}}.web.controller.claim;

import com.yili.claim.common.service.claim.dto.TRmbsClaimPageDto;
import com.yili.claim.common.service.claim.dto.TRmbsClaimPageFullDto;
import com.yili.claim.common.service.line.dto.TRmbsClaimLineDto;
{{#if withPay}}
import com.yili.claim.common.service.pay.dto.ClaimClaimPayLineReqDto;
import com.yili.claim.common.service.pay.dto.ClaimPayListReqParams;
import com.yili.claim.common.service.pay.dto.TRmbsPaylistDto;
import com.yili.claim.common.entity.pay.TRmbsPaylistDo;
import com.yili.claim.common.service.pay.service.ITRmbsPaylistInitService;
{{/if}}
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}DeleteClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}LoadClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}NewClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.head.IT{{templateNum}}SaveClaimService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}DeleteClaimLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}NewClaimLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}SaveClaimLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.line.IT{{templateNum}}UpdateClaimLineService;
{{#if withPay}}
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.IT{{templateNum}}DeleteClaimPayLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.IT{{templateNum}}NewClaimPayLineService;
import com.yili.claim.{{module}}.claim.t{{templateNumLower}}.pay.IT{{templateNum}}SaveClaimPayLineService;
{{/if}}
import com.yili.common.constant.claim.ClaimTemplateEnum;
import com.yili.config.sys.api.param.dto.UserObjectFullDto;
import com.yili.fssc.util.lang.Assert;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.annotation.Resource;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

{{#if withPay}}
import java.util.List;
{{/if}}

/**
 * {{businessDesc}}Controller
 *
 * @author {{author}}
 * @since {{date}}
 */
@Slf4j
@RestController
@RequestMapping("T{{templateNum}}")
@Tag(name = "({{moduleUpper}}){{businessCategory}}/{{businessDesc}}(T{{templateNum}})", description = "{{businessDesc}}")
public class T{{templateNum}}ClaimController {

    private final String itemId = ClaimTemplateEnum.T{{templateNum}}.name();

    // ==================== Head Services ====================
    
    @Resource
    private IT{{templateNum}}NewClaimService newClaimService;

    @Resource
    private IT{{templateNum}}LoadClaimService loadClaimService;

    @Resource
    private IT{{templateNum}}SaveClaimService saveClaimService;

    @Resource
    private IT{{templateNum}}DeleteClaimService deleteClaimService;

    // ==================== Line Services ====================
    
    @Resource
    private IT{{templateNum}}NewClaimLineService newClaimLineService;

    @Resource
    private IT{{templateNum}}SaveClaimLineService saveClaimLineService;

    @Resource
    private IT{{templateNum}}UpdateClaimLineService updateClaimLineService;

    @Resource
    private IT{{templateNum}}DeleteClaimLineService deleteClaimLineService;

{{#if withPay}}
    // ==================== Pay Services ====================
    
    @Resource
    private ITRmbsPaylistInitService paylistInitService;

    @Resource
    private IT{{templateNum}}NewClaimPayLineService newClaimPayLineService;

    @Resource
    private IT{{templateNum}}SaveClaimPayLineService saveClaimPayLineService;

    @Resource
    private IT{{templateNum}}DeleteClaimPayLineService deleteClaimPayLineService;

{{/if}}
    // ==================== Head Endpoints ====================

    @Operation(summary = "新增-页面初始化", description = "新增-页面初始化")
    @PostMapping(value = "new")
    public TRmbsClaimPageDto newClaim(@Schema(hidden = true) UserObjectFullDto user) {
        Assert.notNull(user, "[(#{sys.auth.require.login})]");
        return newClaimService.newClaim(itemId, user);
    }

    @Operation(summary = "报账单加载", description = "报账单加载")
    @PostMapping(value = "load")
    public TRmbsClaimPageFullDto load(@RequestBody TRmbsClaimPageDto param, @Schema(hidden = true) UserObjectFullDto user) {
        Assert.notNull(user, "[(#{sys.auth.require.login})]");
        return loadClaimService.load(param, user);
    }

    @Operation(summary = "报账单保存", description = "报账单保存")
    @PostMapping(value = "save")
    public TRmbsClaimPageDto save(@RequestBody TRmbsClaimPageDto param, @Schema(hidden = true) UserObjectFullDto user) {
        Assert.notNull(user, "[(#{sys.auth.require.login})]");
        return saveClaimService.save(param, user);
    }

    @SneakyThrows
    @Operation(summary = "T{{templateNum}}-删除", description = "T{{templateNum}}-删除")
    @PostMapping(value = "delete")
    public void deleteClaimHead(@RequestBody TRmbsClaimPageDto param, @Schema(hidden = true) UserObjectFullDto user) {
        Assert.notNull(user, "[(#{sys.auth.require.login})]");
        deleteClaimService.delete(param.getClaimId());
    }

    // ==================== Line Endpoints ====================

    @Operation(summary = "T{{templateNum}}明细行初始化", description = "T{{templateNum}}明细行初始化")
    @PostMapping(value = "newClaimLine")
    public TRmbsClaimLineDto newClaimLine(@RequestParam Long claimId) {
        return newClaimLineService.newClaimLine(claimId);
    }

    @Operation(summary = "T{{templateNum}}明细行新增", description = "T{{templateNum}}明细行新增")
    @PostMapping(value = "saveClaimLine")
    public TRmbsClaimLineDto saveClaimLine(@RequestBody TRmbsClaimLineDto claimLineDto) {
        return saveClaimLineService.saveClaimLine(claimLineDto);
    }

    @Operation(summary = "T{{templateNum}}明细行修改", description = "T{{templateNum}}明细行修改")
    @PostMapping(value = "updateClaimLine")
    public TRmbsClaimLineDto updateClaimLine(@RequestBody TRmbsClaimLineDto claimLineDto) {
        return updateClaimLineService.updateClaimLine(claimLineDto);
    }

    @Operation(summary = "T{{templateNum}}明细行删除", description = "T{{templateNum}}明细行删除")
    @PostMapping(value = "deleteClaimLine")
    public void deleteClaimLine(@RequestBody TRmbsClaimLineDto claimLineDto) {
        deleteClaimLineService.deleteClaimLine(claimLineDto);
    }

{{#if withPay}}
    // ==================== Pay Endpoints ====================

    @Operation(summary = "T{{templateNum}}计划付款初始化", description = "T{{templateNum}}计划付款初始化")
    @PostMapping(value = "initPaylist")
    public TRmbsPaylistDo initPaylist(@RequestBody ClaimPayListReqParams params, @Schema(hidden = true) UserObjectFullDto user) {
        Assert.notNull(user, "[(#{sys.auth.require.login})]");
        return paylistInitService.initPaylist(params);
    }

    @Operation(summary = "T{{templateNum}}发票核销明细行初始化(新增按钮)", description = "T{{templateNum}}发票核销明细行初始化(新增按钮)")
    @PostMapping(value = "newClaimPayLine")
    public List<TRmbsPaylistDto> newClaimPayLine(@RequestBody ClaimClaimPayLineReqDto payLineReqDto) {
        return newClaimPayLineService.newClaimPayLine(payLineReqDto);
    }

    @Operation(summary = "T{{templateNum}}发票核销明细行保存", description = "T{{templateNum}}发票核销明细行保存")
    @PostMapping(value = "saveClaimPayLine")
    public void saveClaimPayLine(@RequestBody ClaimClaimPayLineReqDto payLineReqDto) {
        saveClaimPayLineService.saveClaimPayLine(payLineReqDto);
    }

    @Operation(summary = "T{{templateNum}}发票核销明细行删除", description = "T{{templateNum}}发票核销明细行删除")
    @PostMapping(value = "deleteClaimPayLine")
    public void deleteClaimPayLine(@RequestBody ClaimClaimPayLineReqDto payLineReqDto) {
        deleteClaimPayLineService.deleteClaimPayLine(payLineReqDto);
    }
{{/if}}
}
