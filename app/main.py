import os
from datetime import datetime

from slack_bolt import App
from app.db import upsert_today_standup_status, get_today_standup_status, generate_report

# Initialize the Bolt app with the bot token
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SIGNING_SECRET"]
)

# Define functions for handling standup status submission and report generation

def check_standup_status_submission_completed(today_standup_status):
    """
    Checks if standup status is complete for user.
    :param today_standup_status: Today's standup status
    :return: True if standup is complete otherwise False
    """
    if today_standup_status[2] and today_standup_status[3] and today_standup_status[4] and today_standup_status[5]:
        return True
    return False

def post_standup_completion_message(user_id, say):
    """
    Post standup completion message to selected channel.
    :param user_id: User for which standup needs to be posted
    :return: None
    """
    today_standup_status = get_today_standup_status(user_id)
    if check_standup_status_submission_completed(today_standup_status):
        say(
            text={
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"<@{user_id}> submitted standup status for {today_standup_status[1]} 🎉."
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Yesterday's standup status:",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{today_standup_status[2]}"
                        }
                    },
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Today's standup status:",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type​⬤
