<template>
  <fssc-search-page
    ref="table"
    :schema="schema"
    :condition-schema="conditionSchema"
    :condition-ui-schema="conditionUiSchema"
    :condition-data="conditionData"
    :table-schema="tableSchema"
    :table-ui-schema="tableUiSchema"
    :request="handleSearch"
    :label-mode="true"
    :row-buttons="getRowButton"
    @clear="handleClear"
    @row-button-click="onRowButtonClick"
  >
    <template
      slot="condition.orgId"
      slot-scope="scope"
    >
      <fssc-org-select v-model="scope.data.orgId" />
    </template>
  </fssc-search-page>
</template>

<script>
import { SchemaUtils } from 'fssc-web-framework';
import { tableSchemaData } from './tableSchemaFile';
import { apiGetDataList } from './service';

export default {
  data() {
    return {
      schema: {},
      conditionSchema: ['orgId'],
      conditionUiSchema: {},
      conditionData: {},
      tableSchema: [],
      tableUiSchema: {},
    };
  },
  created() {
    this.initSchema();
  },
  methods: {
    initSchema() {
      const schema = this.$getSchemaByApiKey('Claim', 'ExampleDto');
      SchemaUtils.replaceSchemaLabels(schema, {
        orgId: '公司OU',
      });
      this.schema = schema;
      this.tableSchema = tableSchemaData.tableSchema;
      this.tableUiSchema = tableSchemaData.tableUiSchema;
      this.conditionData = this.$createDefaultObjectBySchema(schema);
    },
    handleSearch(params) {
      return apiGetDataList(params);
    },
    handleClear() {
      this.conditionData = this.$createDefaultObjectBySchema(this.schema);
    },
    getRowButton() {
      return [{ key: 'view', label: '查看' }];
    },
    onRowButtonClick() {},
  },
};
</script>
