# 项目地图

## fssc-web

- 技术栈：`Vue 2.6`、`vue-router 3`、`vuex 3`、`Setaria`、`setaria-ui`、`fssc-web-framework`
- schema 输出目录：`src/json-schema`
- 业务主目录：`src/page`
- 路由主目录：`src/config/route`
- 常见页面类型：
- 搜索页：`src/page/**/index.vue + service.js + tableSchemaFile.js`
- 报账单：`src/page/claim/**/T***/`

## fssc-web-framework

- 技术栈：`Vue 2.6`、`TypeScript 配置混用`、`Setaria`
- 组件注册：`src/install.js`
- 入口导出：`src/lib.js`
- 文档示例：`doc/demo/*.md`
- 样式目录：`style/*.scss`
- schema 示例输出目录：`doc/json-schema`

## 关键约定

- schema 通常来自 swagger 生成，再在页面里做二次裁剪与增强
- API domain 来自 `Setaria.getHttp().<domain>`
- 业务页面优先按同目录现有页面的拆分方式新增文件
- 路由注册集中在 `src/config/route/**/index.js`

## 常见 domain

- `claim`
- `fund`
- `tr`
- `rtr`
- `config`
- `image`
- `cac`
- `invoice`
- `pi`
- `aam`
- `voucher`
- `bi`
