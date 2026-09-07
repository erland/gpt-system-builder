import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from tiny_status.app import health_response,message_response

class TestTinyStatus(unittest.TestCase):
    def test_health(self):
        s,_,b=health_response(); self.assertEqual(200,s); self.assertEqual({"status":"ok"},json.loads(b))
    def test_default(self):
        s,_,b=message_response({}); self.assertEqual(200,s); self.assertEqual({"message":"Hello"},json.loads(b))
    def test_configured(self):
        s,_,b=message_response({"STATUS_MESSAGE":"Ready"}); self.assertEqual(200,s); self.assertEqual({"message":"Ready"},json.loads(b))
if __name__=="__main__": unittest.main()
