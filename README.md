# h
第一步：创建xxx项目
scrapy startproject ***

第二步：创建要抓取的名称及抓取网址
scrapy genspider *** 'https://hr.tencent.com/position.php'

第三步：编写items.py，明确需要提取的数据

第四步：编写spiders/xxx.py 编写爬虫文件，处理请求和响应，以及提取数据（yeild item）

第五步：编写pipelines.py管道文件，处理spider返回item数据

第六步：编写settings.py，启动管理文件，以及其他相关设置
ITEM_PIPELINES = {
    'cententjob.pipelines.CententjobPipeline': 300,
}
第七步：执行爬虫
scrapy crawl ***

###[python whl库，windows安装必备！！！](https://www.lfd.uci.edu/~gohlke/pythonlibs/)


###虚拟环境安装依赖：
source /root/venv_spider/bin/activate
pip3.6 install xxx

###运行爬虫：
/root/venv_spider/bin/python3.6 run.py ""spidername""

###部署定时任务：
1. h_airflow/dags下面添加dags文件
2. 服务器上cp h/dags/* ~/h/dags
3. 5分钟后刷新airflow后台 http://127.0.0.1:8080/admin/ 打开开关，手动执行dag命令，看看是否正常