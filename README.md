
==============================================================================
 change.py 是“命令行脚本”，以后转换图片时需要在终端输入命令。
不需要修改代码,只需要更换命令末尾的 SVG 文件名。
==============================================================================
1. 把需要转换的 SVG 文件放进：D:\switch-ion

2. 打开 D:\switch-ion 文件夹。

3. 在文件夹空白处右键，选择“在终端中打开”。

4. 在终端中输入：uv run --python 3.12 --with pillow --with resvg-py .\change.py .\logo.svg

5. 按回车，看到：转换成功：D:\switch-ion\logo.ico

这时文件夹中就会出现：logo.svg  logo.ico
================================================================================
以后转换其他文件，只需要替换命令最后的文件名。例如转换 new_icon.svg：
uv run --python 3.12 --with pillow --with resvg-py .\change.py .\new_icon.svg

规律就是：
命令前面保持不变                         这里换成你的文件名
uv run ... .\change.py                  .\new_icon.svg

如果文件名带空格，需要加引号：
uv run --python 3.12 --with pillow --with resvg-py .\change.py ".\my icon.svg"
