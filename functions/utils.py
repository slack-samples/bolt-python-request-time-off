from datetime import datetime

APPROVE_ID = "approve_action_id"
DENY_ID = "deny_action_id"


def parse_inputs(inputs: dict):
    manager = inputs["manager"]
    employee = inputs["employee"]
    start_date = datetime.fromtimestamp(inputs["start_date"]).strftime("%m/%d/%Y %H:%M")
    end_date = datetime.fromtimestamp(inputs["end_date"]).strftime("%m/%d/%Y %H:%M")
    return manager, employee, start_date, end_date
