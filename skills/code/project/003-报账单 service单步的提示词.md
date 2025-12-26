报账单 service每一步的提示词

# 先分析InsertT047ClaimLineService和UpdateT04ClaimLineService的逻辑，然后更新到新的框架T047SaveClaimLineServiceImpl,先分析你要处理的步骤，其中要遵守不能修改代码，需要变更请重写，如果存在逻辑直接调用父类方法，我确认后才能修改代码
# 注意一步步去做，每一步都是相同约束，如果老逻辑在新代码框架中已实现，帮忙备注，哪个类，哪个方法实现的
先分析老的逻辑，然后更新到新的框架对应service,陈述你的设计及处理的步骤，其中要遵守不能修改代码，需要变更请重写，如果存在逻辑直接调用父类方法，我确认后才能修改代码
* 遵守"不修改继承类的代码，需要变更请重写"的原则
* 调用isImagePool初始化影像状态是t_process_wi_record表和findImage的EIM_IMAGE不是一个东西
* 存在父类逻辑直接调用，不用确认了
* 逻辑要完整
* 抽离出的方法，方法注释上要写出原来代码对应行数
* NumberToCNUtil方法是存在的，其他都创建了
* 有些方法可以在claim-ptp,claim-eer中寻找下逻辑
* 不存在的字段创建在对应的DTO中，不要创建在DO中