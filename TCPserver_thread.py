import socket
import  datetime
#多线程TCP服务器端
import socketserver
import pymssql
dtu_add_Low=0
dtu_add_High=0
def my_fun_send_OK(conn):
    my_str_short = [0x10, 0x80, 0x01, 0x00, 0x81, 0x16]
    my_str_short[2] = dtu_add_Low
    my_str_short[3] = dtu_add_High
    s2 = my_101_com_genert_CRC(my_str_short)
    s3 = bytes(s2)
    conn.sendall(s3)
    my_all_step = 3
    print("send   data:", end='')
    my_str_to_hex_display(s3)



def get_time_count():
    i=datetime.datetime.now()
    time_count=i.hour*3600+i.minute*60+i.second
    time_count2=time_count%65535
    y = time_count2 % 256
    x = time_count2 // 256
    return  int(x),int(y)
#########################3
def my_str_to_hex_display(s):
    #s2 = bytes(s, 'utf-8')
    if s==None:
        return
    print(datetime.datetime.now(),": ",end='')
    s2=s
    for i in s2:
        print(hex(i), end='')
        if i!=s2[-1]:
            print('-', end='')
    print()

#######################
def my_get_fram(s0):
    #s2=bytes(s0,'utf-8')
    s2=s0
    status=0
    for i in s2:
        if i==0x10:
            my_start=s2.index(i)
            status=0x10
        elif i==0x68:
            my_start=s2.index(i)
            status=0x68
        else:
            my_start=0
            status=0

        if status==0x10:
            x=s2[my_start+5]
            if x==0x16:
                s3=s2[my_start:my_start+6]

                break
        elif status==0x68:
            x=s2[my_start+3]
            if x==0x68:
                lenth=int(s2[my_start+1])
                s3=s2[my_start:my_start+lenth+6]

                break
        else:
            s3=None;

    #s = str(s3, encoding="utf-8")
    s=s3

    s = s2
    if s3!=None:
        #print("source data:", end='')
        #my_str_to_hex_display(s)
        print("get    data:",end='')
        my_str_to_hex_display(s)
    else:
        print("None get data")


    return s3
#19201012131415161718  1213101213141516171819
def my_101_com_genert_CRC(s0):
    if s0[0]==0x10:
        crc=s0[1]+s0[2]+s0[3]
        s0[4]=crc%256
        s0[5]=0x16
    else:
        my_lenth=s0[1]
        count=0
        for ii in range(0,my_lenth):
            count=count+s0[ii+4]
        crc=count%256
        ii=ii+1
        s0[ii+4]=crc
        s0[ii + 5] = 0X16
    s1=s0
    return  s1
######################SQL####
class MSSQL:
    def __init__(self,host,user,pwd,db): #类的构造函数，初始化数据库连接ip或者域名，以及用户名，密码，要连接的数据库名称
        self.host=host
        self.user=user
        self.pwd=pwd
        self.db=db
    def __GetConnect(self):  #得到数据库连接信息函数， 返回: conn.cursor()
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn=pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset='utf8')
        cur=self.conn.cursor()  #将数据库连接信息，赋值给cur。
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    #执行查询语句,返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
    def ExecQuery(self,sql):  #执行Sql语句函数，返回结果
        cur = self.__GetConnect()   #获得数据库连接信息
        cur.execute(sql)  #执行Sql语句
        resList = cur.fetchall()  #获得所有的查询结果

        #查询完毕后必须关闭连接
        self.conn.close()   #返回查询结果
        return resList
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

def my_fun_SQL_insertdata(sqlstr):
    #ms=MSSQL(host="120.27.48.70:3538",user="saw",pwd="ncist1525",db="DTU_SERVER")  #实例化类对象，连接数据对象
    ms = MSSQL(host="106.14.41.25:3539", user="sa", pwd="NcisT.DKyT_123456", db="ZSQ_TEST")  # 实例化类对象，连接数据对象[ZSQ_TEST]
    #sqlstr = "insert into TB_cycdata (status,timer,temperature) VALUES (10,11,12)"
    print(sqlstr)
    ms.ExecNonQuery(sqlstr)



