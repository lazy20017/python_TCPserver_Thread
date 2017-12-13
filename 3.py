import socket
import  datetime
def my_fun_send_OK():
    my_str_short = [0x10, 0x80, 0x01, 0x00, 0x81, 0x16]
    my_str_short[2] = dtu_add_Low
    my_str_short[3] = dtu_add_High
    s2 = my_101_com_genert_CRC(my_str_short)
    s3 = bytes(s2)
    conn.send(s3)
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




################################333
sk = socket.socket()
sk.bind(("106.14.41.25",2216))
sk.listen(5)
conn,address = sk.accept()
conn.sendall(bytes("Hello world",encoding="utf-8"))
my_all_step=0
my_heart_time_count=1
while True:


    buf=conn.recv(1024)
    my_get_com_bytes=my_get_fram(buf)
    if my_get_com_bytes==None:
        continue

    if my_get_com_bytes[0]==0x10:
        dtu_add_Low = my_get_com_bytes[2]
        dtu_add_High = my_get_com_bytes[3]
    else:
        dtu_add_Low = my_get_com_bytes[5]
        dtu_add_High = my_get_com_bytes[6]
        my_inf_add=my_inf_add_high=my_get_com_bytes[13]
        my_inf_add_Low = my_get_com_bytes[12]
        my_inf_add =my_inf_add*256+my_get_com_bytes[12]



    my_str2=my_get_com_bytes
    #建立链路过程
    if my_str2[0]==0x10 and my_str2[1]==0x49:  #建立链路0X10，0X49
        my_str_short=[0x10,0x8b,0x10,0x00,0x8c,0x16]
        my_str_short[2]=dtu_add_Low
        my_str_short[3]=dtu_add_High
        s2=my_101_com_genert_CRC(my_str_short)
        s3=bytes(s2)
        conn.send(s3)
        my_all_step=1
        print("send   data:",end='')
        my_str_to_hex_display(s3)
    elif my_str2[0]==0x10 and my_str2[1]==0x40 and my_all_step==1:
        my_fun_send_OK()
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
        my_fun_send_OK()
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
        my_fun_send_OK()
        print("RTC time finish==")

    #周期数据应答
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x68 and my_str2[9] == 0x06:
        my_fun_send_OK()
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x09 and my_str2[9] == 0x12:
        my_fun_send_OK()
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x09 and (my_str2[9] == 0x67 or my_str2[9] == 0x68 or my_str2[9] == 0x69):
        my_fun_send_OK()
    #DTU复位进程命令
    elif my_str2[0] == 0x10 and my_str2[1] == 0x00 and my_all_step == 7:
        pass
    elif my_str2[0] == 0x68 and (my_str2[4] == 0x53 or my_str2[4] == 0x73) and my_str2[7] == 0x69 and my_str2[9] == 0x07 and my_all_step == 7:
        my_fun_send_OK()
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
        my_fun_send_OK()






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
    '''
    sx= my_get_fram(buf)
    if sx!=None:
        s = str(sx, encoding="utf-8")
        print('return data:',end='')
        my_str_to_hex_display(s)
    else:
        print('data error none')
    '''




