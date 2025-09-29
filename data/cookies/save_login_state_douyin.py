# save_login_state.py (修改版，在当前目录下保存)

from playwright.sync_api import sync_playwright


def save_state():
    with sync_playwright() as p:
        # 启动一个可见的浏览器，以便你手动操作
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("请在打开的浏览器窗口中手动登录抖音，然后脚本将自动保存状态...")
        # page.goto("https://creator.douyin.com/")
        page.goto(
            "https://creator.xiaohongshu.com/publish/publish?source=official&from=menu&target=video"
        )
        try:
            # 等待URL变化，表示登录成功。我们等待URL包含 'creator-micro'
            # page.wait_for_url(
            #     "https://creator.douyin.com/creator-micro/*", timeout=600000
            # )  # 等待10分钟
            # 小红书
            page.wait_for_url(
                re.compile(r"https://creator\.xiaohongshu\.com/.*"), timeout=600000
            )

            # 关键改动：将路径改为当前目录下的文件名
            storage_path = "xiaohongshu_login_state.json"

            context.storage_state(path=storage_path)

            print(f"登录状态已成功保存到 {storage_path}")
        except Exception as e:
            print(f"登录超时或失败: {e}")
            print("请确保你手动完成了登录，并且页面跳转到了正确的URL。")

        browser.close()


if __name__ == "__main__":
    save_state()
