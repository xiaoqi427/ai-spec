import Setaria from 'setaria';

const request = Setaria.getHttp().claim;

export const apiGetDataList = (params) => request.post('/example/query', params);

export const apiExportData = (params) => request.post('/example/export', params, {
  responseType: 'arraybuffer',
  showLoading: true,
});
