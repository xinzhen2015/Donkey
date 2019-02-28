<p align="center">
<a href="https://travis-ci.org/onevcat/FengNiao"><img src="https://img.shields.io/travis/onevcat/FengNiao/master.svg"></a>
<a href="https://swift.org/package-manager/"><img src="https://img.shields.io/badge/SPM-ready-orange.svg"></a>
<a href="https://raw.githubusercontent.com/onevcat/Kingfisher/master/LICENSE"><img src="https://img.shields.io/cocoapods/l/Kingfisher.svg?style=flat"></a>
<a href="https://swift.org/package-manager/"><img src="https://img.shields.io/badge/platform-macos%20|%20Linux-blue.svg"/></a>
<a href="https://codecov.io/gh/onevcat/Hedwig"><img src="https://codecov.io/gh/onevcat/Hedwig/branch/master/graph/badge.svg"/></a>
</p>

# Donkey
iOS端轻量级、类Monkey工具：Donkey 🌹

***
## 基于Appium、pytest，所谓成也Appium，败也Appium。
```
优点：  

①基于appium，实现方便。  

②结合pytest，轻松实现多机并发。  

③屏蔽状态栏不可点击区域（尤其针对iphone刘海屏优化）。

缺点：

①基于appium，速度上略逊于Monkey。
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
pip3 install pytest-parallel  （用于并发：--workers auto --tests-per-worker auto）

pip3 install pytest-html  （用于生成报告：--html=report.html）

pip3 install pytest-rerunfailures  （用于用例失败重试：--reruns 3 --reruns-delay 1）
```

## 在终端中执行

```
pytest Donkey.py --workers auto --tests-per-worker auto --reruns 3 --reruns-delay 1 --html=report.html
```

## Donkey模块讲解

#### 并发配置
```python
@pytest.mark.parametrize("device_name, udid, wdalocal_port, appium",
                         [
                             ("测试机iPhone X", "a1bef8664467b9146b9bc7b511049d951dcce327", 5680, '4766'),

                             ("测试机iPhone6S", "4a7fe6672c148956640cfdaff70da48e49f6945c", 5682, '4777'),

                             ("测试机iPhone5s", "ed50fe2a082cd8ea8d1ee7bb11ccc017250da180", 5680, '4777'),


                         ])

```
```
注： 

wdalocal_port 需要设置不同的端口，appium 在一个端口上，也可在不同的端口上。
```

#### 其他模块可查看Donkey.py 中的注释，非常详细，修改上面配置后可直接使用。
```
有不明白的地方，欢迎留言，欢迎star~
```
