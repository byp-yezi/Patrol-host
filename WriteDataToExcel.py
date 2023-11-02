import xlwt
from xlwt import easyxf, Style
import datetime


class WriteDataToExcel(object):

    def __init__(self):
        # 定义不同列的阈值字典，可以根据需求修改
        self.thresholds = {
            0: 80,  # 第一列的阈值为80%
            1: 80,  # 第二列的阈值为80%
            2: 80,  # 第三列的阈值为80%
            3: 80,  # 第四列的阈值为80%
            4: 80,  # 第五列的阈值为80%
            # 添加更多列的阈值以及相应的阈值值
        }

    # 创建一个通用样式
    @staticmethod
    def create_style(font_color_index=57, background_color_index=1):
        # 定义并返回一个样式
        style = easyxf(
            # 设置字体样式
            'font: name 微软雅黑, colour_index {0}, height 240;'.format(font_color_index) +
            # 设置文本对齐方式
            'align: horz center, vert center, wrap on;' +
            # 设置边框样式
            'borders: left thin, right thin, top thin, bottom thin;' +
            # 设置背景颜色
            'pattern: pattern solid, fore_colour {0};'.format(background_color_index)
        )
        return style

    # 写入excel
    def write_data_to_excel(self, data_list):
        try:
            workbook = xlwt.Workbook()  # 创建一个新的Excel工作簿
            sheet = workbook.add_sheet("执行结果")  # 添加一个名为"执行结果"的工作表

            style = self.create_style()  # 创建通用样式
            style2 = self.create_style(background_color_index=Style.colour_map['yellow'])  # 修改背景颜色

            first_data = None  # 用于存储第一个非空数据描述
            for data in data_list:
                if data.desc:
                    first_data = data
                    break

            if first_data:
                # 写入表头
                sheet.write(0, 0, 'IP', style)  # 在第一行第一列写入'IP'，应用通用样式

                for i, desc in enumerate(first_data.desc):
                    sheet.write(0, i + 1, desc, style)  # 写入数据描述，应用通用样式
                    sheet.col(i).width = 22 * 256  # 设置列宽
                # 设置最后一列（数据列）的列宽
                sheet.col(len(first_data.desc)).width = 22 * 256  # 设置最后一列的列宽

            # 写入数据
            for i, data in enumerate(data_list):
                sheet.write(i + 1, 0, data.ip, style)  # 写入IP地址，应用通用样式
                for j, value in enumerate(data.data):
                    if j in self.thresholds and '%' in value:
                        if float(value.strip('%')) > self.thresholds[j]:
                            sheet.write(i + 1, j + 1, value, style2)  # 根据不同列的阈值写入数据
                        else:
                            sheet.write(i + 1, j + 1, value, style)
                    else:
                        sheet.write(i + 1, j + 1, value, style)

            # 获取当前日期和时间，并将其作为文件名的一部分
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"out_{current_datetime}.xls"

            workbook.save(file_name)  # 保存文件

        except Exception as e:
            print(f"An error occurred: {e}")
