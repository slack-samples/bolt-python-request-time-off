# Bolt Python Request Time Off

This is a [Slack CLI](https://api.slack.com/future/overview) compatible app that uses Bolt Python to create an interactive time off request flow.

The application can be used to submit time off requests through a workflow, which will then be sent to a specified manager. The manager will be able to approve or deny the request, notifying the submitter.

![take-your-time-demo](https://user-images.githubusercontent.com/12901850/186937812-6d732228-6b14-41d3-83fc-531125e67957.gif)

## Installation

#### Prerequisites
To use this template, you will need to have installed and configured the Slack CLI. 

Before you start building with the CLI, an admin or owner on your workspace needs to have accepted the Slack Platform and Beta Service Terms [here](https://slack.com/admin/settings#hermes_permissions).

Once you've accepted the Terms of Service, you can get started with the CLI through our [Quickstart Guide](https://api.slack.com/future/quickstart).

### Setup Your Project

```zsh
# Clone this project onto your machine
slack create my-app -t slack-samples/bolt-python-request-time-off

# Change into this project directory
cd my-app

# Run app locally
slack run

# Deployment 
# Slack currently doesn't support deployment of Bolt apps

```
#### Running your app locally

While building your app, you can see your changes propagated to your 
workspace in real-time with `slack run`.

Executing `slack run` starts a local development server, syncing changes to 
your workspace's development version of your app. (You'll know it's the 
development version because the name has the string `(dev)` appended).

Your local development server is ready to go when you see the following:

```zsh
⚡️ Bolt app is running! ⚡️
```

When you want to turn off the local development server, use `Ctrl+c` in the command prompt.

#### Deploying your app
We'll be adding documentation for Bolt app deployments - check back soon!

### Initialize your Workflow Trigger
To allow for a workflow to be executed in a workspace, you'll need to create a [trigger](https://api.slack.com/future/triggers). Slack supports many different kinds of triggers, and for this application, we will use a [link trigger](https://api.slack.com/future/triggers#link). The definition for this link trigger is a JSON config file which can be found in `manifest/triggers/time_off_request.json`.

The contents of the file looks something like this:

```json
{
    "type": "shortcut",
    "name": "Request Time Off",
    "description": "Submit a request to take time off",
    "workflow": "#/workflows/time_off_request",
    "shortcut": {},
    "inputs": {
        "interactivity": {
            "value": "{{data.interactivity}}"
        }
    }
}
```

This file acts as a config for your trigger that specifies which workflow is executed when the trigger is invoked (in this case, it maps the workflow to the `time_off_request` callback ID from the Time Off Request Workflow initialized in `manifest/manifest.json`).

This file will also define how the trigger shows up in your application - for example, the `name` field will be the name of the trigger when it is surfaced as a link trigger in your workspace.

To create a trigger for your workflow, run the following command:
```zsh
slack triggers create --trigger-def "manifest/triggers/time_off_request.json"
```

This trigger will produce an output that looks like this:
```zsh
⚡ Trigger created
     Trigger ID:   [ID for trigger]
     Trigger Type: [type of trigger]
     Trigger Name: [name of trigger]
     URL:  [some URL]
```
To make the trigger accessible, you can paste the link trigger URL in a channel or conversation. We recommend saving the trigger as a channel bookmark for easy access.

#### Adding new triggers

To add new triggers to your app, you’ll need to do the following:

1. Update the `manifest.json` with the desired workflow and/or functionality you’d like your trigger to execute.
2. Run `slack run` so that any new additions to the `manifest.json` file will be detected within the `slack trigger` command.
3. Create a JSON file in the `./manifest/triggers` directory to [generate your trigger](https://api.slack.com/future/triggers).
4. Run `slack triggers create --trigger-def "manifest/triggers/[json-name].json"`.

## Project Structure

### `app.py`

`app.py` is the entry point for the application. This project aims to keep this file as thin as possible, primarily using it as a way to route inbound requests.

### `/functions`
This directory holds function listeners and invocations. `__init__.py` registers the function listener for the app, while `request-approval.py` configures the appropriate function handler that will be called when that function's event is detected. Additional handlers for the function event, such as action handlers, are configured in this file as well.

### `/functions/actions`
This directory holds related actions that are triggered as additional interactivity event handlers when a function is called.

### `/functions/request-approval.py`

This file contains the configuration for notifying a manager once an approval request has been submitted, which then triggers a function. This file sets up a listener to listen for the function being called and then executes a particular response that sends a message to the approver to then approve or deny the request.

### `/manifest`

This directory contains all related initialization of the app as well as any workflow or function definitions used in the project.

### `/manifest/manifest.json`

`manifest.json` is a configuration for Slack CLI apps in JSON. This file will establish all basic configurations for your application, including app name and description. 

### `/manifest/triggers`

All trigger configuration files live in here - for this example, `link-shortcut.json` is the trigger config for a trigger that starts the workflow initialized in `/manifest/manifest.json`.

### `slack.json`

`slack.json` is a required file for running Slack CLI apps. This file is a way for the CLI to interact with your project's SDK. It defines script hooks which are *executed by the CLI* and *implemented by the SDK.*

