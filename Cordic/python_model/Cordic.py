#初始化部分，定义参数
import os
import argparse
import math
from math import floor
from pathlib import Path

NUM_ITER = 16
Frac_Bits=16
Data_Scale=2**Frac_Bits

#  according to the project sturcture set path
BASE_DIR = Path(__file__).parent.parent  # return to project root directory
MODEL_DATA_DIR = BASE_DIR / "Dataset" / "Model_Data"  # absolute path to model data directory


FILE_NAMES = {
    "theta": "Model_Theta_S0I1F16.dat",
    "cos": "Model_Cos_Out_S0I1F16.dat",
    "sin": "Model_Sin_Out_S0I1F16.dat"
}

Angles_Table = []

def create_angel_table():

    for i in range(NUM_ITER):
        angles=math.atan(2**(-i))
        quantized_angles=floor(angles*Data_Scale+0.5)
        #print(angles)
        #print(angles)
        #angles=angles*(1<<Frac_Bits)+0.5
        #angles=floor(angles)
        #print(angles)
        #print(hex(angles))
        Angles_Table.append(quantized_angles/Data_Scale)

def compute_k():
    k=1.0
    for i in range(NUM_ITER):
        angles=math.atan(2**(-i))
        k=k*math.cos(angles)
    #print(K)
    #print(hex(floor(K*(1<<Frac_Bits)+0.5)))
    return  floor(k*Data_Scale+0.5)/Data_Scale  


def cordic(theta,k):
    x=k
    y=0
    angle_temp= floor(math.radians(theta)*Data_Scale+0.5)/Data_Scale  
    for i in range(NUM_ITER):
        if(angle_temp>=0):
            x_next=x-y*2**(-i)
            y_next=y+x*2**(-i)
            angle_temp-=Angles_Table[i]
        else:   
            x_next=x+y*2**(-i)
            y_next=y-x*2**(-i)
            angle_temp+=Angles_Table[i]
        x=x_next
        y=y_next
    return x,y


def generate_test_data():
    """generate test data for CORDIC RTL Model"""
    MODEL_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    create_angel_table()
    k = compute_k()
   
   # intialize file paths
    
    files = {
        name: open(MODEL_DATA_DIR / fname, "w")
        for name, fname in FILE_NAMES.items()
    }

    try:

         for deg in range(1, 90):
            # CORDIC calculation
            cos_val, sin_val = cordic(deg, k)
            # quantize
            theta_quant = floor(math.radians(deg) * Data_Scale + 0.5)
            cos_quant = floor(cos_val * Data_Scale + 0.5)
            sin_quant = floor(sin_val * Data_Scale + 0.5)
            # write to file (fixed 5-bit hex)
            files["theta"].write(f"{theta_quant:05x}\n")
            files["cos"].write(f"{cos_quant:05x}\n")
            files["sin"].write(f"{sin_quant:05x}\n")
    finally:
        for f in files.values():
            f.close()

    print(f"Model data files generated at :{MODEL_DATA_DIR.absolute()}")


def verify_test_data(threshold = 3):
    """verify the CORDIC results"""
    create_angel_table()
    k = compute_k()
   # intialize file paths
    """verify data accuracy"""
    error_log = []
    
    # 读取生成数据
    try:
        with (
     
            open(MODEL_DATA_DIR / FILE_NAMES["cos"]) as f_cos,
            open(MODEL_DATA_DIR / FILE_NAMES["sin"]) as f_sin
        ):
            for line_num, (cos_line, sin_line) in enumerate(zip(f_cos, f_sin), 1):
                # 解析生成值
                gen_cos = int(cos_line.strip(), 16)
                gen_sin = int(sin_line.strip(), 16)
                
                # 计算理论值
                deg = line_num  # 行号对应角度值
                true_cos = floor(math.cos(math.radians(deg)) * Data_Scale + 0.5)
                true_sin = floor(math.sin(math.radians(deg)) * Data_Scale + 0.5)
                
                # 计算误差
                cos_err = abs(gen_cos - true_cos)
                sin_err = abs(gen_sin - true_sin)
                
                if cos_err > threshold or sin_err > threshold:
                    error_log.append((
                        deg,
                        f"Cos: generated{gen_cos:04x} vs true{true_cos:04x} (Δ={cos_err})",
                        f"Sin: generated{gen_sin:04x} vs true{true_sin:04x} (Δ={sin_err})"
                    ))
    except FileNotFoundError:
        print(f"error:unable to find model data filesplease run generate command first")
        return False

    # generting report
    if error_log:
        print(f"\n There are {len(error_log)}inaccurate points(with threshold={threshold}LSB):")
        for deg, cos_msg, sin_msg in error_log[:5]:  # 最多显示前5个错误
            print(f"[{deg:03}°] {cos_msg} | {sin_msg}")
        return False
    
    print("all the points are meet the precision requirement")
    return True
    
def main():
    parser = argparse.ArgumentParser(description="CORDIC model data generating and verification tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # generate command
    gen_parser = subparsers.add_parser('generate', help='generate model data')
    
    # verify command
    verify_parser = subparsers.add_parser('verify', help='verify the model data')
    verify_parser.add_argument('-t', '--threshold', type=int, default=3,
                             help='allowed maximum LSB error')

    args = parser.parse_args()

    if args.command == "generate":
        generate_test_data()
    elif args.command == "verify":
        success = verify_test_data(args.threshold)
        exit(0 if success else 1)

if __name__ == "__main__":
   main()
