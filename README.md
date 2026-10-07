# 目录结构

```text
DATAPROJECT_RockBurst/
├── data/                             # 数据
│   ├── ads/                           # 结果数据
│   |   ├── ......                      # 模型结果
│   |   └── report                      # 报告
│   ├── dwd/                           # 模型输入数据
│   └── ods/                           # 原始数据、中间数据
│       ├── csv           
│       ├── json          
│       └── pdf           
├── scripts/                          # 自动化集成
│   ├── dataget.py                     # ETL
│   ├── run.py                         # 完整管道
│   └── train_pre.py                   # 模型训练预测    
├── src/                              # 源代码目录
│   ├── agent/                         # AI相关
│   │   └── Prompt.txt   
│   ├── model/                         # 模型相关代码    
│   |   ├── add_datapreprocessor.py     # 自定义符合 auto-sklearn 框架的数据处理管道
│   |   ├── auto_classifier.py          # 基于 auto-sklearn 框架搭建模型，并进行训练预测
│   |   ├── nweleaderboard.py           # auto-sklearn 源码 leaderboard 函数存在 bug，继承原函数修正问题
│   |   ├── see_pipelinecomponents.py   # 显示框架内置管道
│   |   └── F14_pre.py                  # 使用训练好的模型
│   └── processor/                     # ETL 代码
│       ├── pdf2_useMinerU.py           # 调用 MinerU 文档解析功能，将论文 pdf 解析为 Json 数据
│       ├── MinerU2tablejson.py         # 从包含文本、表格、公式及布局信息的论文 Json 中提取表格数据
│       ├── table2_useZHIPU.py          # 调用 glm-4.6v，结合 Prompt 从表格 Json 提取岩爆数据，并输出结构化 Json
│       ├── ZHIPUjson2csv.py            # 将每个岩爆数据 json 存储为 csv，并按输入的期望列合并多个数据为最终的原始数据 merge.csv
│       └── data2mysql.py               # 将数据存储至MySQL
├── .env                              # API KEY、关键目录等配置信息，需新建
├── environment.yml                   # 项目环境信息   
└── README.md                         # 项目简介
```

# 配置信息

## 环境配置

- 操作系统：WSL2
- Linux 发行版：Ubuntu 24.04
- 环境管理：conda
- 环境配置文件：environment.yml

## 环境变量配置

在项目根目录下新建 .env，填入你的 API 密钥:

```ini
# 智谱 AI
ZHIPU_API_KEY=YourKey
ZHIPU_MODEL_NAME=glm-4.6v
ZHIPU_API_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions

MINERU_API_BASE=https://mineru.net/api/v4
MINERU_API_KEY=YourKey

# MySQL，账户可以用root，也可以专门新建一个
MySQL_USER=root
MySQL_PASSWORD=YourPassword

PDF_FOLDER=./data/ods/pdf
JSON_FILE=./data/ods/json/example.json
CSV_FILE=./data/ods/csv/example.csv
PROMPT_FILE=./src/agent/Prompt.txt
DATA=./data/dwd/input.csv
```

# 项目概述

本项目源于 2023 年下半年北山高放废物地质处置库开挖工程中的岩爆预测需求，当时没有实测工程数据，只做了理论模型，加上工程验证会更加完整。
[github.com/lamauamal/RockBurst.git](https://github.com/lamauamal/RockBurst.git)版本对原始流程进行了重构和优化，当前版本（[github.com/lamauamal/DataProject_RockBurst.git](https://github.com/lamauamal/DataProject_RockBurst.git)）贴合数据方向做了项目结构优化，并增加了与MySQL的交互。
