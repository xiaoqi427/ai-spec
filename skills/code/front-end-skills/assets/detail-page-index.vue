<template>
  <fssc-detail-page
    ref="detailPage"
    :label-mode.sync="labelMode"
    :status="workflowStatus"
    :claim-info="claimInfo"
    :loading="loading"
  >
    <template slot="header">
      <fssc-detail-page-header
        :title="claimTitle"
        :status="workflowStatus"
        :claim-info="claimInfo"
        @btn-click="headerBtnClick"
      />
    </template>

    <header-info ref="headerInfo" v-model="claimInfo" @done="saveOper" />

    <line-table
      v-if="lineTableSate"
      ref="lineTable"
      :claim-info="claimInfo"
      :claim-tabs="claimTabs"
      :claim-line="claimLine"
      @done="getInitData"
    />

    <fssc-workflow-submitter
      ref="workflowSubmitDrawer"
      :claim-info="claimInfo"
      @submit="submitBySubmitter"
    />

    <template slot="footer">
      <fssc-detail-page-footer
        ref="footer"
        :status="workflowStatus"
        :claim-info="claimInfo"
        @btn-click="footerBtnClickFn"
      />
    </template>
  </fssc-detail-page>
</template>

<script>
import HeaderInfo from './header/index.vue';
import LineTable from './table/index.vue';
import BaseMinxin from '@/page/claim/base/mixins/BaseMixin';
import WorkflowMixin from '@/page/claim/base/mixins/WorkflowMixin';
import {
  apiGetInitData,
  apiSaveData,
  apiSubmitData,
  apiDeleteData,
  apiCopyData,
} from './service';

export default {
  components: { HeaderInfo, LineTable },
  mixins: [BaseMinxin, WorkflowMixin],
  data() {
    return {
      callFun: {
        apiGetInitData,
        apiSaveData,
        apiSubmitData,
        apiDeleteData,
        apiCopyData,
      },
    };
  },
  methods: {
    footerBtnClickFn(type, info) {
      this.footerBtnClick(type, info);
    },
  },
};
</script>
