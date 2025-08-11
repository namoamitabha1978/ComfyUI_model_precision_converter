from .ComfyUI_model_precision_converter import ModelPrecisionConverter
from .ComfyUI_model_precision_checker import ModelPrecisionChecker

# 注册节点
NODE_CLASS_MAPPINGS = {
    "ModelPrecisionChecker": ModelPrecisionChecker,
    "ModelPrecisionConverter": ModelPrecisionConverter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModelPrecisionChecker": "模型精度检测",
    "ModelPrecisionConverter": "模型精度转换与修复工具"
}
    

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']