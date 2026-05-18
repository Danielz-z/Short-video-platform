# 简历包装稿

## 项目名称

短视频平台数据库系统

## 推荐写法

**短视频平台数据库系统 | Python Flask, MySQL, Jinja2**

基于 Flask + MySQL 设计并实现短视频平台数据库应用，覆盖用户、视频、点赞、评论、关注、私信、标签等核心业务模块；完成从单文件课程项目到分层后端架构的工程化重构，并围绕权限、安全、索引优化和并发实验进行二次打磨。

## 简历要点

- 设计 9 张核心业务表，使用主键、外键、唯一约束和 CHECK 约束保证用户、视频、点赞、评论、关注等数据的一致性和完整性。
- 将原始单文件 Flask 应用重构为 `routes / services / dao` 分层架构，拆分 HTTP 处理、业务规则和 SQL 访问逻辑，提高代码可维护性。
- 实现基于 `users.role` 的管理员权限控制，替代用户名判断；使用 Werkzeug 哈希存储密码，并支持旧明文密码登录后自动升级。
- 使用 UUID 生成用户和视频主键，避免并发场景下 `COUNT(*)` 生成 ID 带来的冲突风险；通过 `(user_id, video_id)` 唯一约束防止重复点赞。
- 编写存储过程封装热门视频查询、视频插入、标题更新和视频删除，并在 DAO 层保留普通 SQL fallback，提升本地开发鲁棒性。
- 针对作者页、领域筛选、时间线排序、热门视频等高频访问路径设计二级索引和复合索引，分析索引对读写性能的影响。
- 编写并发插入/查询压测脚本，输出 QPS、平均延迟、P95 延迟，并提供日志汇总脚本用于索引优化前后对比。
- 补充服务层单元测试，覆盖密码策略、角色鉴权、用户创建、视频作者权限校验等核心业务规则。
- 使用 Docker Compose 编排 Flask + MySQL 本地开发环境，支持一条命令启动服务并自动初始化数据库结构、索引、存储过程和种子数据。

## 更短版本

基于 Flask + MySQL 实现短视频平台数据库系统，设计 9 张业务表并使用外键、唯一约束、CHECK 约束保障数据一致性；将单文件课设重构为 `routes / services / dao` 分层架构，加入角色权限、密码哈希、UUID 主键、存储过程、索引优化、并发压测脚本、服务层单元测试和 Docker Compose 一键启动环境。

## 英文简历版本

Built a Flask + MySQL short video platform database system with normalized schema design, role-based administration, password hashing, stored procedures, composite indexes, concurrent benchmark scripts, service-layer unit tests, and Docker Compose local deployment.

## 项目关键词

`Python` `Flask` `MySQL` `Jinja2` `Docker Compose` `数据库设计` `三范式` `外键约束` `索引优化` `存储过程` `权限控制` `密码哈希` `并发压测` `单元测试`
