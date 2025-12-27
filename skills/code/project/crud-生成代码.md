生成代码提示词
帮忙给的表生成代码，服务为otc，模块为discount，注意下各个工程的包路径可能不一样，需要先自己找下包路径



数据库表单脚本如下：

CREATE TABLE "YLADMIN"."T_RMBS_CLAIM_PRE_DISCOUNT" 
   (	"ID" NUMBER NOT NULL ENABLE, 
	"CLAIM_ID" NUMBER, 
	"CLAIM_NO" VARCHAR2(20), 
	"MATERIAL_NO" VARCHAR2(50), 
	"MATERIAL_NAME" VARCHAR2(200), 
	"TAX_CODE" VARCHAR2(20), 
	"UOM_CODE" VARCHAR2(20), 
	"FOREIGN_APPLY_AMOUNT" NUMBER(20,2), 
	"TENANT_CODE" VARCHAR2(50), 
	 CONSTRAINT "T_RMBS_CLAIM_PRE_DISCOUNT_PK" UNIQUE ("ID")


页面字段提供截图
没有就跳过

约束：
1，不生成controller,service
2,生成到claim-otc模块下

生成完需要确认