# 开发了一款视频播放器 Medianex,目前正式开启公测，通过插件化的设计可以支持接入任意云盘，支持自动生成海报墙，支持 Linux 、Windows、Macos，希望您可以喜欢 - V2EX

**原始链接**: https://www.v2ex.com/t/1131533
**提取时间**: 2025-07-28 10:24:03

---

### APP 截图

![](https://file.medianex.app/screenshot/1.png) ![](https://file.medianex.app/screenshot/4.png) ![](https://file.medianex.app/screenshot/5.png) ![](https://file.medianex.app/screenshot/6.png) ![](https://file.medianex.app/screenshot/7.png) ![](https://file.medianex.app/screenshot/8.png)

> V2EX 的 markdown 怎么不支持折叠的语法...

### 下载地址

> 目前 macos 还没有进行签名，会提示恶意软件，需要多次确认才可以打开

[![Static Badge](https://img.shields.io/badge/Macos_arm64_dmg-v0.0.4_beta-blue?style=flat&logo=macos)](https://file.medianex.app/release/0.0.4-beta/medianex-0.0.4-beta-macos_arm64.dmg)

[![Static Badge](https://img.shields.io/badge/Macos_x86_64_dmg-v0.0.4_beta-blue?style=flat&logo=macos)](https://file.medianex.app/release/0.0.4-beta/medianex-0.0.4-beta-macos_x86_64.dmg)

[![Static Badge](https://img.shields.io/badge/Windows_x86_64_exe-v0.0.4_beta-blue?style=flat)](https://file.medianex.app/release/0.0.4-beta/medianex-0.0.4-beta-windows-setup_x86_64.exe)

[![Static Badge](https://img.shields.io/badge/Debian_x86_64_deb-v0.0.4_beta-blue?style=flat&logo=debian)](https://file.medianex.app/release/0.0.4-beta/medianex-0.0.4-beta-linux_x86_64.deb)

[![Static Badge](https://img.shields.io/badge/ArchLinux_x86_64_zst-v0.0.4_beta-blue?style=flat&logo=archlinux)](https://file.medianex.app/release/0.0.4-beta/medianex-0.0.4-beta-linux-x86_64.pkg.tar.zst)

#### 目前支持的插件

目前支持阿里云盘、百度网盘、夸克、115 盘、Webdav 、Sftp 、Ftp 等  
插件仓库[Plugins](https://github.com/medianexapp/plugins)  
插件基于 Webassembly 开发,[wazero_net](https://github.com/labulakalia/wazero_net)提供了在 Wasm 里进行网络请求的功能

#### 如何开发自已的插件

use [plugin_api](https://github.com/medianexapp/plugin_api)

如何你有什么建议或者想法可以在这里提交  
[Discussions](https://github.com/orgs/medianexapp/discussions/new)
