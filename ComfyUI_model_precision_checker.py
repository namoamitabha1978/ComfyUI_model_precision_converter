import torch
import os
import folder_paths
from safetensors.torch import load_file as load_safetensors
from comfy.utils import load_torch_file

class ModelPrecisionChecker:
    """模型精度检测节点，用于分析模型的精度类型和参数分布"""
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_path": ("STRING", {
                    "default": "", 
                    "placeholder": "输入模型路径",
                    "forceInput": True  # 允许文件选择器输入
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("检测结果",)
    FUNCTION = "check_precision"
    CATEGORY = "模型工具/精度检测"
    
    def check_precision(self, model_path):
        if not model_path or not os.path.exists(model_path):
            return ("错误：模型路径不存在",)
        
        # 加载模型
        try:
            model = self._load_model(model_path)
        except Exception as e:
            return (f"加载失败：{str(e)}",)
        
        # 分析精度
        result = []
        dtype_counts = {}
        tensor_count = 0
        
        for name, tensor in model.items():
            if isinstance(tensor, torch.Tensor):
                tensor_count += 1
                dtype = str(tensor.dtype)
                dtype_counts[dtype] = dtype_counts.get(dtype, 0) + 1
                result.append(f"参数 {name}: {dtype}")
            elif isinstance(tensor, dict) and "dtype" in tensor:
                # 处理量化模型格式
                tensor_count += 1
                dtype = tensor["dtype"]
                dtype_counts[dtype] = dtype_counts.get(dtype, 0) + 1
                result.append(f"参数 {name}: 量化格式 {dtype}")
        
        # 汇总结果
        summary = [
            f"模型路径: {model_path}",
            f"总参数数量: {tensor_count}",
            "精度分布:"
        ]
        for dtype, count in dtype_counts.items():
            summary.append(f"- {dtype}: {count} 个参数 ({count/tensor_count*100:.1f}%)")
        
        return ("\n".join(summary + result),)
    
    def _load_model(self, model_path):
        """加载模型文件（支持多种格式）"""
        ext = os.path.splitext(model_path)[1].lower()
        if ext == ".safetensors":
            return load_safetensors(model_path, device="cpu")
        elif ext in [".ckpt", ".pt"]:
            return torch.load(model_path, map_location="cpu", weights_only=True)
        else:
            return load_torch_file(model_path)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "ModelPrecisionChecker": ModelPrecisionChecker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModelPrecisionChecker": "模型精度检测工具"
}
