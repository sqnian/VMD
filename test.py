from vmd import VMD
import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd
from scipy.fftpack import fft
import os
import re


def get_data(file_path:str,i):
    file = pd.read_csv(file_path,usecols=[i],engine='python')
    file_values = file.values
    return file_values

def get_vmd(values, alpha, tau, K, DC, init, tol):
    """  
    alpha、tau、K、DC、init、tol 六个输入参数的无严格要求； 
    alpha 带宽限制 经验取值为 抽样点长度 1.5-2.0 倍； 
    tau 噪声容限 
    K 分解模态(IMF)个数
    DC 合成信号若无常量，取值为 0;若含常量,则其取值为 1 
    init 初始化 w 值，当初始化为 1 时，均匀分布产生的随机数； 
    tol 控制误差大小常量，决定精度与迭代次数
    """

    u, u_hat, omega = VMD(values, alpha, tau, K, DC, init, tol)  
    return u, u_hat, omega

def vmd_plot(u,omega,K):
    # 模态分量
    for i in range(K):
        plt.figure(figsize=(7,7), dpi=200)
        plt.subplot(K,1,i+1)
        plt.plot(u[i,:], linewidth=0.2, c='r')
        plt.ylabel('IMF{}'.format(i+1))
        plt.show()
     
    # 中心模态
    for i in range(K):
        plt.figure(figsize=(7,7), dpi=200)
        plt.subplot(K,1,i+1)
        plt.plot(abs(fft(u[i,:])))
        plt.ylabel('MODE{}'.format(i+1))
        plt.show()
        
    # 中心频率
    # plt.figure(figsize=(12, 7), dpi=80)
    for i in range(K):
        plt.figure(figsize=(7,7), dpi=200)
        plt.subplot(K, 1, i + 1)
        plt.plot(omega[:,i]) # X轴为迭代次数，y轴为中心频率
        plt.ylabel('Frequan{}'.format(i+1))
        # plt.title('mode center-frequencies{}'.format(i + 1))

def compute_frequan(K,i):
    path = r"./vmd/" 
    k_list =[]

    FileNames = os.listdir(path)
    # print("FileNames:\n",FileNames)
    for fn in FileNames:

        if fn.startswith('Freq'):
            fullfilename = os.path.join(path, fn)
            if i == 1:
                values = get_data(fullfilename,0).mean()  # 平均值方式
            elif i==2 :
                values = get_data(fullfilename,0)[-10:].sum() / 10   # 后10位均值
            else:
                values = get_data(fullfilename,0)[len(get_data(fullfilename,0)) // 2 ] # 中间值
            
            k_list.append(values)
    return k_list



def vmd_save(u,u_,u_hat_,omega,omega_,K):
    # 保存数据到文件中
    if u_:
        for i  in range(K):
            a = u[i,:]
            dataframe = pd.DataFrame({'v{}'.format(i+1):a})
            dataframe.to_csv(r"./vmd/IMF_%d.csv"%(i+1),index=False,sep=',')  

    if u_hat_:
        for i  in range(K):
            a = abs(fft(u[i,:]))
            dataframe = pd.DataFrame({'v{}'.format(i+1):a})
            dataframe.to_csv(r"./vmd/MODE_%d.csv"%(i+1),index=False,sep=',')  

    if omega_:
        for i  in range(K):
            a = omega[i,:]
            dataframe = pd.DataFrame({'v{}'.format(i+1):a})
            dataframe.to_csv(r"./vmd/Frequan_%d.csv"%(i+1),index=False,sep=',')  

def run():
    file_path = './vmd/huanghe_data.csv'
    file_values = get_data(file_path,1)

    alpha = 7000      # moderate bandwidth constraint  
    tau = 0.            # noise-tolerance (no strict fidelity enforcement)  
    K = 5        # 3 modes  
    DC = 0             # no DC part imposed  
    init = 1           # initialize omegas uniformly  
    tol = 1e-7 

    u, u_hat, omega = get_vmd(file_values, alpha, tau, K, DC, init, tol)

    # plot  u, u_hat, omega
    vmd_plot(u,omega,K)

    # store u, u_hat, omega data 
    vmd_save(u,True,True,omega,True,K)
    
    # 中心频率计算方式
    frequan_list = compute_frequan(K,1)
    print(frequan_list)

if __name__ == "__main__":
    run()