
import pandas as pd 
import matplotlib.pyplot as plt

def get_data(path,i):
    data_csv = pd.read_csv(path,usecols=[i])
    #数据预处理
    data_csv = data_csv.dropna() #去掉na数据
    dataset = data_csv.values      #字典(Dictionary) values()：返回字典中的所有值。
    # dataset = dataset.astype('float32')   #astype(type):实现变量类型转换  
    return dataset

def plot_():
    path = "./huanghe_data.csv"
    sanxiamen = get_data(path,1)
    huayuankou = get_data(path,2)

    plt.figure(figsize=(8,6))
    plt.plot(sanxiamen,linestyle = '-',color='dodgerblue',label='sanxiamen', linewidth = 1)  
    plt.plot(huayuankou,linestyle = ':',color='r',alpha = 1, label='huanyuankou', linewidth = 1)   
    plt.ylabel('data')  
    plt.xlabel('time')   
    plt.legend()  
    plt.show() 
    plt.savefig("test.png")


def run():
    plot_()


if __name__ == "__main__":
    run()

