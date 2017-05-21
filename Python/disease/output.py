'''Output the result of Frequent ItemSet'''
from llh.Python.disease.mining import RESULT_DICT
from llh.Python.disease.arrange import ARRANGE_LIST
L_DICT = {'雲林縣': 'Yunlin County', '澎湖縣': 'Penghu County', '新北市': 'New Taipei City',
          '屏東縣': 'Pingtung County', '台中市': 'Taichung City', '台北市': 'Taipei City',
          '台南市': 'Tainan City', '桃園市': 'Taoyuan City', '台東縣': 'Taitung County',
          '宜蘭縣': 'Yilan County ', '彰化縣': 'Changhua County', '新竹縣': 'Hsinchu County',
          '南投縣': 'Nantou County', '連江縣': 'Lienchiang County', '花蓮縣': 'Hualien County',
          '金門縣': 'Kinmen County ', '基隆市': 'Keelung City', '高雄市': 'Kaohsiung City',
          '嘉義縣': 'Chiayi County ', '苗栗縣': 'Miaoli County', '嘉義市': 'Chiayi City',
          '新竹市': 'Hsinchu City'}

with open('FrequentItemSet.csv', 'w', newline='', encoding='utf-8') as file:
    for member in RESULT_DICT:
        line = str()
        for name in member:
            line += str(name) + ','
        line += str(RESULT_DICT[member][0]) + ','
        line += str(RESULT_DICT[member][1])
        print(line)
        file.write(line)


with open('ArrangeList.csv', 'w') as file:
    for member in ARRANGE_LIST:
        line = str()
        for name in member.keys():
            line += L_DICT[str(name)] + ','
        line = line[:-1] + '\n'
        file.write(line)
