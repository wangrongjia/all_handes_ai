# 使用 FFmpeg 和 GPU 实现最简“图片+无损音频=视频”的方法 - V2EX

**原始链接**: [https://www.v2ex.com/t/1121476#reply13](https://www.v2ex.com/t/1121476#reply13)  
**来源网站**: www.v2ex.com  
**提取时间**: 2025-07-29 01:18:08

---

> 需求：搜集到的无损音乐太占空间，决定传到 B 站~~网盘~~ 。但 pr 导出太太太耗时，于是使用 FFmepeg 的 GPU 加速 

前置条件清单  
1.支持 NVENC 的 NVIDIA 显卡 确认是否支持 NVENC： 在 CMD 中执行：
[code] 
    nvidia-smi
    
[/code]

或通过 [NVIDIA 官方列表](<https://developer.nvidia.com/video-encode-decode-gpu-support-matrix>) 查询您的显卡型号。  
2.更新到最新 NVIDIA 显卡驱动   
3.支持 `h264_nvenc` 的 FFmpeg 版本   

  * [FFmpeg 官网](<https://www.gyan.dev/ffmpeg/builds/>)
  * 检查 FFmpeg 是否支持 `h264_nvenc`：

  * I think 1969 was second best.


[code] 
    ffmpeg -encoders | findstr "h264_nvenc"
    
[/code]

如果输出中有 `h264_nvenc`，则支持。  

* * *


开始：  
1.将 FFmpeg 的 bin 目录加入环境变量  
2.输入  

[code] 
    ffmpeg -hwaccel cuda -threads 24 -loop 1 -i "picture.png" -i "music.flac" -vf "hwupload" -c:v h264_nvenc -preset 0 -cq 23 -rc constqp -c:a flac -shortest "output.mkv"
    
[/code]

解析：  

  * `ffmpeg`：开源命令行工具
  * `-hwaccel cuda`：启用 CUDA 硬件加速，利用 NVIDIA 显卡的 CUDA 核心来加速视频处理，从而提高处理效率。
  * `-threads 24`：设置处理时使用的线程数为 24 个，多线程加快处理速度，根据电脑配置增减。
  * `-loop 1`：使输入的图像循环播放，这里设置循环次数为 1 次，让图像持续显示。
  * `-i "picture.png"`：指定输入文件为名为`picture.png`的图像文件。
  * `-i "music.flac"`：指定输入文件为名为`music.flac`的音频文件。
  * `-vf "hwupload"`：视频滤镜，将输入视频数据上传到硬件设备（这里与前面的硬件加速相关），以便后续在硬件上进行处理。
  * `-c:v h264_nvenc`：指定视频编码格式为 H.264 ，并使用 NVIDIA NVENC 编码器进行编码，利用 NVIDIA 显卡的编码能力来生成视频流。
  * `-preset 0`：设置编码预设，0 是最快但视频质量最差，可以按需提高。
  * `-cq 23`：设置恒定质量因子为 23 。恒定质量因子模式下，编码器会尝试保持输出视频质量恒定，通过调整码率来适应不同的场景复杂度。较低的 CQ 值通常意味着更高的质量，但可能产生更大的文件。
  * `-rc constqp`：指定使用恒定 QP （量化参数）模式进行编码，与`-cq`类似，用于控制视频质量。
  * `-c:a flac`：指定音频编码格式为 FLAC ，保持音频的原始编码格式不变
  * `-shortest`：使输出视频的时长与输入中最短的流的时长相同，即当音频和视频时长不同时，以最短的时长为准来生成输出视频，确保音频和视频同步结束。
  * `"output.mkv"`：指定输出文件名为`output.mkv`，然后发到 B 站网盘就行了。

* * *


批量处理：  
视频按顺序数字重命名（如 `video1.mp4`, `video2.mp4` 等），且需要与对应的图片（如 `pic1.png`, `pic2.png`）

1.每个视频关联一张图片
[code] 
    @echo off
    set "input_dir=.\videos"       # 视频存放目录（如已重命名的 video1.mp4 ）
    set "image_dir=.\images"       # 图片存放目录（需要同名的 pic1.png 等）
    set "output_dir=.\outputs"     # 输出目录
    
    for %%a in ("%input_dir%\*.mp4") do (
        set "video_file=%%~nxa"
        set "prefix=%%~na"
        ffmpeg -hwaccel cuda -threads 24 -i "%%a" -i "%image_dir%\pic%%~na.png" ^  # 注意：这里的图片名格式可自定义（如 pic1.png 需替换为 pic##匹配你的命名）
        -filter_complex "[0:v]scale=trunc(iw/2)*2:trunc(ih/2)*2[vid]; [vid][1:v] overlay=10:10" ^  # 图片叠加在左上角（ 10 像素偏移）
        -c:v h264_nvenc -preset 0 -cq 23 -rc constqp ^ 
        -c:a copy ^  # 音频直接复制（加速处理）
        "%output_dir%\output_%%~na.mkv"
    )
    
[/code]

2.所有视频使用同一张背景图片
[code] 
    @echo off
    set "input_dir=.\videos"       # 视频目录
    set "image_file=.\background.png"  # 固定背景图片路径
    set "output_dir=.\outputs"
    
    for %%a in ("%input_dir%\*.mp4") do (
        ffmpeg -hwaccel cuda -threads 24 -i "%%a" -loop 1 -i "%image_file%" ^  # 循环播放图片
        -filter_complex "[0:v]scale=trunc(iw/2)*2:trunc(ih/2)*2[vid]; [1:v]scale=trunc(iw/2)*2:trunc(ih/2)*2[img]; [vid][img] overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2" ^  # 图片居中叠加
        -c:v h264_nvenc -preset 0 -cq 23 -rc constqp ^ 
        -c:a copy 
        "%output_dir%\output_%%~na.mkv"
    )
    
[/code]

3.注意事项

  * 确保所有视频/图片格式被 FFmpeg 支持(jpg 格式图片需要额外命令转换)
  * 若视频名包含空格/符号，需用引号包裹路径：
  * 批处理脚本默认顺序执行，可通过多线程化进程（如 GNU Parallel ）提速~~电脑包扛不住吧~~  

4.效果示例

[code] 
    # 输入视频目录：
    videos/
    ├── video1.mp4
    ├── video2.mp4
    └── video3.mp4
    
    # 输入图片目录（场景 1 ）：
    images/
    ├── pic1.png
    ├── pic2.png
    └── pic3.png
    
    # 输出目录：
    outputs/
    ├── output_video1.mkv
    ├── output_video2.mkv
    └── output_video3.mkv
    
[/code]

5.自动化

#### **(1) 保存为批处理文件（ Windows ）**
[code] 
    # 保存为 batch_process.bat ，双击运行即可。
    
[/code]

#### **(2) 可视化进度条（可选）**
[code] 
    echo Processing videos: 
    FOR /L %i IN (1,1,50) DO (
        echo %i%%
        ping localhost -n 1 >nul
    )
    
[/code]

然后可以**快速完成批量视频与图片的合成处理** ,传到 B 站~~网盘~~ 。如需进一步定制（如动态图片透明度、图片/视频尺寸调整、不同叠加效果、音轨混音等）自行添加命令  
使用开源的 B 站音频播放器[电梓播放器](<https://github.com/kenmingwang/azusa-player>)  
然后完美音乐软件 get☆ daze
