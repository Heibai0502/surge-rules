# 国内直连、私有域名与广告过滤规则数据

本仓库读取 Loyalsoldier 的直连、海外、私有域名、中国 IP 和广告 reject-list.txt 五份固定来源。私有域名和广告名单独立生成，不增加应用、国家或广告代理组。发布数据不包含节点、模板、手动组或凭据。

GitHub 工作流每天北京时间 06:30 计划构建，VpsCT 每 4 小时检查并转换资源，客户端每 24 小时更新。计划时间不等于每次实际成功时间。下载失败、广告名单为空、过大、含过宽条目或误覆盖受保护网站时停止发布，保留上一份有效数据。

release 包含 direct.list、direct.json、direct.domains、direct.ipcidr、private.domains、proxy-source.txt、reject.domains、reject.list、reject.json、manifest.json 和 LICENSE。manifest 记录同一代来源、条数、时间和逐文件校验值。下载超过 16MiB 会拒绝。

private.domains 保留精确域名和带点后缀的区别，客户端须在海外与广告名单之前匹配。为兼容旧客户端，直连名单仍保留这些私有条目；仅合并进直连名单不足以解决 router.asus.com 与 .asus.com 等重叠。proxy-source.txt 是本次清洗直连名单时使用的海外原始文本，消费者应从同一 release 获取它，并核对 manifest，避免拼接不同时刻的上游名单。中国 IP 资源继续发布，但当前 VpsCT 完整订阅不将其作为通用直连兜底。

修改构建逻辑后执行 `python3 -B -m unittest discover -s scripts -p 'test_*.py'`。工作流先测试，再构建和发布；精确条目不能扩大成后缀，私有名单为空、过宽或覆盖受保护公网服务时拒绝发布。

完整订阅携带广告过滤；管理员可在 VpsCT 运行页启停过滤、填写误拦白名单，修改后需刷新整份订阅。白名单只跳过广告拦截，仍按原分流处理。raw / URI 无法携带过滤规则。

DNS/域名规则不能可靠过滤与正常内容共用域名的视频广告，不承诺全站无广告。服务器转换、策略和实体手机验收由父项目维护；源数据发布成功不能代替客户端验收。
