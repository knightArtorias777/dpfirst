# 基于状态的滚动处理框架
def process_all_items_with_state():
    # 状态变量：用于记录已处理的最后一个元素的ID和名称
    last_processed = Info(id="-1", name="init")
    
    # 已处理元素的唯一标识集合，用于避免重复处理
    processed_items = set()
    
    # 结束条件：达到底部且没有新元素
    reached_bottom = False
    no_new_items = False
    
    # 获取滚动视口
    scroll_viewport = browser.ele('@@id=data-table-virtual-tree-scroll')
    if not scroll_viewport:
        print("未找到滚动视口元素")
        return
    
    while not (reached_bottom and no_new_items):
        # 获取表格和当前所有可见的行元素
        eletable = browser.ele('@@tag()=table@@class=devui-table devui-table-sm table-hover')
        if not eletable:
            print("未找到表格元素")
            break
            
        all_rows = eletable.eles('@@tag()=tr@@style=font-weight: normal; vertical-align: middle;')
        if not all_rows:
            print("未找到行元素")
            
            # 检查是否已经滚动到底部
            scroll_height = browser.execute('return document.getElementById("data-table-virtual-tree-scroll").scrollHeight')
            scroll_top = browser.execute('return document.getElementById("data-table-virtual-tree-scroll").scrollTop')
            client_height = browser.execute('return document.getElementById("data-table-virtual-tree-scroll").clientHeight')
            
            if scroll_top + client_height >= scroll_height - 5:
                print("已到达底部，且没有新元素")
                reached_bottom = True
                no_new_items = True
                break
            else:
                # 未到底部，继续滚动
                scroll_viewport.scroll.down(400)
                time.sleep(1.5)
                continue
        
        print(f"当前页面发现 {len(all_rows)} 个元素")
        found_new_items = False
        
        # 寻找上次处理的最后一个元素之后的新元素
        for row in all_rows:
            try:
                # 获取当前行的ID和标题
                id_ele = row.ele('@@tag()=a@@class=link devui-table-link ng-star-inserted')
                title_ele = row.ele('@@tag()=span@@class=subject-field-title flex-1-row-overflow devui-table-link devui-table-title cursor-pointer')
                
                if not id_ele or not title_ele:
                    continue
                    
                current_id = id_ele.text
                current_title = title_ele.text
                item_key = f"{current_id}_{current_title}"
                
                # 跳过已处理的元素
                if item_key in processed_items:
                    print(f"跳过已处理的元素: ID={current_id}, 标题={current_title}")
                    continue
                
                # 如果是第一次运行或者找到了上次处理的元素之后的元素
                if last_processed.id == "-1" or found_last_element:
                    print(f"处理新元素: ID={current_id}, 标题={current_title}")
                    
                    # 处理当前元素
                    current_info = Info(id=current_id, name=current_title)
                    corebackup(title_ele, current_info)
                    
                    # 记录已处理状态
                    processed_items.add(item_key)
                    last_processed = current_info
                    found_new_items = True
                
                # 检查是否找到了上次处理的最后一个元素
                elif current_id == last_processed.id and current_title == last_processed.name:
                    print(f"找到上次处理的最后一个元素: ID={current_id}, 标题={current_title}")
                    found_last_element = True
            
            except Exception as e:
                print(f"处理元素时出错: {e}")
        
        # 检查是否已经滚动到底部
        scroll_height = browser.execute('return document.getElementById("data-table-virtual-tree-scroll").scrollHeight')
        scroll_top = browser.execute('return document.getElementById("data-table-virtual-tree-scroll").scrollTop')
        client_height = browser.execute('return document.getElementById("data-table-virtual-tree-scroll").clientHeight')
        
        if scroll_top + client_height >= scroll_height - 5:
            print("已到达底部")
            reached_bottom = True
            
            # 如果到达底部且没有发现新元素，则结束循环
            if not found_new_items:
                print("到达底部且没有新元素，结束处理")
                no_new_items = True
                break
        
        # 如果没有发现新元素且未到底部，则继续滚动
        if not found_new_items and not reached_bottom:
            print("没有发现新元素，继续滚动")
            scroll_viewport.scroll.down(400)
            time.sleep(1.5)
    
    print(f"总共处理了 {len(processed_items)} 个元素")
    print("所有元素处理完成")