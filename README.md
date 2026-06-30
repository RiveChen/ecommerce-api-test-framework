# ecommerce-api-test-framework

基于 **pytest + requests + Allure** 搭建的接口自动化测试框架，覆盖 DummyJSON 电商 API 的 Auth / Products / Users 三个模块，支持 YAML 数据驱动，接入 GitHub Actions CI，测试报告自动发布至 GitHub Pages。

-> **[在线 Allure 报告](https://RiveChen.github.io/ecommerce-api-test-framework)** <-

---

## 技术栈

| 用途      | 工具                                  |
| --------- | ------------------------------------- |
| 包管理    | [uv](https://github.com/astral-sh/uv) |
| 测试框架  | pytest 9.x                            |
| HTTP 请求 | requests                              |
| 报告生成  | allure-pytest                         |
| 数据驱动  | PyYAML                                |
| 断言增强  | jsonschema                            |
| CI/CD     | GitHub Actions                        |
| 报告托管  | GitHub Pages                          |

---

## 快速开始

```bash
git clone https://github.com/RiveChen/ecommerce-api-test-framework.git
cd ecommerce-api-test-framework
uv sync
```

**运行测试：**

```bash
uv run pytest                          # 运行全部用例
uv run pytest tests/test_auth/         # 运行单模块
uv run pytest -m smoke                 # 冒烟用例
uv run pytest -m "not slow"            # 排除慢速用例
uv run pytest -v --tb=short            # 详细输出 + 精简错误堆栈
```

**本地查看 Allure 报告：**

```bash
uv run pytest --alluredir=allure-results
allure serve allure-results            # 自动在浏览器打开报告
```

---

## 测试覆盖

| 模块     | 文件              | 用例数 | 覆盖场景                               |
| -------- | ----------------- | ------ | -------------------------------------- |
| Auth     | `test_login.py`   | 5      | 登录成功、错误密码、空字段、token 刷新 |
| Products | `test_query.py`   | 7      | 列表、分页、搜索、单条查询、ID 不存在  |
| Products | `test_crud.py`    | 5      | 新增、更新（PUT/PATCH）、删除          |
| Users    | `test_profile.py` | 6      | 个人信息查询、购物车查询、越权访问     |
| **合计** |                   | **23** |                                        |

---

## 框架设计

### **分层结构**

```txt
请求层（BaseClient）→ API 模块层（auth/product/user_api）→ 测试层（test_*）
```

测试用例不直接调用 `requests`，通过 API 模块类发起请求。当接口 URL 或签名变更时，只需修改对应的 API 模块文件，测试逻辑不受影响，降低维护成本。

### **YAML 数据驱动**

测试数据与测试逻辑分离。`data/product_cases.yaml` 中每条用例包含 `id`、`description`、`input`、`expected` 四个字段，通过 `pytest.mark.parametrize` 加载。新增测试场景只需编辑 YAML 文件，无需改动测试代码。

### **Session 级别的 JWT Fixture**

根层 `conftest.py` 中的 token fixture 使用 `scope="session"`，整次测试运行只触发一次登录请求，token 在 Products 和 Users 模块间共享，减少无效网络开销，也避免因频繁登录触发限流。

### **Allure 三级标签体系**

```txt
Epic:    DummyJSON API
  └── Feature:  Products 模块
        └── Story:    查询商品详情
              └── Step: 发送请求 → 断言状态码 → 断言响应字段
```

报告中可按模块、场景、严重等级多维度筛选用例，失败用例的请求体和响应体作为 attachment 自动附加，便于定位问题。

---

## CI/CD

每次向 `main` 推送代码或发起 Pull Request，GitHub Actions 自动执行以下流程：

1. 安装 Python 3.11 + uv
2. 执行 `uv sync` 还原依赖
3. 运行 `uv run pytest --alluredir=allure-results`
4. 生成 Allure HTML 报告并部署至 GitHub Pages

在线报告地址：`https://RiveChen.github.io/ecommerce-api-test-framework`

---

## 添加新用例

1. 在 `data/<module>_cases.yaml` 追加测试数据条目
2. 如涉及新接口，在 `utils/api/<module>_api.py` 增加对应方法
3. 运行 `uv run pytest tests/test_<module>/ -v` 本地验证通过后提交

---

## License

MIT
