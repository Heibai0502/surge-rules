# 国内直连与广告过滤规则数据

本仓库读取 Loyalsoldier 的直连、海外、私有域名、中国 IP 和广告 reject-list.txt 五份固定来源。广告名单单独生成，不增加应用、国家或广告代理组。发布数据不包含节点、模板、手动组或凭据。

GitHub 工作流每天北京时间 06:30 计划构建，VpsCT 每 4 小时检查并转换资源，客户端每 24 小时更新。计划时间不等于每次实际成功时间。下载失败、广告名单为空、过大、含过宽条目或误覆盖受保护网站时停止发布，保留上一份有效数据。

release 包含 direct.list、direct.json、direct.domains、direct.ipcidr、reject.domains、reject.list、reject.json、manifest.json 和 LICENSE。manifest 记录同一代来源、条数、时间和逐文件校验值。下载超过 16MiB 会拒绝。

完整订阅携带广告过滤；管理员可在 VpsCT 运行页启停过滤、填写误拦白名单，修改后需刷新整份订阅。白名单只跳过广告拦截，仍按原分流处理。raw / URI 无法携带过滤规则。

DNS/域名规则不能可靠过滤与正常内容共用域名的视频广告，不承诺全站无广告。服务器转换、策略和实体手机验收由父项目维护；源数据发布成功不能代替客户端验收。
