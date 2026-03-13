# =============================
# 预测指标
# =============================

FEATURE_COLUMNS = [
    "cpu_usage",
    "response_time",
    "memory_usage",
    "disk_usage",
    "io_read",
    "io_write",
    "service_rt",
    "service_qps"
]

# =============================
# LSTM参数
# =============================

SEQ_LENGTH = 30        # 输入窗口
PRED_LENGTH = 1        # 预测步长

INPUT_SIZE = 8
HIDDEN_SIZE = 64
NUM_LAYERS = 2

BATCH_SIZE = 64
EPOCHS = 15
LR = 0.001

# =============================
# 分批训练参数
# =============================

SERVER_BATCH_SIZE = 2   # 每次训练几个服务器

# =============================
# 路径
# =============================

MODEL_DIR = "outputs/models/"
PREDICT_DIR = "../../results"
DATA_PATH = "../../data_generator/metrics.db"
