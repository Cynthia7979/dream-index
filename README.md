# Dream Index
记梦、分享梦、和从梦中找到灵感的平台。

## 环境
查看`requirements.txt`，或使用`pip install -r requirements.txt`全部安装

## 目录结构
`Documents/` 项目相关原型及流程图文件  
&nbsp;&nbsp;&nbsp;&nbsp;└ \*

`src/`    
&nbsp;&nbsp;&nbsp;&nbsp;└ `run.bat` 快捷本地部署  
&nbsp;&nbsp;&nbsp;&nbsp;└ `setup.py` 本地包调试文件（用于文件之间互相引用）  
&nbsp;&nbsp;&nbsp;&nbsp;└ `dreamindex/` 网站代码  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ `__init__.py` 主代码，包括路由、前端相关的信息抓取等  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ `database/` 数据库（`*.db`)文件目录  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ `static/` 静态文件目录，如CSS、图片等  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ `templates/` 模板文件目录  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ `dev/` 开发用工具  

## 运行
运行`src`目录下的`run.bat`.

**请注意：**
1. 不要使用PyCharm插件运行
2. 如果使用了虚拟环境，请激活Dream Index对应的环境后，再从同一命令行运行
3. 如果嫌麻烦可以直接手打

CMD，在`src`目录下：
```batch
set FLASK_APP=src/dreamindex
set FLASK_ENV=development
pip install -e .
python -m flask run
```

Bash，在`src`目录下：
```shell script
export FLASK_APP=src/dreamindex
export FLASK_ENV=development
pip install -e .
python -m flask run
```

## 外部链接
* 调研结果和计划：[在线思维导图](https://docs.qq.com/mind/DRXJuaFphZG5qeWpT)
* Flask简化版教程及第三方库笔记：[Cynthia7979/flask-test](https://github.com/Cynthia7979/flask-test)
* Flask官方文档：[Flask Documentation 2.0.x](http://flask.pocoo.org)
* Jinja官方文档：[Jinja Documentation 2.0.x](https://jinja.palletsprojects.com/en/3.0.x/)