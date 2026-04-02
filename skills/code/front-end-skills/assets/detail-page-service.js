import {
  commonApiLoadClaim,
  commonApiInitClaim,
  commonApiSaveOrUpateData,
  commonApiSubmitData,
  commonApiDeleteData,
  commonApiCopyData,
  commonApiInitLineData,
  commonApiSaveLineData,
  commonApiUpdateLineData,
  commonApiDeleteLineData,
} from '@/page/claim/base/service/';

const itemId = 'T000';

export const apiGetInitData = (claimId) => {
  if (claimId) {
    return commonApiLoadClaim(itemId, claimId);
  }
  return commonApiInitClaim(itemId);
};

export const apiSaveData = (params) => commonApiSaveOrUpateData(itemId, params);
export const apiDeleteData = (claimId) => commonApiDeleteData(itemId, claimId);
export const apiSubmitData = (claimId) => commonApiSubmitData(claimId);
export const apiCopyData = (claimId) => commonApiCopyData(itemId, claimId);

export const apiInitLineData = (claimId) => commonApiInitLineData(itemId, claimId);
export const apiSaveLineData = (params) => commonApiSaveLineData(itemId, params);
export const apiUpdateLineData = (params) => commonApiUpdateLineData(itemId, params);
export const apiDeleteLineData = (lineIds) => commonApiDeleteLineData(itemId, lineIds);
