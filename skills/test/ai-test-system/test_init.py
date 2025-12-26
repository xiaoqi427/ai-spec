"""测试 ai_test_system 包的导入功能"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_package_import():
    """测试包是否可以正常导入"""
    try:
        import ai_test_system
        print("✓ ai_test_system 包导入成功")
        return True
    except ImportError as e:
        print(f"✗ ai_test_system 包导入失败: {e}")
        return False


def test_module_imports():
    """测试包内各模块是否可以正常导入"""
    modules = [
        "ai_test_system.main",
        "ai_test_system.config_loader",
        "ai_test_system.pipeline",
        "ai_test_system.case_model",
        "ai_test_system.excel_io",
        "ai_test_system.image_marker",
        "ai_test_system.locator_service",
        "ai_test_system.screenshot_captor",
        "ai_test_system.vision_model_client",
    ]
    
    results = []
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name} 导入成功")
            results.append(True)
        except Exception as e:
            print(f"✗ {module_name} 导入失败: {e}")
            results.append(False)
    
    return all(results)


def test_main_function():
    """测试 main 函数是否存在"""
    try:
        from ai_test_system.main import main
        print("✓ main 函数可访问")
        return True
    except Exception as e:
        print(f"✗ main 函数访问失败: {e}")
        return False


def test_config_loader():
    """测试配置加载器的基本功能"""
    try:
        from ai_test_system.config_loader import (
            AppConfig,
            ExcelConfig,
            ScreenshotConfig,
            VisionModelConfig,
            MarkConfig,
            LogConfig,
        )
        print("✓ 配置类导入成功")
        
        # 测试创建配置对象
        excel_cfg = ExcelConfig(
            input_path="test.xlsx",
            sheet_name="Sheet1",
            case_id_column="CaseID",
            description_column="Description",
            system_url_column="SystemURL",
            extra_context_column="ExtraContext",
            output_image_column="ScreenshotPath",
        )
        print("✓ ExcelConfig 实例化成功")
        return True
    except Exception as e:
        print(f"✗ 配置加载器测试失败: {e}")
        return False


def test_pipeline():
    """测试 Pipeline 类是否可以导入"""
    try:
        from ai_test_system.pipeline import AiTestPipeline
        print("✓ AiTestPipeline 类导入成功")
        return True
    except Exception as e:
        print(f"✗ AiTestPipeline 类导入失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("开始测试 ai_test_system 包")
    print("=" * 60)
    
    test_results = []
    
    print("\n1. 测试包导入")
    print("-" * 60)
    test_results.append(test_package_import())
    
    print("\n2. 测试模块导入")
    print("-" * 60)
    test_results.append(test_module_imports())
    
    print("\n3. 测试 main 函数")
    print("-" * 60)
    test_results.append(test_main_function())
    
    print("\n4. 测试配置加载器")
    print("-" * 60)
    test_results.append(test_config_loader())
    
    print("\n5. 测试 Pipeline")
    print("-" * 60)
    test_results.append(test_pipeline())
    
    print("\n" + "=" * 60)
    passed = sum(test_results)
    total = len(test_results)
    print(f"测试完成: {passed}/{total} 通过")
    print("=" * 60)
    
    sys.exit(0 if all(test_results) else 1)
