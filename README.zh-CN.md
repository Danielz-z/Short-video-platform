# 短视频平台

[English][en] | 简体中文

[![CI](https://github.com/Danielz-z/Short-video-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Danielz-z/Short-video-platform/actions/workflows/ci.yml)

一个工程化的 Flask + MySQL 短视频平台数据库系统。本项目由数据库课程设计升级为一个可用于作品集展示的后端项目，包含规范化的关系模型、分层 Flask 架构、基于角色的管理、安全加固，以及可复现的数据库性能实验。

---

## 项目亮点

- **作品集级后端项目**：将数据库课程设计升级为 Flask + MySQL 短视频平台。
- **规范化关系建模**：9 张业务表，包含约束、索引和存储过程。
- **分层 Flask 架构**：`routes / services / dao` 三层，配合 MySQL 连接池。
- **安全加固**：密码哈希、UUID 主键、基于角色的管理员权限，以及基于 POST 的破坏性操作。
- **数据库性能实验**：索引前后对比，查询吞吐从 **363.63 QPS 提升至 1,390.38 QPS**。
- **CI/CD 就绪**：GitHub Actions + Docker Compose 一键启动。

---

## 项目价值

本项目聚焦短视频平台的数据库与后端工程：

- 建模核心业务实体：用户、视频、点赞、评论、关注、消息、标签和内容领域。
- 利用 MySQL 约束、索引和存储过程保障数据一致性，并支持常见访问路径。
- 将课程风格的单文件 Flask 应用重构为可维护的 `routes / services / dao` 结构。
- 增加安全性与可靠性改进：密码哈希、基于环境的配置、UUID 主键、基于角色的管理员权限，以及基于 POST 的破坏性操作。
- 提供并发压测脚本和日志汇总工具，用于索引实验分析。

## 技术栈

| 领域 | 技术 |
| --- | --- |
| 后端 | Python, Flask, Jinja2 |
| 数据库 | MySQL 8.x, InnoDB, 存储过程, 索引 |
| 数据访问 | mysql-connector-python, 连接池, DAO 层 |
| 安全 | Werkzeug 密码哈希, 环境变量, 基于角色的访问控制 |
| 测试 | unittest, unittest.mock |
| CI | GitHub Actions |
| 实验 | Python threading, CSV 日志, pandas, matplotlib |
| 部署 | Docker, Docker Compose |

## 工程亮点

| 亮点 | 实现 |
| --- | --- |
| 分层后端 | `routes` 处理 HTTP/模板，`services` 处理业务规则，`dao` 处理 SQL 和存储过程 |
| 关系建模 | 9 张业务表，包含主键、外键、唯一约束和 CHECK 约束 |
| 角色授权 | 通过 `users.role` 字段控制管理员访问，而非用户名约定 |
| 密码安全 | 新密码进行哈希；历史明文密码在成功登录后升级 |
| 并发安全 | UUID 视频/用户 ID 避免基于计数的 ID 冲突；点赞使用唯一 `(user_id, video_id)` 约束 |
| 连接复用 | Flask 请求使用 MySQL 连接池，而非每次查询新建连接 |
| 查询优化 | 二级索引和复合索引支撑作者主页、分类筛选、时间线和热门视频排行 |
| 分页读取 | 管理员用户列表和个人视频列表采用 `COUNT + LIMIT/OFFSET` 分页 |
| 性能实验 | 插入/查询/混合压测脚本输出 QPS、平均延迟和 P95 延迟 |
| 可测试性 | 服务层单元测试覆盖密码策略、角色授权、用户创建和所有权校验 |
| 持续集成 | GitHub Actions 在 push 和 pull request 时运行单元测试与 Python 语法检查 |
| 一键启动 | Docker Compose 启动 Flask 和 MySQL，并初始化表结构、索引、存储过程和种子数据 |

## 功能特性

- 用户登录，以及由管理员基于角色管理的用户注册
- 用户资料查看、编辑和删除
- 分页展示用户列表和视频列表
- 视频上传、详情查看、标题更新和删除
- 点赞记录，防止重复点赞
- 数据库备份和恢复入口
- MySQL 表结构、索引、存储过程和种子数据脚本
- 并发插入/查询压测脚本，输出 QPS、平均延迟和 P95 延迟
- 密码校验、角色授权和视频所有权的单元测试
- Docker Compose 本地环境，一键启动 Flask + MySQL

## 项目架构图

### 系统架构

<p align="center">
  <img src="docs/assets/architecture.png" alt="短视频平台系统架构" width="900">
</p>

架构图展示了分层的 Flask 后端、MySQL 数据模型、数据库脚本，以及独立的性能实验工作流。

### 数据库性能实验

<p align="center">
  <img src="docs/assets/performance-results.png" alt="数据库性能实验对比" width="900">
</p>

性能图总结了索引实验的预期对比形式：添加索引前后的查询延迟和 QPS。

## 应用截图

以下截图来自原课程项目文档，展示主要用户工作流。

| 登录 | 视频大盘 |
| --- | --- |
| <img src="docs/assets/screenshots/login.png" alt="登录页" width="420"> | <img src="docs/assets/screenshots/video-dashboard.png" alt="视频大盘" width="420"> |

| 上传视频 | 管理员后台 |
| --- | --- |
| <img src="docs/assets/screenshots/upload-video.png" alt="上传视频页" width="420"> | <img src="docs/assets/screenshots/admin-dashboard.png" alt="管理员后台" width="420"> |

## 目录结构

```text
backend/
  app.py              # Flask 应用入口
  config.py           # 基于环境的配置
  routes/             # HTTP 和模板层
  services/           # 业务规则
  dao/                # SQL 和存储过程访问
  utils/db.py         # MySQL 连接池助手
database/             # 表结构、索引、存储过程、种子数据、备份
experiments/          # 插入/查询/并发性能实验
docs/                 # 设计和性能分析文档
```

## 数据库设计

核心表：

- `users`：用户账户，使用 UUID 主键、哈希密码和基于角色的访问控制
- `videos`：视频元数据，关联作者和内容领域
- `likes`：点赞事件，使用唯一 `(user_id, video_id)` 约束
- `comments`：评论记录，关联用户和视频

辅助表包括 `fields`、`tags`、`video_tags`、`follows` 和 `messages`，用于保留原平台功能。

## 路由参考

详见 [docs/api.md](docs/api.md)，包含 Flask 路由参考、路由层映射和压测命令入口。

## 简历与面试资料

- 中文简历包装：[docs/resume_zh.md](docs/resume_zh.md)
- 英文简历包装：[docs/resume.md](docs/resume.md)
- 面试要点：[docs/interview_guide_zh.md](docs/interview_guide_zh.md)

## 性能优化

关键索引定义在 `database/indexes.sql`：

```sql
CREATE INDEX idx_videos_author_id ON videos(author_id);
CREATE INDEX idx_videos_field_id ON videos(field_id);
CREATE INDEX idx_videos_upload_time ON videos(upload_time);
```

这些索引优化了作者主页、分类筛选、时间线排序和热门视频查询。实验系统用于对比添加二级索引前后的效果。

本地压测记录见 [docs/performance_results.md](docs/performance_results.md)。在记录的 Docker/MySQL 运行中，添加 `idx_videos_upload_time` 将最新视频查询吞吐从 363.63 QPS 提升至 1,390.38 QPS。

## 实验输出

压测脚本输出：

- 总操作数
- 耗时
- 平均延迟
- P95 延迟
- QPS

日志写入 `experiments/logs`。图表可使用 `experiments/analysis/draw_pictures.py` 生成，Markdown 汇总可使用 `experiments/analysis/summarize_logs.py` 生成。实验计划和结果记录流程见 `docs/performance_analysis.md` 和 `docs/performance_results.md`。

## 快速开始

### Docker Compose

启动 Flask 应用和 MySQL 数据库：

```bash
docker compose up --build
```

打开应用：

```text
http://localhost:5000
```

演示账号：

| 角色 | 用户名 | 密码 |
| --- | --- | --- |
| 管理员 | `admin_demo` | `DemoPass123` |
| 用户 | `food_creator` | `DemoPass123` |
| 用户 | `tech_creator` | `DemoPass123` |

MySQL 容器按以下顺序初始化数据库：

1. `database/schema.sql`
2. `database/indexes.sql`
3. `database/procedures.sql`
4. `database/seed.sql`

如需重置 Docker 数据卷并重新初始化：

```bash
docker compose down -v
docker compose up --build
```

### 手动部署

安装依赖：

```bash
pip install -r requirements.txt
```

创建环境变量。在 Windows PowerShell 中：

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="short_video_platform"
$env:DB_POOL_SIZE="5"
$env:SECRET_KEY="change-me"
```

可参考 `.env.example` 获取本地配置所需值。

初始化 MySQL：

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/indexes.sql
mysql -u root -p < database/procedures.sql
mysql -u root -p < database/seed.sql
```

如果你是在添加基于角色的访问控制之前创建的本地数据库，请运行：

```bash
mysql -u root -p < database/migrations/001_add_user_roles.sql
```

演示种子用户的密码为 `DemoPass123`。在真实部署前请修改或移除这些用户。

运行 Web 应用：

```bash
python backend/app.py
```

运行混合压测：

```bash
python experiments/run_parallel.py --threads 8 --batch-size 500 --duration 300 --author-id 33333333-3333-3333-3333-333333333333
```

汇总压测日志：

```bash
python experiments/analysis/summarize_logs.py experiments/logs/query_no_index.csv experiments/logs/query_with_index.csv
```

运行测试：

```bash
python -m unittest discover -s tests
```

预期测试结果：

```text
Ran 8 tests
OK
```

## 安全说明

- 请勿提交 `.env` 文件或真实数据库备份。
- 部署前设置强 `SECRET_KEY`。
- 数据库凭证仅通过环境变量存储。
- 管理员权限通过 `users.role` 字段校验，而非用户名约定。
- 在真实环境中使用种子账号前，请替换演示种子密码。

[en]: README.md
