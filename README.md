# 国内直连规则数据

本仓库基于 Loyalsoldier/surge-rules，只生成国内域名、国内 IP 及本地网络的直连名单。名单以外的流量由客户端统一交给代理；没有按应用、国家、广告拦截划分的规则或代理组。

GitHub Actions 每天北京时间 06:30 构建，也支持手动触发。仅从固定的三个上游数据文件读取内容，生成并校验后才发布；下载或校验失败时保留上一份有效数据。构建的实际开始时间可能因 GitHub 排队延后。

release 分支仅包含：

- `direct.list`：Surge、Clash/Mihomo、小火箭使用的 classical RULE-SET。
- `direct.json`：sing-box 使用的 source rule-set。
- `manifest.json`：来源、时间、数量与校验值。
- `LICENSE`：许可证。

客户端模板、订阅、代理节点和凭据均不由本仓库构建或发布，数据更新不会覆盖客户端的分流结构。

数据来源为 Loyalsoldier/v2ray-rules-dat 的直连域名、Loyalsoldier/domain-list-custom 的私有域名，以及 Loyalsoldier/geoip 的中国 IP 列表。域名转换范围与原 Surge 项目保持一致，不展开 regexp/keyword 记录。
