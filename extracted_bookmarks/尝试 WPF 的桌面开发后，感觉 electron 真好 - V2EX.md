# 尝试 WPF 的桌面开发后，感觉 electron 真好 - V2EX

**原始链接**: https://www.v2ex.com/t/1145558#reply3
**提取时间**: 2025-07-28 10:27:56

---

之前没有学过 .NET ，所有内容都是现学的，需要给老项目做后续的开发和优化，项目是基于 .NET Framework 的 WPF 应用，在一个页面中需要绘制大量的 Path 。

项目是在 Canvas 的组件中直接挂载 Path ，在挂载组件的时候，系统非常卡，在计算完所有的 Path 后，需要 8 秒左右才能完全显示出来。

优化为仅绘制可视区域，虽然初次加载变快了，但是滚动条拖动重新渲染还是很卡，并且初次渲染也要花 2s 左右

[后面又对.NET](http://后面又对.NET) 升级，拉到了.NET8 但是提升效果几乎没有

也又考虑过利用 Bitmap 去做优化，但是原来的 Path 上面绑定了一堆事件，改起来非常麻烦

于是就利用了几个技术栈对绘制做了测试：

  * WPF .NET8: 按照微软官方的[优化推荐](https://learn.microsoft.com/zh-cn/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging)，，利用 StreanGeome 去绘制可视区域内的 Path ，但是每当计算完毕提交 Path 到 Canvas 的时候，还是会卡顿（视图更新慢）

  * avaloniaui：和 WPF 表现差不多，甚至在某些情况下会比 WPF 卡一点点

  * electron: ；利用 React+Vite ，使用 d3.js 在 SVG 下绘制 path ，绘制全部（可视区域/非可视区域），初次计算和渲染一起大概不到 3s ，虽然计算的时间可能比不过 C#，但是绘制出来后，滚动条滑动还是流畅的




除此之外，Electron 节省了大量的学习和研发成本，刚刚接触 .NET 的时候真的头疼，每次优化的时候都在想，用 electron 能快速解决的事情，在 WPF 里是完全的蒙圈。网上浏览了一圈，很多关于 WPF 渲染性能的问题

体积大点就大点，不用费劲心思去做渲染优化是真的爽
