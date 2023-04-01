## 目录结构说明
~~~
├── README.md README.md         README.md文件
├── requirements.txt            依赖包文件
├── run.py                      flask项目管理文件 与项目进行交互的命令行工具集的入口
└── wx                          app目录
    ├── __init__.py             python项目必带  模块化思想
    ├── dao.py                  数据库访问模块
    ├── model.py                数据库对应的模型
    ├── response.py             响应结构构造
    ├── templates               模版目录,包含主页index.html文件
    └── views.py                执行响应的代码所在模块  代码逻辑处理主要地点  项目大部分代码在此编写
~~~
## 服务 API 文档
#### 调用示例
### `POST /api/count`
#### 请求参数
##### 请求参数示例
#### 响应结果
##### 响应结果示例
#### 使用注意
## License

[MIT](./LICENSE)
