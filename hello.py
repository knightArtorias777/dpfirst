from dataclasses import dataclass
from DrissionPage import Chromium, ChromiumOptions
from DrissionPage._elements.none_element import NoneElement
from DrissionPage.errors import *
from DrissionPage.common import Settings

# from DrissionPage.common import Keys
import time
import html2text
import os


@dataclass
class Info:
    id: str
    name: str

# 打开弹窗进行数据备份核心逻辑
def download_pic(popup, browser=None, path_dir=None):
    pic_list = popup.eles('@tag()=img')
    # if not pic_list:
    #     pic_list = popup.eles('@tag()=div@@data-image')
    if pic_list: 
        for ele in pic_list:
            download_link = ele.link
            print(ele.link)
            path_segments = download_link.split('/')[3:-1]
            save_path = os.path.join(path_dir, *path_segments)
            
            # 修复目录创建逻辑
            try:
                os.makedirs(save_path, exist_ok=True)
                print(f"保存路径: {save_path}")
            except Exception as e:
                print(f"创建目录失败: {e}")
                continue
            
            save_name = download_link.split('/')[-1]
            
            browser.download(file_url=download_link,
                             save_path=save_path,
                             rename=save_name,
                             file_exists='skip')
            
            print("save_path", save_path)
            print("save_name", save_name)
            # browser.download(download_link, pic_dir)
            
    else:
        print("没有找到图片元素")
    

def corebackup(clickobj,info:Info,browser=None,path_dir=None):
    if clickobj is None and isinstance(clickobj, NoneElement):
        print("没有找到点击对象")
        return 
    if clickobj.click():
        print("点击成功")
        # 增加等待时间，确保弹窗完全加载
        time.sleep(0.5)
        # 定位弹窗
        popup = browser.ele('@@tag()=div@@class=ql-editor')
        if popup is None and isinstance(popup, NoneElement):
            print("没有找到弹窗元素")
        if popup:
            print("找到弹窗")
            download_pic(popup, browser, path_dir)
            text = html2text.html2text(popup.html)
            path = os.path.join(path_dir, "1", "Demand")
            # 确保路径存在
            os.makedirs(path, exist_ok=True)
            # 处理文本内容
            modified_name = info.name.replace(" ", "_").replace("/", "_")
            md_file_path = os.path.join(path, f"{info.id}_{modified_name}.md")
            with open(md_file_path, "w", encoding="utf-8") as file:
                file.write(text)
            print(f"Markdown 文件已创建：{md_file_path}")
            # 获取弹窗的文本内容
            # text = popup.html
            print("弹窗文本内容：", text)
            time.sleep(0.5)
        
            # 方法1：直接查找并点击关闭按钮

            print("尝试点击关闭按钮")
            # close = browser.ele('@@tag()=div@@class=icon-close btn-24px circle-button center-height ng-star-inserted')
            close = browser.ele('xpath://html/body/d-drawer/div/div/div[2]/div[1]/scrum-task-detail/div/div[1]/div[1]/div[3]/div/div[4]/div[2]')
            if close is None and isinstance(close, NoneElement):
                print("没有找到关闭按钮")
                return
            else:
                print("找到关闭按钮")
                try:
                    close.click()
                    time.sleep(0.5)  # 给点击操作一些时间执行
                    print("关闭弹窗成功")
                except ElementLostError:
                    print("关闭按钮在点击过程中失效，尝试其他方法")
                except Exception as e:
                    print(f"点击关闭按钮时发生错误: {e}")

            
        # try:
        #     print("尝试按ESC键关闭弹窗")
        #     browser.actions.key_down('Escape')  # 按下ESC键
        #     time.sleep(0.1)
        #     browser.actions.key_up('Escape')  # 松开ESC键
        #     time.sleep(0.5)  # 等待弹窗关闭
        #     print("按ESC键关闭弹窗成功")
            
        # except Exception as key_e:
        #     print(f"按ESC键失败: {key_e}")
            
        

"""
tableStruct:useClass
class="devui-table devui-table-sm table-hover"
    scrollele:useClass
    div class="cdk-virtual-scroll-content-wrapper"

    onestripStruct:useStyle
    style=font-weight: normal; vertical-align: middle;

        IDinfo:useClass
        aclass=link devui-table-link ng-star-inserted</a>

        ClickObj:useClass
        class=subject-field-title flex-1-row-overflow devui-table-link devui-table-title cursor-pointer

"""

# generator函数，分段滚动
# def scroll_in_segments(scroll_viewport, REACHED_BOTTOM, segments=10):

#     for i in range(segments):
#         print(f"滚动操作第 {i+1} 次")
#         try:
#             scroll_viewport.scroll.down(400)
#         except Exception as e:
#             print(f"滚动失败: {e}")
#             break
#         time.sleep(0.5)
#         if i == segments - 1:
#             REACHED_BOTTOM = True
#         yield REACHED_BOTTOM

# def get_onestrip(eletable,corearg:Info):
    
#     while True:
#         # 定位table的下一条数据 todo:有一个坑在这里 你得需要解决第一个元素的问题
#         if not corearg.id == "-1" or not corearg.name == "init":
#             onestrip = eletable.ele('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;').next()
#         else:
#             onestrip = eletable.ele('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;')

#         onestrip = eletable.ele('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;').next()
#         if onestrip is None and isinstance(onestrip, NoneElement):
#             print("没有下一个元素了")
#             break
#         else:
#             yield onestrip