################################333
#sk = socket.socket()
#sk.bind(("106.14.41.25",2216))
#sk.listen(5)
#conn,address = sk.accept()
#conn.sendall(bytes("Hello world",encoding="utf-8"))
#while True:
    #buf=conn.recv(1024)

my_all_step = 0
my_heart_time_count = 1
file_count = 0
class ZSQ:
    def __init__(self):
        self.duanlu= 0    # 短路
        self.jiedi= 0     # 接地
        self.A_all =0.0     #
        self.E_fild=0.0
        self.temperature=0.0
        self.Li_bat=0.0
        self.Sun_bat=0.0
        self.xian_V=0.0
        self.A_half=0.0
        self.Gan_bat=0.0
        self.timer=0
class DTU:
    def __init__(self):
        self.temperature= 0.0
        self.bat_v=0.0
        self.bat_sun=0.0
        self.shidu=0.0

class AC12T:
    def __init__(self):
        self.T1= 0.0
        self.T2=0.0
        self.T3=0.0
        self.T4=0.0
        self.T5 = 0.0
        self.T6 = 0.0
        self.T7= 0.0
        self.T8 = 0.0
        self.T9 = 0.0
        self.T10 = 0.0
        self.T11 = 0.0
        self.T12= 0.0


zsqA=ZSQ()
zsqB= ZSQ()
zsqC = ZSQ()
mydtu=DTU()
ac12tA=AC12T()
ac12tB = AC12T()
ac12tC = AC12T()
def my_fun_work(buf,conn):
    global  my_all_step
    global my_heart_time_count
    global  file_count
    global zsqA
    global zsqB
    global zsqC
    global mydtu
    global ac12tA
    global ac12tB
    global ac12tC
    mydtuadd=0
    my_get_com_bytes=my_get_fram(buf)

    if my_get_com_bytes==None:
        return

    if my_get_com_bytes[0]==0x10:
        dtu_add_Low = my_get_com_bytes[2]
        dtu_add_High = my_get_com_bytes[3]
    else:
        dtu_add_Low = my_get_com_bytes[5]
        dtu_add_High = my_get_com_bytes[6]
        my_inf_add=my_inf_add_high=my_get_com_bytes[13]
        my_inf_add_Low = my_get_com_bytes[12]
        my_inf_add =my_inf_add*256+my_get_com_bytes[12]

    mydtuadd=dtu_add_Low+dtu_add_High*256
    my_str2=my_get_com_bytes
    #建立链路过程
    if my_str2[0]==0x10 and my_str2[1]==0x49:  #建立链路0X10，0X49
        my_str_short=[0x10,0x8b,0x10,0x00,0x8c,0x16]
        my_str_short[2]=dtu_add_Low
        my_str_short[3]=dtu_add_High
        s2=my_101_com_genert_CRC(my_str_short)
        s3=bytes(s2)
        conn.sendall(s3)
        my_all_step=1
        print("send   data:",end='')
        my_str_to_hex_display(s3)
    elif my_str2[0]==0x10 and my_str2[1]==0x40 and my_all_step==1:
        my_fun_send_OK(conn)
        #10 C9 01 00 CA 16
        my_str_short = [0x10, 0xC9, 0x01, 0x00, 0x81, 0x16]
        my_str_short[2] = dtu_add_Low
        my_str_short[3] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 2
        print("send   data:", end='')
        my_str_to_hex_display(s3)
    elif my_str2[0] == 0x10 and my_str2[1] == 0x0B and my_all_step==2:
        my_str_short = [0x10, 0xC0, 0x01, 0x00, 0x81, 0x16]
        my_str_short[2] = dtu_add_Low
        my_str_short[3] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 3
        print("send   data:", end='')
        my_str_to_hex_display(s3)
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step==3:
        my_str_short = [0x68,0x0B,0x0B ,0x68,0xF3,0x01,0x00,0x46,0x01,0x04,0x01,0x00,0x00,0x00,0x00,0x40,0x16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 4
        print("send   data:", end='')
        my_str_to_hex_display(s3)
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step==4:
        print("link buid finish==")
        # 发送计数同步帧
        my_str_short = [0x68, 0x0C, 0x0C, 0x68, 0x73, 0x01, 0x00, 0xDC, 0x01, 0x65, 0x01, 0x00, 0x01, 0x4F, 0x01, 0x02,0XFF,0x16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        x,y=get_time_count()
        my_str_short[14]=int(x)
        my_str_short[15]=int(y)
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 4
        print("send   data:", end='')
        my_str_to_hex_display(s3)

    #计数同步帧应答
    elif my_str2[0] == 0x68 and my_str2[4] == 0x80 and my_str2[7] == 0xDC and my_str2[9] == 0x66:
        my_heart_time_count = my_heart_time_count + 1
        print("time_count finish==%d"%my_heart_time_count)

    #心跳包
    elif my_str2[0] == 0x10 and my_str2[1] == 0xD2:
        my_fun_send_OK(conn)
        print("heart time finish==")
        #计数同步值
        my_str_short = [0x68, 0x0C, 0x0C, 0x68, 0x73, 0x01, 0x00, 0xDC, 0x01, 0x65, 0x01, 0x00, 0x01, 0x4F, 0x01, 0x02,0XFF, 0x16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        x, y = get_time_count()
        my_str_short[14] = x
        my_str_short[15] = y
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 4
        print("send   data:", end='')
        my_str_to_hex_display(s3)

    #时钟同步应答
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step == 5:
        pass
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x67 and my_str2[9] == 0x07 and my_all_step == 5:
        my_fun_send_OK(conn)
        print("RTC time finish==")

    #周期数据应答
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x68 and my_str2[9] == 0x06:
        #密码验证
        print('周期密码OK')
        my_fun_send_OK(conn)
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x02 and my_str2[9] == 0x14:
        #遥信数据
        zsqA.duanlu=my_str2[14]
        zsqA.jiedi=my_str2[15]
        zsqB.duanlu=my_str2[16]
        zsqB.jiedi=my_str2[17]
        zsqC.duanlu=my_str2[18]
        zsqC.jiedi=my_str2[19]
        print('周期遥信')
        my_fun_send_OK(conn)
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x09 and my_str2[9] == 0x14:
        #遥测数据
        if my_str2[12]==0x01 and my_str2[13]==0x40:
            zsqA.A_all=(my_str2[14]+my_str2[15]*256)/10.0
            zsqA.temperature = (my_str2[17] + my_str2[18] * 256) / 10.0
            zsqA.E_fild= (my_str2[20] + my_str2[21] * 256) / 10.0
            zsqA.Li_bat= (my_str2[23] + my_str2[24] * 256) / 10.0

            zsqB.A_all = (my_str2[26] + my_str2[27] * 256) / 10.0
            zsqB.temperature = (my_str2[29] + my_str2[30] * 256) / 10.0
            zsqB.E_fild = (my_str2[32] + my_str2[33] * 256) / 10.0
            zsqB.Li_bat = (my_str2[35] + my_str2[36] * 256) / 10.0

            zsqC.A_all = (my_str2[38] + my_str2[39] * 256) / 10.0
            zsqC.temperature = (my_str2[41] + my_str2[42] * 256) / 10.0
            zsqC.E_fild = (my_str2[44] + my_str2[45] * 256) / 10.0
            zsqC.Li_bat = (my_str2[47] + my_str2[48] * 256) / 10.0
            print('周期遥测数据')
        elif  my_str2[12]==0x00 and my_str2[13]==0x41:
            mydtu.bat_v=(my_str2[14]+my_str2[15]*256)/10.0
            mydtu.bat_sun=(my_str2[16]+my_str2[17]*256)/10.0
            mydtu.temperature=(my_str2[18]+my_str2[19]*256)/10.0
            mydtu.shidu=(my_str2[20]+my_str2[21]*256)/10.0
            print('周期遥测环境数据')
        my_fun_send_OK(conn)
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x09 and (my_str2[9] == 0x67 or my_str2[9] == 0x68 or my_str2[9] == 0x69):
        #遥测补充、遥测12T、计数同步值
        if my_str2[9] == 0x67:
            zsqA.Sun_bat=(my_str2[14]+my_str2[15]*256)/10.0
            zsqA.xian_V=(my_str2[16]+my_str2[17]*256)/10.0
            zsqA.Gan_bat=(my_str2[18]+my_str2[19]*256)/10.0
            zsqA.A_half=(my_str2[20]+my_str2[21]*256)/10.0

            zsqB.Sun_bat = (my_str2[22] + my_str2[23] * 256) / 10.0
            zsqB.xian_V = (my_str2[24] + my_str2[25] * 256) / 10.0
            zsqB.Gan_bat = (my_str2[26] + my_str2[27] * 256) / 10.0
            zsqB.A_half = (my_str2[28] + my_str2[29] * 256) / 10.0

            zsqC.Sun_bat = (my_str2[30] + my_str2[31] * 256) / 10.0
            zsqC.xian_V = (my_str2[32] + my_str2[33] * 256) / 10.0
            zsqC.Gan_bat = (my_str2[34] + my_str2[35] * 256) / 10.0
            zsqC.A_half = (my_str2[36] + my_str2[37] * 256) / 10.0
            print('周期遥测补充')
        elif my_str2[9] == 0x68:
            ac12tA.T1 =(my_str2[14]+my_str2[15]*256)/10.0
            ac12tA.T2 = (my_str2[16] + my_str2[17] * 256) / 10.0
            ac12tA.T3 = (my_str2[18] + my_str2[19] * 256) / 10.0
            ac12tA.T4 = (my_str2[20] + my_str2[21] * 256) / 10.0
            ac12tA.T5 = (my_str2[22] + my_str2[23] * 256) / 10.0
            ac12tA.T6 = (my_str2[24] + my_str2[25] * 256) / 10.0
            ac12tA.T7 = (my_str2[26] + my_str2[27] * 256) / 10.0
            ac12tA.T8 = (my_str2[28] + my_str2[29] * 256) / 10.0
            ac12tA.T9 = (my_str2[30] + my_str2[31] * 256) / 10.0
            ac12tA.T10 = (my_str2[32] + my_str2[33] * 256) / 10.0
            ac12tA.T11 = (my_str2[34] + my_str2[35] * 256) / 10.0
            ac12tA.T12 = (my_str2[36] + my_str2[37] * 256) / 10.0

            ac12tB.T1 = (my_str2[38] + my_str2[39] * 256) / 10.0
            ac12tB.T2 = (my_str2[40] + my_str2[41] * 256) / 10.0
            ac12tB.T3 = (my_str2[42] + my_str2[43] * 256) / 10.0
            ac12tB.T4 = (my_str2[44] + my_str2[45] * 256) / 10.0
            ac12tB.T5 = (my_str2[46] + my_str2[47] * 256) / 10.0
            ac12tB.T6 = (my_str2[48] + my_str2[49] * 256) / 10.0
            ac12tB.T7 = (my_str2[50] + my_str2[51] * 256) / 10.0
            ac12tB.T8 = (my_str2[52] + my_str2[53] * 256) / 10.0
            ac12tB.T9 = (my_str2[54] + my_str2[55] * 256) / 10.0
            ac12tB.T10 = (my_str2[56] + my_str2[57] * 256) / 10.0
            ac12tB.T11 = (my_str2[58] + my_str2[59] * 256) / 10.0
            ac12tB.T12 = (my_str2[60] + my_str2[61] * 256) / 10.0

            ac12tC.T1 = (my_str2[62] + my_str2[63] * 256) / 10.0
            ac12tC.T2 = (my_str2[64] + my_str2[65] * 256) / 10.0
            ac12tC.T3 = (my_str2[66] + my_str2[67] * 256) / 10.0
            ac12tC.T4 = (my_str2[68] + my_str2[69] * 256) / 10.0
            ac12tC.T5 = (my_str2[70] + my_str2[71] * 256) / 10.0
            ac12tC.T6 = (my_str2[72] + my_str2[73] * 256) / 10.0
            ac12tC.T7 = (my_str2[74] + my_str2[75] * 256) / 10.0
            ac12tC.T8 = (my_str2[76] + my_str2[77] * 256) / 10.0
            ac12tC.T9 = (my_str2[78] + my_str2[79] * 256) / 10.0
            ac12tC.T10 = (my_str2[80] + my_str2[81] * 256) / 10.0
            ac12tC.T11 = (my_str2[82] + my_str2[83] * 256) / 10.0
            ac12tC.T12 = (my_str2[84] + my_str2[85] * 256) / 10.0
            print('周期遥测12T')
        my_fun_send_OK(conn)
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0xDC and my_str2[9] == 0x69:

        dtutimer=(my_str2[14]+my_str2[15]*256)
        RTCtime =str(my_str2[22])+"-"+str(my_str2[21])+"-"+str(my_str2[20])+" "+str(my_str2[19])+":"+str(my_str2[18])+":"+str(my_str2[16])
        mytodattime = datetime.datetime.now()
        myservertime = str(mytodattime.year) +"-"+ str(mytodattime.month) +"-"+ str(mytodattime.day) +" "+ str(
        mytodattime.hour)  +":"+ str(mytodattime.minute) +":"+ str(mytodattime.second)
        print('周期计数同步值')
        #把收到的数据写入到数据库中
        #mydtuadd,RTCtime,dtutimer,mydtu.bat_v,mydtu.bat_sun,mydtu.temperature,mydtu.shidu,
        #zsqA.duanlu, zsqA.jiedi,zsqA.A_all,zsqA.E_fild,zsqA.Li_bat,zsqA.Sun_bat,zsqA.xian_V,zsqA.A_half,zsqA.Gan_bat,zsqA.temperature,zsqA.timer,
        #zsqB.duanlu, zsqB.jiedi, zsqB.A_all, zsqB.E_fild, zsqB.Li_bat, zsqB.Sun_bat, zsqB.xian_V, zsqB.A_half, zsqB.Gan_bat, zsqB.temperature,zsqB.timer,
        #zsqC.duanlu, zsqC.jiedi, zsqC.A_all, zsqC.E_fild, zsqC.Li_bat, zsqC.Sun_bat, zsqC.xian_V, zsqC.A_half, zsqC.Gan_bat,zsqC.temperature, zsqC.timer

        sqlstr ='insert into TB_cycdata  VALUES (1,'+"\'"+str(myservertime)+"\'"+','+str(mydtuadd)+','+"\'"+str(RTCtime)+"\'"+','+str(dtutimer)+','+str(mydtu.bat_v)+','+str(mydtu.bat_sun)+','+str(mydtu.temperature)+','+str(mydtu.shidu)+','+str(zsqA.duanlu)+','+str(zsqA.jiedi)+','+str(zsqA.A_all)+','+str(zsqA.E_fild)+','+str(zsqA.Li_bat)+','+str(zsqA.Sun_bat)+','+str(zsqA.xian_V)+','+str(zsqA.A_half)+','+str(zsqA.Gan_bat)+','+str(zsqA.temperature)+','+str(zsqA.timer)+','+str(zsqB.duanlu)+','+str(zsqB.jiedi)+','+str(zsqB.A_all)+','+str( zsqB.E_fild)+','+str(zsqB.Li_bat)+','+str(zsqB.Sun_bat)+','+str(zsqB.xian_V)+','+str(zsqB.A_half)+','+str( zsqB.Gan_bat)+','+str(zsqB.temperature)+','+str(zsqB.timer)+','+str(zsqC.duanlu)+','+str(zsqC.jiedi)+','+str(zsqC.A_all)+','+str( zsqC.E_fild)+','+str(zsqC.Li_bat)+','+str(zsqC.Sun_bat)+','+str(zsqC.xian_V)+','+str(zsqC.A_half)+','+str(zsqC.Gan_bat)+','+str(zsqC.temperature)+','+str( zsqC.timer)+')'
        print(sqlstr)
        my_fun_SQL_insertdata(sqlstr)
        my_fun_send_OK(conn)
    #DTU复位进程命令
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step == 7:
        pass
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x69 and my_str2[9] == 0x07 and my_all_step == 7:
        my_fun_send_OK(conn)
        my_all_step = 0
        print("rest com finish==")
    #设定参数1
    elif my_str2[0] == 0x68 and my_str2[4] == 0X00 and my_str2[7] == 0x30 and my_str2[9] == 0x07 and my_all_step == 8:
        pass
        my_all_step = 0
        print("set para_1 com finish==")
        # 设定参数1
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step == 9:
        pass
        my_all_step = 0
        print("set para_2 finish==")
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step == 10:
        pass
        my_all_step = 0
        print("set para_3 finish==")
    elif my_str2[0] == 0x68 and my_str2[4] == 0X00 and my_str2[7] == 0x2D and my_str2[9] == 0x07 and my_all_step == 11:
        pass
        my_all_step = 0
        print("Control finish==")
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x09 and my_str2[9] == 0x71 and my_all_step == 12:
        pass
        my_all_step = 0
        print("Get RTC finish==")
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step == 13:
        pass
    elif my_str2[0] == 0x68 and my_str2[4] == 0x00  and my_str2[7] == 0x30 and my_str2[9] == 0x07 and my_all_step == 13 and my_inf_add==0x5020:
        pass
        my_all_step = 0
        print("Get para finish==")
    #文件录波数据
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step == 14:
        pass
        file_count=0
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73)  and my_str2[7] == 0x64 and my_str2[9] == 0x72 and my_all_step == 14:
        file_count=file_count+1
        my_str_short = [0x68, 0x0B, 0x0B, 0x68, 0x73, 0x01, 0x00, 0x64, 0x01, 0x73, 0x01, 0x00, 0x01, 0x45,0X00,0XFF, 0x16]
        my_str_short[12] =  my_inf_add_Low
        my_str_short[13] =  my_inf_add_high
        my_str_short[14]=file_count


        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High

        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 14
        print("send   data:", end='')
        my_str_to_hex_display(s3)

        print("Get File finish==%d"%file_count)

    else:
        my_fun_send_OK(conn)

    #########服务器主动发送
    # 时钟同步
    my_time_adjust_status=1#1为允许此主动发送命令，0为不开启此命令
    my_heart_cyc_time=5 #RTC时间校正对应的心跳周

    my_call_data_stasut=0
    cyc_time=337
    my_reset_com_status=0
    my_reset_com_cyc_time=17

    my_set_parameter_status=0
    my_set_parameter_cyc_time=3

    my_set_parameter_status2 = 0
    my_set_parameter_cyc_time2 = 5

    my_set_parameter_status3 = 0
    my_set_parameter_cyc_time3 = 7

    my_Control_para_status = 0
    my_Control_para_status_time = 7

    my_RTC_para_status = 0
    my_RTC_para_status_time = 3

    my_get_para_status = 0
    my_get_para_status_time = 3

    my_get_file_status=0
    my_get_file_status_time=5
  #RTC时间校正
    if my_heart_time_count%my_heart_cyc_time==0 and my_time_adjust_status==1:
        my_str_short = [0x68,0x11,0x11,0x68,0x53,0x01,0x00,0x67,0x01,0x06,0x01,0x00,0x00,0x00,0x8B,0xD4,0x0B,0x0F,0x05,0x07,0x0E,0x56,0x16]
        my_str_short[5] =my_str_short[10]= dtu_add_Low
        my_str_short[6] =my_str_short[11]= dtu_add_High
        x=datetime.datetime.now()
        my_str_short[14] =int(x.second)
        my_str_short[15] =0
        my_str_short[16] = int(x.minute)
        my_str_short[17] = int(x.hour)
        my_str_short[18] = x.day
        my_str_short[19] = int(x.month)
        my_str_short[20] = int(x.year)%100

        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 5
        print('heart time=%d' % my_heart_time_count)
        print("RTC send   data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
    #总召周期数据
    elif my_heart_time_count%cyc_time==0 and my_call_data_stasut==1:
        my_str_short = [0x68,0x0B,0x0B,0x68,0x73,0x01,0x00,0x64,0x01,0x06,0x01,0x00,0x00,0x00,0x14,0xF4,0x16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 6
        print('heart time=%d' % my_heart_time_count)
        print("call   data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
    #发送重新启动命令
    elif my_heart_time_count%my_reset_com_cyc_time==0 and my_reset_com_status==1:
        my_str_short = [0x68,0x0B,0x0B,0x68,0x73,0x01,0x00 ,0x69 ,0x01 ,0x06 ,0x01 ,0x00 ,0x00 ,0x00 ,0x01 ,0xE6 ,0x16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 7
        print('heart time=%d' % my_heart_time_count)
        print("rest com data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
        #发送设置参数命令
    elif my_heart_time_count%my_set_parameter_cyc_time==0 and my_set_parameter_status==1:
        my_str_short = [0x68,0x0C ,0x0C ,0x68 ,0x73 ,0x03 ,0x00 ,0x30 ,0x01 ,0x06 ,0x03 ,0x00 ,0x02 ,0x50 ,0x12 ,0x00 ,0x0E ,0x16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 8
        print('heart time=%d' % my_heart_time_count)
        print("set prara_1 send data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
        #发送设置参数命令2
    elif my_heart_time_count%my_set_parameter_cyc_time2==0 and my_set_parameter_status2==1:
        my_str_short = [0x68,0x0C,0x0C ,0x68 ,0x73 ,0x03 ,0x00 ,0x64 ,0x01 ,0x6E ,0x03 ,0x00 ,0x10 ,0x50 ,0x01 ,0x02 ,0x0E ,0x16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 9
        print('heart time=%d' % my_heart_time_count)
        print("set prara_2 send data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
        #发送设置参数命令3
    elif my_heart_time_count%my_set_parameter_cyc_time3==0 and my_set_parameter_status3==1:
        my_str_short = [0x68,0x0E,0x0E ,0x68 ,0x73 ,0x03 ,0x00 ,0x64 ,0x01 ,0x6E ,0x03 ,0x00 ,0x31 ,0x50 ,0x01 ,0x00 ,0X03,0X04,0x0E ,0x16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 10
        print('heart time=%d' % my_heart_time_count)
        print("set prara_3 send data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
        #发送控制命令
    elif my_heart_time_count%my_Control_para_status_time==0 and my_Control_para_status==1:
        my_str_short = [0X68,0X0E ,0X0E ,0X68 ,0X73 ,0X03 ,0X00 ,0X2D ,0X02 ,0X06 ,0X03 ,0X00 ,0X01 ,0X60 ,0X01 ,0X02 ,0X60 ,0X00 ,0X72 ,0X16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 11
        print('heart time=%d' % my_heart_time_count)
        print("Control para send data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
     #发送获取RTC时间命令
    elif my_heart_time_count%my_RTC_para_status_time==0 and my_RTC_para_status==1:
        my_str_short = [0X68,0X0C ,0X0C ,0X68 ,0X73 ,0X03 ,0X00 ,0X09 ,0X01 ,0X70 ,0X03 ,0X00 ,0X70 ,0X50 ,0X00 ,0X00 ,0XFF ,0X16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 12
        print('heart time=%d' % my_heart_time_count)
        print("Get RTC send data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
   #发送获得参数命令
    elif my_heart_time_count%my_get_para_status_time==0 and my_get_para_status==1:
        my_str_short = [0X68,0X0C ,0X0C ,0X68 ,0X73 ,0X03 ,0X00 ,0X30 ,0X01 ,0X06 ,0X03 ,0X00 ,0X20 ,0X50 ,0X00 ,0X00 ,0XFF ,0X16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 13
        print('heart time=%d' % my_heart_time_count)
        print("Get prara send data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
        #发送获得文件命令
    elif my_heart_time_count%my_get_para_status_time==0 and my_get_file_status==1:
        my_str_short = [0X68,0X0B ,0X0B ,0X68 ,0X73 ,0X03 ,0X00 ,0X64 ,0X01 ,0X6D ,0X03 ,0X00 ,0X01 ,0X45 ,0X00 ,0XFF ,0X16]
        my_str_short[5] = my_str_short[10] = dtu_add_Low
        my_str_short[6] = my_str_short[11] = dtu_add_High
        s2 = my_101_com_genert_CRC(my_str_short)
        s3 = bytes(s2)
        conn.send(s3)
        my_all_step = 14
        print('heart time=%d' % my_heart_time_count)
        print("Get File send data:", end='')
        my_str_to_hex_display(s3)
        my_heart_time_count=my_heart_time_count+1
    #my_str_to_hex_display(buf)


##################################################3333
##多线程处理函数
class MyServer(socketserver.BaseRequestHandler):

    def handle(self):

        conn = self.request
        myls=bytes((0x01,0x02,0x03))

        conn.sendall(myls)

        Flag = True

        while Flag:

            data = conn.recv(1024)
            #print(data)
            my_fun_work(data,conn)



if __name__ == '__main__':

    server = socketserver.ThreadingTCPServer(('106.14.41.25',2216),MyServer)

    server.serve_forever()


