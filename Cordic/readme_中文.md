# README.md

## 📁 CORDIC 算法 RTL 实现项目

完整的 CORDIC 算法实现，包含 Verilog RTL 设计、Python 模型和自动化验证流程。

## 📂 项目结构

```
├── vscode/
│   └── tasks.json           # VS Code配置
├── Cordic.assets/           # Cordic文档图片资源
│   └── image.png
├── Dataset/
│   ├── Model_Data/          # Python模型数据
│   │   ├── Model_Theta_SO18F0.dat
│   │   ├── Model_Cos_Out_SO18F0.dat
│   │   └── Model_Sin_Out_SO18F0.dat
│   ├── RTL_Data/            # RTL模型数据
│   │   ├── RTL_Cos_Out_SO18F0.dat
│   │   └── RTL_Sin_Out_SO18F0.dat
├── python_model/            # Python模型
│   └── Cordic.py
├── rtl_model/               # RTL模型
│   ├── Cordic.v             # CORDIC核心模块
│   ├── Cordic_Test.v        # 测试平台
│   └── simulation/          # 仿真日志
│   └── check_data.py        # 数据验证脚本
└── Codic.ipynb              # 核心代码实验记录
```

## ⚙️ 依赖环境

1. **仿真工具**
   • Icarus Verilog (iverilog) ≥ 11.0
   • VVP 运行时（随 Icarus 安装）

2. **Python 环境**
   • Python 3.11+

3. **推荐工具**
   • Visual Studio Code + Verilog 扩展插件
   • Jupyter Lab（查看实验记录）

## 📚 目录指南

1. **/vscode**
   • `tasks.json`: 预配置的一键式仿真任务
   • 支持任务：
   ▶️ RTL 编译
   ▶️ 仿真运行
   ▶️ 数据验证

2. **/rtl_model**
   • `Cordic.v`: 流水线式 CORDIC 核心（16 级迭代）
   • `Cordic_Test.v`: 支持文件 IO 的测试平台
   • 关键参数：

   ```verilog
   parameter NUM_ITER = 16;    // CORDIC迭代次数
   parameter FRAC_BITS = 16;   // Q1.16定点数格式
   ```

3. **/Dataset**
   • Model_Data/: 1°-89° 参考数据（黄金标准）
   • RTL_Data/: 仿真输出数据
   • 验证脚本：

   ```bash
   python3 Dataset/check_data.py -t 3 Model_Data/ RTL_Data/
   ```

4. **/python_model**
   • 完整的 CORDIC 实现与误差分析
   • 命令行操作：

   ```bash
   # 生成数据
   python3 Cordic.py generate

   # 验证精度
   python3 Cordic.py verify
   ```

## 🚀 使用流程

**步骤 1：生成参考数据**

```bash
cd python_model
python Cordic.py generate
```

**步骤 2：验证参考数据**

```bash
cd python_model
python Cordic.py verify
```

**注意**：需先生成参考数据以验证模型数据精度

**步骤 3：运行 RTL 仿真**
在路径 `rtl_model` 下执行：

```bash
# 编译（项目根目录）
iverilog -o simv Cordic.v Cordic_Test.v

# 运行仿真（编译后执行）
vvp simv
```

或  
**VSCode 用户**：使用预配置任务：  
`运行任务(Run Task) -> Run Cordic Test` 编译  
`运行任务(Run Task) -> Simulate` 生成验证用 RTL 数据

**步骤 4：数据验证**
在项目根目录 `Cordic` 下执行：

```bash
python Dataset/check_data.py Dataset/Model_Data Dataset/RTL_Data
```

或  
在路径 `Cordic/Dataset` 下执行：

```bash
python check_data.py Model_Data RTL_Data
```

**VSCode 用户**：通过菜单路径  
`终端 > 运行任务(Run Task) -> Verify Data` 使用预配置任务
