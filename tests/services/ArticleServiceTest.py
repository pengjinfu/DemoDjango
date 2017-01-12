import unittest
import json
from article.services import ArticleServices
#from article.models import Article

class ArticleServiceTest(unittest.TestCase):
    def test_upper(self):
        self.assertTrue(True);

    # 可以连接FB的
    def testDetail(self):
        service = ArticleServices();
        data =  service.detail()
        #data = Article.test('aaa')
        #data = 'AAA'
        self.assertIsNotNone(data)



if __name__ == '__main__':
    unittest.main()