from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np



def test_oracle(n, oracle_type):
    qc = QuantumCircuit(n + 1, n)
    # 翻转为1
    qc.x(n)
    # 对所有 n+1 个比特应用 H 门
    qc.h(range(n + 1))
    
    if oracle_type == "parity":
        # 奇偶性：f(x)=x₀⊕x₁⊕x₂ → 坍缩到111
        for i in range(n):
            qc.cx(i, n)
            # i为控制比特，n为目标比特
            
    elif oracle_type == "first_bit":
        # 只依赖第一个比特：f(x)=x₀ → 坍缩到001
        qc.cx(0, n)
        
    elif oracle_type == "second_bit":
        # 只依赖第二个比特：f(x)=x₁ → 坍缩到010
        qc.cx(1, n)
        
    elif oracle_type == "third_bit":
        # 只依赖第三个比特：f(x)=x₂ → 坍缩到100
        qc.cx(2, n)
        
    elif oracle_type == "majority":
        # 多数函数（复杂平衡函数）→ 可能坍缩到其他态
        qc.ccx(0, 1, n)  # 需要更复杂的实现
    
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc









# def deutsch_jozsa(n):
    # 创建量子电路：n+1 个量子比特用于计算，n 个经典比特用于测量；最后一个量子比特（索引 n）是辅助比特
    # 0-n-1 为控制比特，n 为辅助比特
    # qc = QuantumCircuit(n + 1, n)   
    # breakpoint()


    # x门将辅助比特初始化为｜1>;H门将所有比特置于叠加态
    # 括号中的参数为量子比特的索引
    # qc.x(n) # 对辅助比特应用X门，将其从|0>变为|1>
    # qc.h(range(n + 1))  # 对所有量子比特应用Hadamard门


    # 简单 balanced oracle f(x) 异或操作
    # for i in range(n):
        # """
        # 每个输入比特都通过CNOT门与辅助比特耦合
        # 函数 f(x) 定义为 f(x) = x_0 ⊕ x_1 ⊕ ... ⊕ x_{n-1}（奇偶性）
        # 对于n=3，有4个输入使f(x)=0，4个输入使f(x)=1，因此是平衡的
        # """
        # qc.cx(i, n) # CNOT门：控制位i，目标位n（辅助比特）
    

    # """
    # 第二次H门用于干涉，将相位信息转换为振幅信息
    # 如果是常数函数，测量结果全为0
    # 如果是平衡函数，测量结果非全0
    # """
    # qc.h(range(n))  # 对前n个量子比特再次应用H门
    # qc.measure(range(n), range(n))  # 测量并存储到经典比特

    # return qc

qc = test_oracle(3, "first_bit")
# qc = deutsch_jozsa(3)  # 创建Deutsch-Jozsa电路，n=3

sim = AerSimulator()    # 使用Aer模拟器
# 使用 GPU 进行模拟
# sim_gpu = AerSimulator(method='statevector', device='GPU')


result = sim.run(qc, shots=1024).result()   # 运行1024次

"""
(Pdb) result.get_counts
<bound method Result.get_counts of Result(backend_name='aer_simulator', backend_version='0.17.2', job_id='d75ca816-ee3a-4a7c-8eb6-9caa5ab8deb5', 
success=True, results=[ExperimentResult(shots=1024, success=True, meas_level=2, data=ExperimentResultData(counts={'0x0': 1024}), 
header={'creg_sizes': [['c', 3]], 'global_phase': 0.0, 'memory_slots': 3, 'n_qubits': 4, 'name': 'circuit-46', 
'qreg_sizes': [['q', 4]], 'metadata': {}}, status=DONE, seed_simulator=453817674, metadata={'num_bind_params': 1, 'runtime_parameter_bind': False, 
'parallel_state_update': 8, 'parallel_shots': 1, 'sample_measure_time': 0.000979166, 'noise': 'ideal', 'batched_shots_optimization': False, 
'remapped_qubits': False, 'active_input_qubits': [0, 1, 2, 3], 'device': 'CPU', 'time_taken': 0.002850042, 'measure_sampling': True, 
'num_clbits': 3, 'max_memory_mb': 16384, 'input_qubit_map': [[3, 3], [2, 2], [1, 1], [0, 0]], 'num_qubits': 4, 'method': 'stabilizer', 
'required_memory_mb': 0, 'fusion': {'enabled': False}}, time_taken=0.002850042)], date=2026-04-01T14:36:11.710882, status=COMPLETED, 
header=None, qobj_id='', metadata={'time_taken_parameter_binding': 0.0002555, 'max_memory_mb': 16384, 'time_taken_execute': 0.003537334, 
'omp_enabled': True, 'max_gpu_memory_mb': 0, 'parallel_experiments': 1}, time_taken=0.015402078628540039)>
"""
print(result.get_counts())
