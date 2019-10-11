# import json
# from application.tests.base import BaseTestCase
# # from application.jsonschemas.schemas import\
# #     ping_schema
# from jsonschema import validate

# class TestViews(BaseTestCase):
#     def test_ping(self):
#         response = self.client.get('/users/ping')
#         data = json.loads(response.data.decode())
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('success', data['message'])
#         validate(ping_schema, data)