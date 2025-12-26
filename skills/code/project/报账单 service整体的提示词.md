报账单 service整体的提示词

# 参考md的整体文件，md有老代码路径，没有需要提供。更新T048的逻辑
## 1，更新New接口报账单头对应service
老逻辑：NewT048ClaimService
转换到新的：T048NewClaimServiceImpl

## 2，更新New接口报账单行对应的service
老逻辑：NewT048ClaimLineService
转换到新的 T048NewClaimLineServiceImpl

## 3，更新save接口报账单头对应service
老逻辑：InsertT048ClaimService，UpdateT048ClaimService
转换到新的：T048SaveClaimServiceImpl


## 4，更新save接口报账单行对应service
老逻辑：InsertT048ClaimLineService，UpdateT048ClaimLineService
转换到新的：T048SaveClaimLineServiceImpl


## 5，更新delete报账单对应service
老逻辑：DeleteT048ClaimService,DeleteT048ClaimLinesService
转换到新的：T048DeleteClaimLineServiceImpl



## 7，更新load报账单对应service，注意这里以前老逻辑分头行，现在合并了
老逻辑：LoadAllT048Service，ViewT048ClaimService，ViewT048ClaimLineService
转换到新的：T048LoadClaimServiceImpl



# 注意一步步去做，每一步都是相同约束，如果老逻辑在新代码框架中已实现，帮忙备注，哪个类，哪个方法实现的
先分析老的逻辑，然后更新到新的框架对应service,陈述你的设计及处理的步骤，其中要遵守不能修改代码，需要变更请重写，如果存在逻辑直接调用父类方法，我确认后才能修改代码
* 遵守"不修改代码，需要变更请重写"的原则
* 调用isImagePool初始化影像状态是t_process_wi_record表和findImage的EIM_IMAGE不是一个东西
* 存在父类逻辑直接调用，不用确认了
* 逻辑要完整
* 抽离出的方法，方法注释上要写出原来代码对应行数
* NumberToCNUtil方法是存在的，其他都创建了
* 有些方法可以在claim-ptp,claim-eer中寻找下逻辑
* 不存在的字段创建在对应的DTO中，不要创建在DO中


