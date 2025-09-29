from playwright.sync_api import sync_playwright
import re
import time


def save_login_state():
    with sync_playwright() as p:
        # 打开 Chromium 可视化浏览器
        browser = p.chromium.launch(headless=False)
        # 创建上下文，可设置 viewport
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        print("请在浏览器中手动登录小红书账号...")
        # 打开小红书创作者后台上传页面
        page.goto(
            "https://creator.xiaohongshu.com/publish/publish?source=official&from=menu&target=video"
        )
        time.sleep(10)  # 等待页面加载
        try:
            # ✅ 等待登录成功后跳转到页面（用正则匹配 URL）
            page.wait_for_url(
                re.compile(r"https://creator\.xiaohongshu\.com/.*"), timeout=600000
            )
            print("检测到登录成功！正在保存登录状态...")

            # 保存状态到 json 文件
            storage_path = "xiaohongshu_login_state.json"
            context.storage_state(path=storage_path)
            print(f"✔ 登录状态已保存到 {storage_path}")

        except Exception as e:
            print(f"❌ 登录超时或失败: {e}")
            print("请确保你手动完成了登录，并跳转到正确的页面。")

        finally:
            browser.close()


if __name__ == "__main__":
    save_login_state()
