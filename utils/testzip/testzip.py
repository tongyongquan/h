#coding=UTF-8
#使用字典暴力破解zip文件密码
import zipfile
import threading
import optparse  #指数剖析

def extractFile(zFile,password):
	try:
		zFile.extractall(pwd=password)
		print('Found Passwd:',password)
		return password
	except:
		pass

def main():

	parser = optparse.OptionParser('usage%Prog '+ '-f <zipfile> -d <dictionary>' )
	parser.add_option('-f',dest='zname',action='store',type='string',help='specfy zip file')
	parser.add_option('-d',dest='dname',type='string',help='specfy dicttionary file')
	(options,args) = parser.parse_args()#把操作还有参数以元组的形式贮存
	if (options.zname == None) | (options.dname == None):   #注意这里()先判断再|
		print(parser.usage)
	else:
		zname = options.zname
		dname = options.dname
		zFile = zipfile.ZipFile(zname)
		dFile = open(dname, 'r')
		for line in dFile.readlines():
			password = line.strip('\n')
			t = threading.Thread(target=extractFile, args=(zFile, password))
			t.start()

"""
	zFile =zipfile.ZipFile('unzip.zip')
	passFile=open('dictionary.txt')
	for line in passFile.readlines():
		password=line.strip('\n')
		t=threading.Thread(target=extractFile,args=(zFile,password))
		t.start()
"""

if __name__=='__main__':
	main()



# zip -rP abc#123 test.zip test.txt


"""
Linux下如何使用zip压缩、解压和加密


一般linux下都默认安装了zip解压缩，通常格式如下（包含详细的参数中文解释）：

# zip -rP abc#123 test.zip test.txt

-P abc#123 是加密密码,注意大写P

-r 递归，将指定目录下的所有文件和子目录一并处理
test.zip 是生成的压缩文件
test.txt 是被压缩的文件

zip [参数] <压缩包> <源文件>

使用zip格式打包文件
-r 递归，将指定目录下的所有文件和子目录一并处理
-S 包含系统和隐藏文件
-y 直接保存符号连接，而非该连接所指向的文件
-X 不保存额外的文件属性
-m 将文件压缩并加入压缩文件后，删除源文件
-<压缩级别> 1~9，数字越大，压缩率越高
-F 尝试修复已损坏的压缩文件
-T 检查备份文件内的每个文件是否正确无误
-q 不显示指令执行过程
-g 将文件压缩后附加在既有的压缩文件之后，而非另行建立新的压缩文件
-u 更新压缩包内文件
-f 更新压缩包内文件。如果符合条件的文件没有包含在压缩包中，则压缩后添加
-$ 保存第一个被压缩文件所在磁盘的卷标
-j 只保存文件名称及其内容
-D 压缩文件内不建立目录名称
-i <表达式> 压缩目录时，只压缩符合条件的文件
-x <表达式> 排除符合条件的文件
-n <文件名后缀> 排除指定文件名后缀的文件
-b <缓存路径> 指定临时文件目录
-d <表达式> 从压缩文件内删除指定的文件
-t <日期时间> 把压缩文件的日期设成指定的日期
-o 以压缩文件内拥有最新更改时间的文件为准，将压缩文件的更改时间设成和该文件相同
-A 调整可执行的自动解压缩文件
-c 替每个被压缩的文件加上注释
-z 替压缩文件加上注释
-k 使用MS-DOS兼容格式的文件名称。
-l 压缩文件时，把LF字符置换成LF+CR字符。
-ll 压缩文件时，把LF+CR字符置换成LF字符。

unzip [参数] <压缩文件> [压缩包中将被释放的文件]

解压zip压缩包文件
-P <密码> zip压缩包的密码
-d <路径> 指定解压路径
-n 解压缩时不覆盖原有文件
-f 覆盖原有文件
-o 不经询问，直接覆盖原有文件
-u 覆盖原有文件，并将压缩文件中的其他文件解压缩到目录中
-l 显示压缩文件内所包含的文件
-t 检查压缩文件是否正确理里排除压缩包中的指定文
-z 显示压缩包注释
-Z unzip -Z等于执行zipinfo指令
-j 不处理压缩文件中原有的目录路径
-C 压缩文件中的文件名称区分大小写
-L 将压缩文件中的全部文件名改为小写
-s 将文件名中的空格转换下划线
-X 解压缩时保留文件原来的UID/GID
-q 执行时不显示任何信息
-v 执行是时显示详细的信息
-c 将解压缩的结果显示到屏幕上，并对字符做适当的转换
-p 与-c参数类似，会将解压缩的结果显示到屏幕上，但不会执行任何的转换
-a 对文本文件进行必要的字符转换
-b 不要对文本文件进行字符转换
-x <表达式> 处理里排除压缩包中的指定文件
-M 将输出结果送到more程序处理

附录：

Linux常用打包解包方法

1、打包/压缩
zip filename.zip filename
tar cvf filename.tar filename
gtar zcvf filename.tar.gz filename
gzip filename 将产生文件 filename.gz
2、解包
unzip filename.zip
tar xvf filename.tar
gtar zxvf filename.tar.gz
gzip -d filename.gz
"""
