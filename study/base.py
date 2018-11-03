# 基本的python能力
# 0. 对象，类，方法的操作
# 1. 数组的操作能力，包括打印创建数组，组合数组，多数组操作
# 2. 文件的操作能力
# 3. 数据库的操作能力
# 4. 线程/进程的能力
# 5. 类/对象/包的操作
# 6. 使用第三方模块的能力
# 7. 使用开源框架的能力
# 8. web开发能力
# 9. 算法转化能力
import json

if __name__ == '__main__':
    # print("Hello world!")

    arr = ['id', 'name']
    data = [{'Michael': 95, 'Bob': 75, 'Tracy': 85, 'id': 1, 'name': 30}]

    # 获取ID和名称
    id = data[0]['id']
    name = data[0]['name']

    # 复制一个数组，然后向后追加
    copyData = data[0]

    data.append(copyData)

    # 解析json的数据
    # jsonData = json.loads(data.)

    print(jsonData)