# datacontext={
#     "id":"-1"
# }
def main():
    Settings.set_raise_when_ele_not_found(True)
    co = ChromiumOptions()
    co.set_local_port(9222)

    # 确保下载路径存在并配置正确
    # download_path = r'/Users/haveanicedayi/Python/work/crawler_hd/download'
    # os.makedirs(download_path, exist_ok=True)
    # co.set_download_path(download_path)
    # print(f"下载路径设置为: {download_path}")

    #co.set_browser_path(r'/Applications/Arc.app')
    browser = Chromium(co).latest_tab

    browser.get(url="https://hd.devcloud.huaweicloud.com/projectman/scrum/c5c40d898d4f477fa97bcae10a49f8d5/workitem/list")
    # 添加等待时间，确保页面完全加载
    time.sleep(3)
    input("请手动登录后按回车继续...")
    # 使用绝对路径替代相对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    path_dir = os.path.join(base_dir, 'backup')
    print(f"备份路径设置为: {path_dir}")

    corearg = Info(id="-1", name="init")
    # process_items = set()

    REACHED_BOTTOM = False
    NO_NEW_ITEMS = False
    # 创建一个滚动控制器
    scroll_counter = 0
    max_scrolls = 10  # 滚动次数上限
    # 获取滚动视口
    scroll_viewport = browser.ele('@@id=data-table-virtual-tree-scroll')
    if scroll_viewport is None and isinstance(scroll_in_segments, NoneElement):
        print("未找到滚动视口元素")
        return
    # 定位table
    eletable = browser.ele('@@tag()=table@@class=devui-table devui-table-sm table-hover') 
    if eletable is None and isinstance(eletable, NoneElement):
        print("未找到表格元素")
        return 
    print("find table over")
    while not (REACHED_BOTTOM and NO_NEW_ITEMS):
        try:
        # gen = scroll_in_segments(scroll_viewport, REACHED_BOTTOM)

        # 定位table的下一条数据 todo:有一个坑在这里 你得需要解决第一个元素的问题
            if not corearg.id == "-1" or not corearg.name == "init":
                # onestrip = eletable.ele('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;').next()
                try:
                    onestrip = eletable.ele(f'@@tag()=a@@class=link devui-table-link ng-star-inserted@@text()={corearg.id}').parent('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;').next()
                    print("onestrip", onestrip)
                except ElementNotFoundError:
                    print("没有找到元素，尝试滚动")
                    # if onestrip is None and isinstance(onestrip, NoneElement):
                    # print("没有下一个元素了")
                    if REACHED_BOTTOM:
                        print("已到达底部，且没有新元素")
                        NO_NEW_ITEMS = True
                        continue
                    
                        # 变化REATHED_BOTTOM的状态
                        # try:
                        #     next(gen)
                        # except StopIteration:
                        #     print("滚动操作已完成")
                        #     continue
                        # except Exception as e:
                        #     print(f"滚动操作失败: {e}")
                        #     break
                    print(f"滚动操作第 {scroll_counter + 1} 次")
                    try:
                        scroll_viewport.scroll.down(400)
                        scroll_counter += 1
                        time.sleep(0.5)  # 给页面加载时间
                        
                        # 检查是否达到最大滚动次数
                        if scroll_counter >= max_scrolls:
                            print(f"已达到最大滚动次数 {max_scrolls}，标记为已到底部")
                            REACHED_BOTTOM = True
                        continue
                    except Exception as e:
                            print(f"滚动失败: {e}")
                            REACHED_BOTTOM = True  # 滚动失败也视为到达底部
            else:
                onestrip = eletable.ele('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;')



            # # 获取id信息
            onestripid = onestrip.ele('@@tag()=a@@class=link devui-table-link ng-star-inserted')
            if onestripid is None and isinstance(onestripid, NoneElement):
                print("没有找到ID元素")
                break
            # print(idinfo.text)
            # # 主要点击操作对象
            clickobj = onestrip.ele('@@tag()=span@@class=subject-field-title flex-1-row-overflow devui-table-link devui-table-title cursor-pointer')
            if clickobj is None and isinstance(clickobj, NoneElement):
                print("没有找到点击对象")
                break
            # corearg = Info(id=onestripid.text, name=clickobj.text)
            # 更新对象
            corearg.id = onestripid.text
            corearg.name = clickobj.text
            print("find clickobj over", corearg.id, corearg.name)
            corebackup(clickobj, corearg, browser, path_dir)
            time.sleep(0.5)
        
        except Exception as e:
            print(f"发生错误: {e}")
            # 处理异常情况
            # 可以选择继续滚动或退出循环
            time.sleep(1)
        # 找到可滚动的虚拟滚动视口元素

        # if scroll_viewport is None:
        #     # 备用选择器，尝试通过类名找到
        #     scroll_viewport = browser.ele('@@tag()=cdk-virtual-scroll-viewport')
            
        # if scroll_viewport:
        #     print("找到滚动元素")
            
        #     # 打印滚动元素的属性
        #     print(f"滚动元素高度: {scroll_viewport.attr('style')}")
        #     print(f"滚动元素ID: {scroll_viewport.attr('id')}")
            
        #     # 也可以使用DrissionPage的方法进行滚动
        #     print("使用DrissionPage方法滚动")
        #     # scroll_viewport.scroll.to_bottom()
        #     # time.sleep(1)
            
        #     # scroll_viewport.scroll.to_top()
        #     # time.sleep(1)
            
        #     # 滚动特定像素
        #     scroll_viewport.scroll.down(400)
        #     time.sleep(1)
        #     #400 完美向下翻动10行
        #     print("向下滚动400像素")
        # else:
        #     print("未找到滚动元素，请检查页面结构")




if __name__ == "__main__":
    # 运行主函数
    main()







