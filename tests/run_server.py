from flask import Flask
import subprocess
import threading
import os
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 定义要删除的文件的完整路径
FILES_TO_DELETE = [
    r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\video.mp4",
    r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\image.jpg",
    r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\replan.txt",
]


def delete_file_with_retry(filepath, max_retries=5, delay=2):
    """
    尝试删除文件，如果失败则重试
    :param filepath: 文件路径
    :param max_retries: 最大重试次数
    :param delay: 每次重试间隔（秒）
    """
    if not os.path.exists(filepath):
        logger.info(f"⚠ 文件不存在，跳过删除: {filepath}")
        return True

    for attempt in range(max_retries):
        try:
            os.remove(filepath)
            logger.info(f"✅ 文件已删除: {filepath}")
            return True
        except PermissionError:
            logger.warning(
                f"⚠ 文件被占用，第 {attempt + 1}/{max_retries} 次重试... {filepath}"
            )
            time.sleep(delay)
        except Exception as e:
            logger.error(f"❌ 删除文件失败: {filepath}. 错误: {e}")
            return False

    logger.error(f"❌ 删除文件失败（已重试{max_retries}次）: {filepath}")
    return False


def run_tests():
    """执行 pytest 并清理文件"""
    try:
        logger.info("=" * 60)
        logger.info("🚀 开始执行 pytest tests...")
        logger.info("=" * 60)

        # 1. 执行 pytest，等待完成
        result = subprocess.run(
            ["pytest", "tests", "-v"],  # -v 显示详细输出
            capture_output=True,
            text=True,
            timeout=600,  # 10分钟超时
        )

        # 打印 pytest 输出
        logger.info("📋 pytest 标准输出:")
        logger.info(result.stdout)

        if result.returncode != 0:
            logger.error("📋 pytest 错误输出:")
            logger.error(result.stderr)

        logger.info("=" * 60)
        logger.info(f"✅ pytest 执行完毕 (返回码: {result.returncode})")
        logger.info("=" * 60)

        # 2. 等待一段时间，确保所有文件句柄都已释放
        logger.info("⏳ 等待 3 秒，确保文件句柄释放...")
        time.sleep(3)

        # 3. 开始清理文件
        logger.info("=" * 60)
        logger.info("🧹 开始清理文件...")
        logger.info("=" * 60)

        success_count = 0
        fail_count = 0

        for filepath in FILES_TO_DELETE:
            if delete_file_with_retry(filepath):
                success_count += 1
            else:
                fail_count += 1

        logger.info("=" * 60)
        logger.info(f"🏁 文件清理完毕: 成功 {success_count} 个，失败 {fail_count} 个")
        logger.info("=" * 60)

    except subprocess.TimeoutExpired:
        logger.error("❌ pytest 执行超时！")
    except Exception as e:
        logger.error(f"❌ 执行过程发生错误: {e}", exc_info=True)


@app.route("/run-tests", methods=["POST"])
def trigger_tests():
    """触发 pytest 测试和文件清理"""
    logger.info("=" * 60)
    logger.info("📨 收到测试触发请求")
    logger.info("=" * 60)

    # 用线程异步执行，避免阻塞 Flask
    thread = threading.Thread(target=run_tests, daemon=True)
    thread.start()

    return {
        "status": "success",
        "message": "全自动上传任务已启动，请查看控制台日志",
    }, 200


@app.route("/health", methods=["GET"])
def health_check():
    """健康检查端点"""
    return {"status": "ok", "service": "pytest-runner"}, 200


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🌐 Flask 服务启动中...")
    logger.info("📍 监听端口: 5001")
    logger.info("📍 触发测试: POST http://127.0.0.1:5001/run-tests")
    logger.info("📍 健康检查: GET http://127.0.0.1:5001/health")
    logger.info("=" * 60)
    app.run(port=5001, debug=False)  # 生产环境建议 debug=False
