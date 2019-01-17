from .basetest import BaseTestCase
from flask import json


class IncidentTestCase(BaseTestCase):
    """ Test for all Incidents tests"""

    def setUp(self):
        """
            Sets up all the reusable parts of the test cases.
            In this way mkaing the testcases more maintainable,
            and cognitive complexity.
        """

        self.new_incident_data = json.dumps({
            "comment": "Police taking a bribe",
            "incidentType": "red-flag",
            "location": "-1.28333, 36.81667",
            "images": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.jpg"],
            "videos": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                       "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"]
        })

        self.new_incident_data_with_wrong_format = json.dumps({
            "comment": "Police taking a bribe",
            "incidntType": "red-flag",
            "location": "-1.28333, 36.81667",
            "createdBy": 1,
            "images": [],
            "videos": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                       "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"]
        })

        self.user_signup_data = json.dumps({
            "first_name": "Joseph",
            "last_name": "Mutiga",
            "other_names": "Kirega",
            "phonenumber": "0716570355",
            "email": "joseph.mutiga934@gmail.com",
            "username": "Joe",
            "password": "123456990"
        })
        self.login_data = json.dumps(
            {"username": "Joe", "password": "123456990"})
        self.app.post('/api/v2/signup', data=self.user_signup_data)
        result = self.app.post('/api/v2/login', data=self.login_data)
        self.token = json.loads(result.data)['access_token']

    def test_1_create_new_incident(self):
        """Test successful creation of a new incident"""
        result = self.app.post('/api/v2/incidents',
                               data=self.new_incident_data,
                               headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "New incident created")

    def test_2_create_new_incident_with_wrong_format(self):
        """Test creation of a new incident with wrong data format """
        result = self.app.post('/api/v2/incidents',
                               data=self.new_incident_data_with_wrong_format,
                               headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_3_get_all_incidents(self):
        result = self.app.get('/api/v2/incidents',
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 200)

    def test_4_get_specific_incident(self):
        result = self.app.get("/api/v2/incident/1",
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data["id"], 1)

    def test_5_get_non_existing_record(self):
        result = self.app.get("/api/v2/incident/1000",
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "No incident by that id/ Not owned")

    def test_6_update_comment_on_with_wrong_format(self):
        data = json.dumps({"commment": "Too many potholes",
                           })
        result = self.app.put('/api/v2/incident/1/comment',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Comment is not present")

    def test_7_update_comment_on_incident_not_in_draft_or_owned(self):
        """Test that an incident that is not in draft cannot be
        edited except to change the status"""
        data = json.dumps({"comment": "Too many potholes"})
        result = self.app.put('/api/v2/incident/100/comment',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Forbidden: Record not owned/ Not in draft status")

    def test_8_update_an_incident_comment(self):
        data = json.dumps({"comment": "Too many potholes"})
        result = self.app.put('/api/v2/incident/1/comment',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Incident Updated")

    def test_9_update_location_on_with_wrong_format(self):
        data = json.dumps({"locations": "1.234 -43.43",
                           })
        result = self.app.put('/api/v2/incident/1/location',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "location is not present")

    def test_10_update_location_on_incident_not_in_draft_owned(self):
        """Test that an incident that is not in draft cannot be
        edited except to change the status"""
        data = json.dumps({"location": "Too many potholes"})
        result = self.app.put('/api/v2/incident/100/location',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Forbidden: Record not owned/ Not in draft status")


class IncidentDeleteTestCase(BaseTestCase):

    def setUp(self):
        """
            Sets up all the reusable parts of the test cases.
            In this way mkaing the testcases more maintainable,
            and cognitive complexity.
        """

        self.new_incident_data = json.dumps({
            "comment": "Police taking a bribe",
            "incidentType": "red-flag",
            "location": "-1.28333, 36.81667",
            "images": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.jpg"],
            "videos": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                       "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"]
        })

        self.user_signup_data = json.dumps({
            "first_name": "Joseph",
            "last_name": "Mutiga",
            "other_names": "Kirega",
            "phonenumber": "0716570355",
            "email": "joseph.mutiga934@gmail.com",
            "username": "KiregaJ",
            "password": "123456789"
        })

        self.admin_signup_data = json.dumps({
            "first_name": "John",
            "last_name": "Murio",
            "other_names": "K",
            "phonenumber": "0716570522",
            "email": "john.murio97@gmail.com",
            "username": "Murio",
            "password": "432189900",
            "isAdmin": True
        })
        self.login_data = json.dumps(
            {"username": "KiregaJ", "password": "123456789"})
        self.admin_data = json.dumps(
            {"username": "Murio", "password": "432189900"})
        self.app.post('/api/v2/signup', data=self.user_signup_data)
        result = self.app.post('/api/v2/login', data=self.login_data)
        self.token = json.loads(result.data)['access_token']
        self.refresh_token = json.loads(result.data)['refresh_token']
        self.app.post('/api/v2/incidents',
                      data=self.new_incident_data,
                      headers=dict(Authorization="Bearer " + self.token))
        self.app.post('/api/v2/signup', data=self.admin_signup_data)
        admin_result = self.app.post('/api/v2/login', data=self.admin_data)
        self.admin_token = json.loads(admin_result.data)['access_token']

    def test_1_update_an_incident_location(self):
        """Test delete works successfully on an incident"""
        data = json.dumps({"location": "1.3242, -53.3"})
        result = self.app.put('/api/v2/incident/1/location',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Incident Updated")

    def test_2_admin_can_change_status(self):
        """Test admin can update the status of an incident"""
        data = json.dumps({"status": "resolved"})
        result = self.app.put('/api/v2/incident/1/status',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.admin_token))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Incident status updated")

    def test_3_admin_bad_status_update(self):
        """Test admin cannot update the status of an incident with an
           invalid status
        """
        data = json.dumps({"status": "resolve dfds"})
        result = self.app.put('/api/v2/incident/1/status',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.admin_token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'],
                         "Status can only be draft,under-investigation,resolved or rejected")

    def test_4_status_update_with_non_admin(self):
        """Test non_admin cannot update the status of an incident 
        """
        data = json.dumps({"status": "resolved"})
        result = self.app.put('/api/v2/incident/1/status',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Incident does not exist/ Not Admin")

    def test_5_status_update_with_bad_format(self):
        """Test status fails for empty payloads/ bad formats
        """
        data = json.dumps({"statuds": "resolved"})
        result = self.app.put('/api/v2/incident/1/status',
                              data=data,
                              headers=dict(Authorization="Bearer " + self.admin_token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "status is not present")

    def test_6_delete_incident(self):
        """Test delete works successfully on an incident"""
        result = self.app.delete('/api/v2/incident/1',
                                 headers=(dict(Authorization="Bearer " + self.token)))
        data = json.loads(result.data)
        self.assertEqual(data["status"], 200)
        self.assertEqual(data['message'], "Incident record has been deleted")

    def test_7_delete_nonexisting_incident(self):
        """Test delete for a non-existing incident fails"""
        result = self.app.delete('/api/v2/incident/1000',
                                 headers=(dict(Authorization="Bearer " + self.token)))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(
            data['message'], "Forbiden cannot delete,record may not exist")

    def test_8_refresh_token(self):
        """Test success in creating a new token"""
        result = self.app.post('/api/v2/token',
                               headers=dict(Authorization="Bearer " + self.refresh_token))
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "New access token created")


class EdgeCaseTest(BaseTestCase):
    """
        This test case class implements other tests that were not considered during the initial writing of tests
    """

    def setUp(self):
        """
            Sets up all the reusable parts of the test cases.
            In this way mkaing the testcases more maintainable,
            and cognitive complexity.
        """
        self.new_incident_data_with_wrong_type = json.dumps({
            "comment": "Police taking a bribe",
            "incidentType": "fadfadfadfa",
            "location": "-1.28333, 36.81667",
            "images": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.jpg"],
            "videos": ["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                       "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"]
        })
        self.user_signup_data = json.dumps({
            "first_name": "Joseph",
            "last_name": "Mutiga",
            "other_names": "Kirega",
            "phonenumber": "0716570355",
            "email": "joseph.mutiga934@gmail.com",
            "username": "Joe",
            "password": "123456990"
        })
        self.login_data = json.dumps(
            {"username": "Joe", "password": "123456990"})
        self.app.post('/api/v2/signup', data=self.user_signup_data)
        result = self.app.post('/api/v2/login', data=self.login_data)
        self.token = json.loads(result.data)['access_token']

    def test_1_get_when_no_incidents_exist(self):
        """Test that the view refuses  non_id accesses"""
        result = self.app.get("/api/v2/incidents",
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "No incidents")

    def test_2_create_new_incident_with_wrong_type(self):
        """Test failing in creation of a new incident"""
        result = self.app.post('/api/v2/incidents',
                               data=self.new_incident_data_with_wrong_type,
                               headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Incident can only be red-flag/intervention")

    def test_get_incident_with_no_id(self):
        """Test that the view refuses  non_id accesses"""
        result = self.app.get("/api/v2/incident/adfa",
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Failed! incidentId is not an id")

    def test_delete_incident_with_no_id(self):
        """Test that the view refuses  non_id accesses"""
        result = self.app.delete("/api/v2/incident/adfa",
                                 headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Failed! incidentId is not an id")

    def test_put_incident_comment_with_no_id(self):
        """Test that the view refuses  non_id accesses"""
        data = json.dumps({"commment": "Too many potholes",
                           })
        result = self.app.put("/api/v2/incident/adfa/comment", data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Failed! incidentId is not an id")

    def test_put_incident_location_with_no_id(self):
        """Test that the view refuses  non_id accesses"""
        data = json.dumps({"location": "Too many potholes",
                           })
        result = self.app.put("/api/v2/incident/adfa/location", data=data,
                              headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Failed! incidentId is not an id")
