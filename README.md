# Bolt Python Request Time Off

This is a Slack CLI compatible app that uses Bolt Javascript to create an interactive time off request flow.

The application can be used to submit time off requests through a workflow, which will then be sent to a specified manager. The manager will be able to approve or deny the request, notifying the submitter.

## How to
In order to run this application locally you will need to have [python](https://www.python.org/) and the [SlackCLI](https://api.slack.com/future/tools/cli) installed on your machine

1. Install the dependencies 
   ```bash
   pip install -r requirements.txt
   ```
2. Login to your slack workspace
   ```bash
   slack login
   ```
3. Create the trigger for the function
   ```bash
   slack trigger create --trigger-def manifest/triggers/time_off_request.json
   ```
4. Start your application
   ```
   slack run
   ```
5. Use the trigger url in your workspace

