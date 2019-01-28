# Donkey
iOS端轻量化、类Monkey工具：Donkey 🌹

***
## 基于Appium、pytest，所谓成也Appium，败也Appium。
```
优点：  

①基于appium，实现方便。  
②结合pytest，轻松实现多机并发。  
③屏蔽状态栏不可点击区域（尤其针对iphone刘海屏优化）。

缺点：

①基于appium，速度上不如略逊于Monkey。
```
***

## 环境配置

1、Appium安装。  
```
（此处可参照【官网：http://appium.io】方法）  
```
2、pytest安装  
```python
pip3 install pytest
```
3、pytest插件安装
```
pip3 install pytest-parallel  

pip3 install pytest-html  

pip3 install pytest-rerunfailures
```
