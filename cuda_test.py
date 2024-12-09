import tensorflow as tf

# Check for available GPUs
print("Num GPUs Available:", len(tf.config.list_physical_devices('GPU')))

# Verify TensorFlow is using GPU
print("Is TensorFlow using GPU:", tf.test.is_gpu_available())
