# AIS-140

中文 | [English](./README.md)

## 简介

AIS-140，全称 AUTOMOTIVE INDUSTRY STANDARD，汽车行业标准，是印度制定的一套针对车载卫星定位系统的通信协议。该协议主要用于道路车辆的卫星定位设备与后台监控中心之间的数据通讯，支持车辆定位、跟踪、应急救援等功能。它由印度汽车工业标准委员会 (AISC) 制定，印度汽车研究协会（ARAI）发布，是印度智能交通系统（ITS）的重要组成部分。

本项目基于 QuecPython 语言开发。

目前支持的版本为 AIS-140 (2016)。

该库的目的是提供构建车辆位置跟踪和紧急按钮的构建块。 **该库不提供完整的解决方案，因为任何实现都是特定于其预期用途的**。该库中的文档提供了有关如何最好地构建完整解决方案的指导。

## 用法

- [API 参考手册](./docs/zh/API参考手册.md)
- [用户使用手册](./docs/zh/用户使用手册.md)
- [客户端示例代码](./demo/ais_client_demo.py)
- [服务端示例代码](./demo/ais_server_demo.py)

## 贡献

我们欢迎对本项目的改进做出贡献！请按照以下步骤进行贡献：

1. Fork 此仓库。
2. 创建一个新分支（`git checkout -b feature/your-feature`）。
3. 提交您的更改（`git commit -m 'Add your feature'`）。
4. 推送到分支（`git push origin feature/your-feature`）。
5. 打开一个 Pull Request。

## 许可证

本项目使用 Apache 许可证。详细信息请参阅 [LICENSE](./LICENSE) 文件。

## 支持

如果您有任何问题或需要支持，请参阅 [QuecPython 文档](https://python.quectel.com/doc) 或在本仓库中打开一个 issue。
