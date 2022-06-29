from locust import HttpUser, task


class ServerPerfTest(HttpUser):

    @task
    def list_club(self):
        self.client.get("/list_club")

    @task
    def index(self):
        self.client.get("/index")

    @task
    def show_summary(self):
        self.client.post("/showSummary", {"email": "admin@irontemple.com"})

    @task
    def book(self):
        competition = "Spring Festival"
        club = "Iron Temple"
        self.client.get("/book/"+competition+"/"+club)

    @task
    def purchasePlaces(self):
        self.client.post("/purchasePlaces", {"competition": "Spring Festival", "club": "Iron Temple", "places": "3"})

    @task
    def logout(self):
        self.client.get("/logout")
