1. PLAN (IN PROGRESS)
    (JIRA/Confluence)
    - using this doc atm

2. CODE (IN PROGRESS)
    (GitHub/Gitlab)
    - Github Actions for CI/CD processes 
        - build-and-test for every pull
            -test.yml in .github/workflow
            -requirements.txt for dependencies of ACTION

    - A minimal 3 tier web app for demo purpose (DONE)
        - React front end (DONE)
        - Golang API (compiled so can test auto build) (DONE)
        - Python SQL call and load generator (DONE)
        - PostgreSQL database (DONE)

3. BUILD (NOT STARTED)
    (webpack?)
    - pyproject.toml for poetry installing python dep

4. TEST (IN PROGRESS)
    (Jest/Playwright/Junit)
    - automated code testing via Github Action (in progress)
        - python (DONE)
        - GO (not started)

5. RELEASE (NOT STARTED)
    (Jenkins/Buildkite)

6. DEPLOY (NOT STARTED)
    - manual docker build pushing to dockerHub (DONE)
    - gcp deployment via kubernetes (DONE)
        - tried kind local deployment, there's issue with kind's load balancer not routing ports correctly (web 80 is not routing to 8000 for api call)

7. OPERATE (IN PROGRESS)
    (kubernetes)

8. MONITOR (NOT STARTED)
    (Prometheus)