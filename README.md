# 贴吧评论爬虫
## 可以大量爬取指定吧下的大量帖子的评论

## 1
![image](https://github.com/user-attachments/assets/41186ff1-7708-4eb7-a9ca-123497a4f8b3)
首先需要修改get_main函数下的url的值中的kw字段后的对应的吧的名字，具体操作就是在对应吧的首页将链接复制粘贴下来，将kw值替换掉url中的kw值

## 2
![image](https://github.com/user-attachments/assets/052e9a32-6f58-407d-84d8-2a5e422e023d)
分别将get_one和get_page函数中的url值中的t值替换为对应吧的帖子的评论包的请求参数中的t值

