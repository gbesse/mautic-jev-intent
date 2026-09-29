import os
import unittest
from unittest.mock import patch
from app import process
class MauticTests(unittest.TestCase):
    def test_form_intent(self):
        event={"mautic.form_on_submit":[{"submission":{"lead":{"id":5},"results":{"message":"Please show a demo"}}}]}
        calls=[]
        with patch.dict(os.environ,{"TYPESAFE_API_KEY":"test"}):
            result=process(event,evaluate=lambda text,policy,key:{"outcome":"demo"},update=lambda *args:calls.append(args))
        self.assertEqual(calls,[(5,"demo")])
        self.assertEqual(result[0]["contactId"],5)

    def test_non_text_form_value_is_skipped(self):
        event={"mautic.form_on_submit":[{"submission":{"lead":{"id":5},"results":{"message":["a","b"]}}}]}
        self.assertEqual(process(event,evaluate=lambda *_: self.fail("Jev must not run")),[])

    def test_contact_patch_request(self):
        from app import update_contact
        requests=[]
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self): return b'{}'
        with patch.dict(os.environ,{"MAUTIC_URL":"https://mautic.example","MAUTIC_API_USER":"user","MAUTIC_API_PASSWORD":"test"}),patch('app.urlopen',side_effect=lambda request,timeout:requests.append(request) or Response()):
            update_contact(5,'demo')
        self.assertEqual(requests[0].full_url,'https://mautic.example/api/contacts/5/edit')
        self.assertEqual(requests[0].data,b'jev_intent=demo')
        self.assertEqual(requests[0].get_method(),'PATCH')
