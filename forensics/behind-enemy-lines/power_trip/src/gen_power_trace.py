import numpy as np
import matplotlib.pyplot as plt

LOW, MEDIUM, HIGH = 143, 213, 237
WIDTH = 50
SMOOTHNESS = int(0.6 * WIDTH)

key = 0x67abcaee7dd4ed8998efae04b6966eb368e1d612f0079c17e2cedcbcda4e1219f331041b57ca22d7530ebf564068a140fcc5f05d9b3204b5d1a60a44b237ad8d15e5a3647f26f07290a150e5820cb75877bcbb0c270e5d2cb98c23642b33778293c9ea938fb7da0469c151dd2a6631488bc71a69f7e8981d255139b4972ed30d618e31c741e96e71c9011969aaab176d1ab91d51f9a1fdc21786598556fb35c545f86a28fc8d280e12b5cd86219c0339f12c9d396274e69fedacb31ab15af90b0f9489102e942136c4ab40733db716c841ffefaaa9bdb83f07e80cfb07b0a8b5048da81f2adf19b12b5f350f56993a91f108df44bfe3d64ed7a1cb298e505bf46ea7714dc9303134a303646b880af163dbcce935443ef5aa4842a92939da270cc53ee82b3381fcc04e705c1a4cebc426b1a2e05cc654fbb3f024f6f68d903f58198a070f6d0bcb710c1a24321841175417a0c2363dda2a863b33c668cd0ec33ee6f3aefcdee180c397d600a67ffea2075844f3a7b7b579c6185c1e1de0979a7bad0c89af9381aaecc09ac3c9eed04f7b4dbd651c722836f1f536cfe59fd8a80b91a20004da31cc69bd07412cfdf0c72f6837efd08e9fe497e4ffd1fe708b402035bc43787fa15ed5ddf152d48dd7f6343a265a379b2ab2b5b81f962c84ee9638d686f65e9591757c836104504435c004e6521186636c9f79f9218fdc321e8fd1
keybits = str(bin(key)[2:])

trace = [LOW] * (WIDTH - SMOOTHNESS // 2)
for bit in keybits:
    for i in range(SMOOTHNESS):
        trace.append(LOW + (i + 1) * (MEDIUM - LOW) // SMOOTHNESS)
    trace += [MEDIUM] * (WIDTH - SMOOTHNESS)
    
    if bit == "1":
        for i in range(SMOOTHNESS):
            trace.append(MEDIUM + (i + 1) * (HIGH - MEDIUM) // SMOOTHNESS)
        trace += [HIGH] * (WIDTH - SMOOTHNESS)
        for i in range(SMOOTHNESS):
            trace.append(LOW + (SMOOTHNESS - i) * (HIGH - LOW) // SMOOTHNESS)
    else:
        for i in range(SMOOTHNESS):
            trace.append(LOW + (SMOOTHNESS - i) * (MEDIUM - LOW) // SMOOTHNESS)

    trace += [LOW] * (WIDTH - SMOOTHNESS)


noise = np.random.normal(0, 8, len(trace))

trace += noise

plt.plot(trace[:5000])
plt.show()

with open("trace.npy", "wb") as f:
    np.save(f, trace)
