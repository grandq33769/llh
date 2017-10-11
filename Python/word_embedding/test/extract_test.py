'''
Module for testing method in extract.py
Date : 2017/10/02
'''
import unittest
import re
import llh.Python.word_embedding.extract as extract
from llh.Python.word_embedding.word2vec import Word2vecConverter


class TestDataProcessing(unittest.TestCase):
    '''
    Class for testing data processing
    '''

    def setUp(self):
        self.json = open(
            '/Users/lhleung/Documents/Data/Ptt/Gossiping/raw/test/Gossiping-23431-25000.json', 'r')
        self.content = '泰利又變胖 氣象局：周三、四影響最劇烈 今年第18號颱風泰利恐直撲台灣，根據中央氣象局今晚8時最新資料，\
        泰利七級風半徑從 100公里擴大為120公里。氣象局指出，估計明起泰利進入 成長爆發期 ，接近台灣時將是中 颱以上強度，\
        若移動速度與路徑不變，最快周二上午先發布海上警報、周二晚上發布陸上 警報，周三到周五受泰利影響，全台將有強風豪雨，\
        其中周三、四則是影響最劇烈時刻， 估中心從東半部登陸，但後續影響狀況仍有變數，請民眾注意氣象局最新天氣訊息。 \
        輕颱泰利今晚8時中心位置在鵝鑾鼻東南東方約1900公里海面上，以每小時27公里速度， 向西北西朝台灣陸地進逼，\
        強度和今天下午一樣，但暴風圈擴大為120公里，依照氣象局 潛勢路徑預報圖，中心估從恆春半島到台東一帶登陸。 \
        氣象局表示，由於未來所經海域較溫暖，垂直風切較小，估明起將進入快速成長期，接近 台灣將增強到中颱以上，\
        不排除達到強颱，暴風圈估將擴大到180公里，若移動速度與路 徑沒變化，估周二上午到下午發布海上警報，\
        周二晚上到周三凌晨晨發布陸上警報。 隨著泰利步步進逼，氣象局預估，周二深夜起東半部風雨開始轉趨明顯，\
        周三凌晨接著是 北部，周三白天各地風雨轉趨明顯，估周三下午暴風圈就會接觸陸地，颱風中心可能從東 半部登陸，\
        周三到周五受泰利影響，全台各地將有強風豪雨， 周三、四則是影響最劇烈， 請民眾做好防颱準備； 預計周六起風雨趨緩。\
        （許敏溶台北報導） 蘋果新聞 https://goo.gl/VuXSmm 鬼島老闆:勞工只想著颱風假 一點都沒有競爭力'

        self.converter = Word2vecConverter(
            '/Users/lhleung/Documents/Data/Word2vec/400_include_stopword/med400.model.bin')

    def tearDown(self):
        self.json.close()

    def test_read(self):
        '''
        Test case for reading .json and extract the content
        '''
        result = extract.process_article(self.json)
        self.assertTrue(all([re.match('[\u4e00-\u9fff]+', x) for x in result]))

    def test_converter(self):
        '''
        Test case for converter function
        '''
        # print(cut_s)
        cut, s_vec = self.converter.sen2vec('我是男生')
        print(cut, s_vec)
        self.assertEqual(len(s_vec), 3)

    def test_sen_index_vec(self):
        '''
        Test case for sen_index_vec() function
        Test for: array shape
        '''
        cut, _ = self.converter.sen2vec('我是男生')
        arr = self.converter.sen_index_vec(cut)
        self.assertEqual(arr.shape, (3, 955583))


if __name__ == '__main__':
    unittest.main()
