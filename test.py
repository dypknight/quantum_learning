from pyqpanda import *

if __name__ == "__main__":
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    # breakpoint()
    prog1 = QProg()
    prog1 <<H(qubits[0]) <<CNOT(qubits[1],qubits[2])
    mat = get_matrix(prog1,True)
    prog = QProg()
    prog << QOracle([qubits[0],qubits[1],qubits[2]],mat)

    res1 = qvm.prob_run_dict(prog1,qubits)
    res2 = qvm.prob_run_dict(prog,qubits)

    # 打印测量结果
    print(res1)
    print(res2)