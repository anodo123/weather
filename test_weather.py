import unittest
import weather as model
from unittest.mock import patch
from unittest import TestCase

class testweather(unittest.TestCase):
    global api_key
    api_key= '07405a909fc118b1af94a19d61c85463'
    def test_convert(self):
        self.assertEqual(model.convert(1643869800),'2022-02-03 12:00:00')
        self.assertEqual(model.convert(1643956200),'2022-02-04 12:00:00')
        self.assertEqual(model.convert(1644042600),'2022-02-05 12:00:00')
        self.assertEqual(model.convert(1644129000),'2022-02-06 12:00:00') 
        self.assertEqual(model.convert(1644215400),'2022-02-07 12:00:00')
    #testing latitude and longitude function
    l = [["'85.0' '27.5674'",api_key],["'85' '23.5'",api_key],["'25.0' '34.5674'",api_key],
        ["'123.5' '658.67'",api_key],["'844.0' '27.5674'",api_key],["'58.0' '5780.0'","1"]]
    for i in l:
        global temp,temp1,expected 
        temp= list(map(str,i[0].split()))
        temp1 = i[1]
        expected = ("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely&appid={}".format(temp[0],temp[1],temp1))
        @patch('builtins.input', side_effect=i)
        def test_latlong(self,side_effect):
            result = model.latlong()
            self.assertEqual(result,expected)
            
    #testing login function 
    l = [[1,1,2,'bahraich',api_key,'2022-02-04',5],['',''],['1','0',4],
        [1,1,0,2,'lucknow',api_key,'2022-02-04',5],[1,1,1,"26.8467 80.9462",api_key,'2022-02-04',5],[1,1,2,"bahraich",'lk']] 
    for i in l:    
        if(i!=l[len(l)-1]):
            @patch('builtins.input', side_effect=i)
            def test_login(self,mock_inputs):
                result = model.login()
                self.assertEqual(result,None)
        else:
            @patch('builtins.input', side_effect=i)
            def test_login(self,mock_inputs):
                with self.assertRaises(SystemExit):
                    result = model.login()
    #testing create user function
    l = [[2,2,2,2,2,2,'bahraich',api_key,'2022-02-04',5],[3,3,3,3,3,2,'bahraich',api_key,'2022-02-04',5],
         ['','','',4,4,4,4,4,2,'bahraich',api_key,'2022-02-04',5],[5,5,6]]
    for i in l:
        @patch('builtins.input', side_effect=i)
        def test_createuser(self,mock_inputs):
            result = model.createuser()
            self.assertEqual(result,None)
    #testing delete function
    l = [['','',2,2],[3,3]]
    for i in l:
        @patch('builtins.input', side_effect=i)
        def test_deleteuser(self,mock_inputs):
            result = model.deleteuser()
            self.assertEqual(result,None)
    #testing start function
    l = [[1,2,2,2,2,2,2,'bahraich',api_key,'2022-02-04',5],[2,2,2,'bahraich',api_key,'2022-02-04',5],[3,2,2],['exit_input']]
    for i in l:
        if(i!=l[len(l)-1]):
            @patch('builtins.input', side_effect=i)
            def test_start(self,mock_inputs):
                result = model.start()
                self.assertEqual(result,None)
        else:
            @patch('builtins.input', side_effect=i)
            def test_start(self,mock_inputs):
                with self.assertRaises(SystemExit):
                    result = model.start()    
if __name__ == '__main__':
    unittest.main()