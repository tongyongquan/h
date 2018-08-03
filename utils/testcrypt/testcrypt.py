#coding=UTF-8

#破解linux密码

import crypt

def testPass(cryptPass):  #传入哈希密码
	print 'cryptPass ='+ cryptPass   #通过打印进行测试
	salt = cryptPass.strip(cryptPass.split('$')[-1])      #截取盐
	dictfile = open('dictionary.txt','r')  #打开字典文件
	for word in dictfile.readlines():
		word = word.strip('\n')
		cryptWord = crypt.crypt(word,salt)
		print 'cryptWord ='+cryptWord
		if cryptPass == cryptWord:
			print('Found passed:',word)
			return
		

def main():
	passfile=open('passwords.txt','r') #读取密码文件 cat /etc/shadow | grep root
	try:
		for line in passfile.readlines():
			user = line.split(':')[0]
			cryptPass = line.split(':')[1]
			print("Cracking Password For:",user)
			testPass(cryptPass)
	except:
		return
if __name__ == '__main__':

	main()




"""
 shadow文件中密码的加密方式

1) 查看shadow文件的内容

    cat /etc/shadow

    可以得到shadow文件的内容，限于篇幅，我们举例说明：

    root:$1$Bg1H/4mz$X89TqH7tpi9dX1B9j5YsF.:14838:0:99999:7:::

    其格式为：

    {用户名}：{加密后的口令密码}：{口令最后修改时间距原点(1970-1-1)的天数}：{口令最小修改间隔(防止修改口令，如果时限未到，将恢复至旧口令)：{口令最大修改间隔}：{口令失效前的警告天数}：{账户不活动天数}：{账号失效天数}：{保留}

    【注】：shadow文件为可读文件，普通用户没有读写权限，超级用户拥有读写权限。如果密码字符串为*，则表示系统用户不能被登入；如果字符串为！，则表示用户名被禁用；如果字符串为空，则表示没有密码。

    我们可以使用passwd –d 用户名 清空一个用户的口令密码。

2) 解析shadow文件中密码字符串的内容

    对于示例的密码域$1$Bg1H/4mz$X89TqH7tpi9dX1B9j5YsF.，我们参考了linux标准源文件passwd.c，在其中的pw_encrypt函数中找到了加密方法。

    我们发现所谓的加密算法，其实就是用明文密码和一个叫salt的东西通过函数crypt()完成加密。

    而所谓的密码域密文也是由三部分组成的，即：$id$salt$encrypted。

    【注】： id为1时，采用md5进行加密；

    id为5时，采用SHA256进行加密；

    id为6时，采用SHA512进行加密。

3) 数据加密函数crypt()讲解

    i. 头文件：#define _XOPEN_SOURCE

    #include <unistd.h>

    ii. 函数原型：char *crypt(const char *key, const char *salt);

    iii. 函数说明：crypt()将使用DES演算法将参数key所指的字符串加以编码，key字符串长度仅取前8个字符，超过此长度的字符没有意义。参数salt为两个字符组成的字符串，由a-z、A-Z、0-9，’.’和’/’所组成，用来决定使用4096种不同内建表格的哪一种。函数执行成功后会返回指向编码过的字符串指针，参数key所指向的字符串不会有所改动。编码过的字符串长度为13个字符，前两个字符为参数salt代表的字符串。

    iv. 返回值：返回一个指向以NULL结尾的密码字符串

    v. 附加说明：使用GCC编译时需要加上 –lcrypt

4) 加密参数salt的由来

    在我们的示例密码域中salt为Bg1H/4mz，那么它又是如何来的？

    我们还是从标准源文件passwd.c中查找答案。在passwd.c中，我们找到了与salt相关的函数crypt_make_salt。

    在函数crypt_make_salt中出现了很多的判断条件来选择以何种方式加密(通过id值来判断)，但其中对我们最重要的一条语句是gensalt(salt_len)。

    我们继续查看了函数static char *gensalt (unsigned int salt_size)，才发现原来神秘无比的salt参数只是某个固定长度的随机字符串而已。

5) 最终结论

    在我们每次改写密码时，都会随机生成一个这样的salt。我们登录时输入的明文密码经过上述的演化后与shadow里的密码域进行字符串比较，以此来判断是否允许用户登录。

    【注】：经过上述的分析，我们发现破解linux下的口令也不是什么难事，但前提是你有机会拿到对方的shadow文件。

6) 示例代码(测试代码)：

    #include <pwd.h>
    #include <stddef.h>
    #include <string.h>
    #include <shadow.h>
    #include <stdio.h>
    #include <unistd.h>
    int main(int argc, char *argv[])

    {

        if(argc < 2)

        {

            printf("no usrname input");

            return 1;

        }

        if (geteuid() != 0)

        {

            fprintf(stderr, "must be setuid root");

            return -1;

        } 

        struct spwd *shd= getspnam(argv[1]);

        if(shd != NULL)

        {

            static char crypt_char[80];

            strcpy(crypt_char, shd->sp_pwdp);

            char salt[13];

            int i=0,j=0;

            while(shd->sp_pwdp[i]!='\0')

            {

                salt[i]=shd->sp_pwdp[i];

                if(salt[i]=='$')

                {

                    j++;

                    if(j==3)

                    {

                        salt[i+1]='\0';

                        break;

                    }

                }

                i++;

            }

            if(j<3)

            perror("file error or user cannot use.");

            if(argc==3)

            {

                printf("salt: %s, crypt: %s\n", salt, crypt(argv[2], salt));

                printf("shadowd passwd: %s\n", shd->sp_pwdp);

            }

        }

        return 0;

    }

    编译： gcc passwd.c -lcrypt -o passwd

    运行： ./passwd root 123

    结果： salt: $1$Bg1H/4mz$, crypt: $1$Bg1H/4mz$X89TqH7tpi9dX1B9j5YsF.

                shadowd passwd: $1$Bg1H/4mz$X89TqH7tpi9dX1B9j5YsF.

"""

