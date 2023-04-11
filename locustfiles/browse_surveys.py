from locust import HttpUser, task, between
from random import randint


class Website(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def view_surveys(self):
        survey_id = randint(2,6)
        self.client.get(f'/surveys/?survey={survey_id}', name="surveys")
        print('View surveys')

    @task(4)
    def view_questions(self):
        question_id = randint(1,10)
        self.client.get(f"/questions/{question_id}", name="/questions/:id")
        print('View surtvey detaikl')
    
    @task(1)
    def add_to_survey(self):
        survey_id = randint(1,10)
        self.client.post(
            f"/surveys/{self.survey_id}/questions",
            name="/survey/questions",
            json={"survey_id": survey_id, 'quantity': 1}
            )
        print('addto survey')
    
    @task
    def say_hello(self):
        self.client.get('/hello/')

    def on_start(self):
        response = self.client.post("/surveys")
        result = response.json()
        self.survey_id = result['id']