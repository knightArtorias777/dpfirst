from dataclasses import dataclass
from DrissionPage import Chromium, ChromiumOptions
from DrissionPage._elements.none_element import NoneElement
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
    if clickobj.click():
        print("点击成功")
        # time.sleep(1)
        # 定位弹窗
        popup = browser.ele('@@tag()=div@@class=ql-editor')
        if popup:
            print("找到弹窗")
            download_pic(popup, browser, path_dir)
            text = html2text.html2text(popup.html)
            path = os.path.join(path_dir, "1", "Demand")
            # 处理文本内容
            md_file_path = os.path.join(path, f"{info.id}_{info.name}.md")
            with open(md_file_path, "w", encoding="utf-8") as file:
                file.write(text)
            print(f"Markdown 文件已创建：{md_file_path}")
            # 获取弹窗的文本内容
            # text = popup.html
            print("弹窗文本内容：", text)
        close = browser.ele('@@tag()=div@@class=icon-close btn-24px circle-button center-height ng-star-inserted')
        if close:
            print("找到关闭按钮")
            close.click()
            print("关闭弹窗成功")
        else:
            print("未找到关闭按钮,手动操作")

"""
tableStruct:useClass
class="devui-table devui-table-sm table-hover"
    scrollele:useClass
    div class="cdk-virtual-scroll-content-wrapper"

    onestripStruct:useStyle
    style=font-weight: normal; vertical-align: middle;

        IDinfo:useClass
        <a>class=link devui-table-link ng-star-inserted</a>

        ClickObj:useClass
        class=subject-field-title flex-1-row-overflow devui-table-link devui-table-title cursor-pointer

"""


def scroll_in_segments(scroll_viewport, REACHED_BOTTOM, segments=10):

    for i in range(segments):
        print(f"滚动操作第 {i+1} 次")
        try:
            scroll_viewport.scroll.down(400)
        except Exception as e:
            print(f"滚动失败: {e}")
            break
        time.sleep(0.1)
        if i == segments:
            REACHED_BOTTOM = True
        yield REACHED_BOTTOM



# datacontext={
#     "id":"-1"
# }
def main():
    co = ChromiumOptions()
    co.set_local_port(9222)

    # 确保下载路径存在并配置正确
    # download_path = r'/Users/haveanicedayi/Python/work/crawler_hd/download'
    # os.makedirs(download_path, exist_ok=True)
    # co.set_download_path(download_path)
    # print(f"下载路径设置为: {download_path}")

    #co.set_browser_path(r'/Applications/Arc.app')
    browser = Chromium(co).latest_tab

    browser.get(url="https://hd.devcloud.huaweicloud.com/projectman/scrum/7faaa4876bb64548904ef58bb6ee12bf/workitem/list")
    # 添加等待时间，确保页面完全加载
    time.sleep(1)

    # 使用绝对路径替代相对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    path_dir = os.path.join(base_dir, 'backup')
    print(f"备份路径设置为: {path_dir}")

    corearg = Info(id="-1", name="init")
    # process_items = set()

    REACHED_BOTTOM = False
    NO_NEW_ITEMS = False
    # 获取滚动视口
    scroll_viewport = browser.ele('@@id=data-table-virtual-tree-scroll')
    if scroll_viewport is None and isinstance(scroll_in_segments, NoneElement):
        print("未找到滚动视口元素")
        return
    
    
    print("find table over")
    while not (REACHED_BOTTOM and NO_NEW_ITEMS):
        # 定位table
        eletable = browser.ele('@@tag()=table@@class=devui-table devui-table-sm table-hover') 
        if eletable is None and isinstance(eletable, NoneElement):
            print("未找到表格元素")
            break
        gen = scroll_in_segments(scroll_viewport, REACHED_BOTTOM)

        # 定位table的下一条数据 todo:有一个坑在这里 你得需要解决第一个元素的问题
        if not corearg.id == "-1" or not corearg.name == "init":
            onestrip = eletable.ele('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;').next()
        else:
            onestrip = eletable.ele('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;')

        if onestrip is None and isinstance(onestrip, NoneElement):
            print("没有下一个元素了")
            if REACHED_BOTTOM:
                print("已到达底部，且没有新元素")
                NO_NEW_ITEMS = True
                continue
            else:
                # 变化REATHED_BOTTOM的状态
                try:
                    next(gen)
                except StopIteration:
                    print("滚动操作已完成")
                    continue
                except Exception as e:
                    print(f"滚动操作失败: {e}")
                    break


        # # 获取id信息
        onestripid = onestrip.ele('@@tag()=a@@class=link devui-table-link ng-star-inserted')
        if onestripid is None and isinstance(onestrip, NoneElement):
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







