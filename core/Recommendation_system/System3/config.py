import torch

# Device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Paths
DB_DIR = "db.sqlite3"
CHECKPOINT_PATH = "core/Recommendation_system/System3/checkpoints"

# Model Parameters
MODEL_NAME='Base Model'
INPUT_CHANNELS = 3
NUM_CLASSES = 10
LR = 1e-3
EMBEDDING_DIM=128
DROPOUT_PROB= 0.2
CHECKPOINT_FILE= 'core/Recommendation_system/System3/checkpoints/Base_Model_model_epoch20.pth'
# Training Hyperparameters
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001
WEIGHT_DECAY=0.1

# Logging
LOG_INTERVAL = 10
