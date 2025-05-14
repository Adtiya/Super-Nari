Below is a simple example of a multilingual HR hiring agent using Python. In this solution, `Agent` class represents an AI agent that would interact with job applicants, while `HiringAgent` utilizes Google translate API to provide a translate feature across multiple languages.

```python
# Import required libraries
import random
from googletrans import Translator

# Define constants
SUCCESS_MESSAGES = ["You have been selected", "Congratulations, you have got the job"]
REJECTION_MESSAGES = ["We regret to inform you have not been selected", "You have not got the job this time"]

# Define agent class
class Agent:
    def __init__(self, name):
        self.name = name
    def greet(self):
        return "Hello, I am {}".format(self.name)

# Define hiring agent class
class HiringAgent(Agent):
    def __init__(self, name, language="en"):
        super().__init__(name)
        self.lang = language
        self.translator = Translator()

    def greet(self):
        greeting = super().greet()
        return self.translator.translate(greeting, dest=self.lang).text

    def make_decision(self, applicant):
        decision = random.choice([True, False])  # Randomly decide if the job applicant is hired

        if decision:
            message = random.choice(SUCCESS_MESSAGES)
        else:
            message = random.choice(REJECTION_MESSAGES)

        return self.translator.translate(message, dest=self.lang).text

def main():
    # Create a list of job applicants
    job_applicants = ["John", "Sarah", "Mike", "Jane"]

    # Create a German Hiring agent
    german_hr = HiringAgent("German HR", "de")
    print(german_hr.greet())

    # Making decisions for German applicants
    for applicant in job_applicants:
        print(f"Applicant: {applicant}, Hiring decision: {german_hr.make_decision(applicant)}")

    # Create a Spanish Hiring agent
    spanish_hr = HiringAgent("Spanish HR", "es")
    print(spanish_hr.greet())

    # Making decisions for Spanish applicants
    for applicant in job_applicants:
        print(f"Applicant: {applicant}, Hiring decision: {spanish_hr.make_decision(applicant)}")

if __name__ == "__main__":
    main()
```

In the above code:
1. `Agent` is an AI agent class with the ability to `greet`.
2. `HiringAgent` is an extension to the `Agent` class. It has access to all the instance methods in `Agent`, and includes the functionality to make a hiring decision in a given language using the Google Translate API.
3. In the `main` function, we create German and Spanish HR agents that make hiring decisions for respective job applicants.

Please note, this script requires `googletrans` library. You can install it using pip:
```
pip install googletrans==4.0.0-rc1
```
Also, decision making is randomized for demo purposes, further features can be included such as candidate screening & interviewing, according to realistic HR procedures.