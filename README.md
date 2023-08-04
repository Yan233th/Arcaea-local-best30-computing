# Arcaea-Local-Best30-Computing

一个本地ArcaeaBest30计算器, 无论你是苹果或是安卓, 只要你能够拿到Arcaea软件数据目录下的st3文件, 那么就可以计算

### 请注意计算出的Best30是根据你本地成绩计算的, 若有成绩未成功上传的也会计入

不过我没有苹果设备, 只知道越狱可以拿到, 其他的不知道
安卓的话最方便的是有root权限, 直接去读"/data/datamoe.low.arc/files/st3"就行, 理论上带root的模拟器也可以, 没有的话adb好像也有办法读取软件数据

#### 保证你的电脑上有python环境, 然后运行"run.bat"选择st3文件就可以了, 如果有报错或是曲目有缺漏的话可以去运行一下"update_data.bat"进行歌曲数据库更新, 如果更新了还是有问题就是github上的数据库没更新

使用的数据库是Arcaea-Infinity/ArcaeaSongDatabase项目中的arcsong.db, 在此特别感谢!