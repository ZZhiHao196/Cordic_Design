# README.md

## 📁 CORDIC Algorithm RTL Implementation Project

A complete implementation of CORDIC algorithm with Verilog RTL design, Python model and automatic verification flow.

##  📂 Project Structure

```
├── vscode/
│   └── tasks.json           # config
├── Cordic.assets/           # Cordic.md images
│   └── iamge.png
├── Dataset/
│   ├── Model_Data/          # python model data
│   │   ├── Model_Theta_SO18F0.dat
│   │   ├── Model_Cos_Out_SO18F0.dat
│   │   └── Model_Sin_Out_SO18F0.dat
│   ├── RTL_Data/            # RTL model data
│   │   ├── RTL_Cos_Out_SO18F0.dat
│   │   └── RTL_Sin_Out_SO18F0.dat
├── python_model/            # Python model
│   └── Cordic.py
├── rtl_model/               # RTL Model
│   ├── Cordic.v             # CORDIC core
│   ├── Cordic_Test.v        # testbench
│   └── simulation/          # simualtion log
│   └── check_data.py        # data validation
└── Codic.ipynb              # core code record

```

## ⚙️ Dependencies

1. **Simulation Tools**
   • Icarus Verilog (iverilog) >= 11.0
   • VVP Runtime (bundled with Icarus)

2. **Python Environment**
   • Python 3.6+
   • Core Packages: numpy, matplotlib (for analysis)

3. **Recommended Tools**
   • Visual Studio Code with Verilog extension
   • Jupyter Lab (for notebook)



## 📚 Directory Guide

1. **/vscode**
   • `tasks.json`: Preconfigured build tasks for 1-click simulation
   • Supported Tasks:
     ▶️ RTL Compilation
     ▶️ Simulation
     ▶️ Data Validation

2. **/rtl_model**
   • `Cordic.v`: Pipelined CORDIC core (16-stage)
   • `Cordic_Test.v`: Testbench with file I/O
   • Key Parameters:

     ```verilog
   parameter NUM_ITER = 16;    // CORDIC iterations
   parameter FRAC_BITS = 16;  // Q1.16 fixed-point
     ```

3. **/Dataset**
   • Model_Data/: 89-angle golden data (1°-89°)
   • RTL_Data/: Simulation outputs
   • Validation Script:

     ```bash
   python3 Dataset/check_data.py -t 3 Model_Data/ RTL_Data/
     ```

4. **/python_model**
   • Full CORDIC implementation with error analysis
   • CLI Commands:

     ```bash
     # Generate data
     python3 Cordic.py generate
   
     # Verify accuracy
     python3 Cordic.py verify 
     ```

   



## 🚀 Workflow Guide

**Step 1: Generate Reference Data**

```bash
cd python_model
python Cordic.py generate
````



**Step 2: Verify Reference  Data**

```bash
cd python_model
python Cordic.py verify
```

**Note**: You need to generate Reference Data first to Verify model data with Accurate data

**Step 3: Run RTL Simulation**

under the path : `rtl_model`

```bash
# Compile (from project root)
iverilog -o simv Cordic.v Cordic_Test.v

# Run Simulation after compilation
vvp simv
```

or

To compile, in **Vscode**, used preconfigured tasks：`Run Task->Run Cordic Test `; `Run Task-->Simulate` could be used to generate RTL data for validation

**Step 4: Data Validation**

You can validate the model data with reference data under the `Cordic`,  and run:

```bash
python Dataset/check_data.py Dataset/Model_Data Dataset/RTL_Data

```

or 

Under the path :`Cordic/Dataset`, run:

```bash
python check_data.py Model_Data RTL_Data
```

for **Vscode Users**: Use preconfigured tasks via `Terminal > Run Task->Verify Data`
