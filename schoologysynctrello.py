import schoolopy
import requests
from datetime import datetime

# Schoology API credentials
schoology_key = 'cfbafa380dc674a7cb1f0f88c9bb8e6b066030100'
schoology_secret = 'a715600fbcafee292486455876af32da'
user_id = '88900029'  # ID of the user whose assignments you're fetching

# Trello API credentials (API Key and Token)
trello_key = 'bb92e157965f1f71f00032b062792776'
trello_token = 'c06b6d41802160f7c687d2d81936f9172c1174a00f12d296aa77fcc92d59db2a'
trello_board_id = '66c3c7e6e63381789951a1dd'

checklist_ids = {
    'Math': '66c3c7e754395df586dbfb3b',
    'ELA': '66c3c7e7cd890f21f3da3088',
    'Science': '66c3c7e7620e4f5f9bbf74d1',
    'History': '66c3c80d7b8bf9865171b7d4',
    'Engineering': '66c3c81277cbc584e0cef5cd',
}

# Sample mapping for section_id to course names
section_id_to_course = {
    7354798618: "Math",
    7354798552: "ELA",
    7354803440: "Engineering",
    7354802315: "Science",
    7354802356: "History"
    # Add other section_id to course mappings as needed
}

# Initialize Schoology API with OAuth
sc = schoolopy.Schoology(schoolopy.Auth(schoology_key, schoology_secret))

# Function to check if an assignment already exists in Trello
def assignment_exists_in_trello(assignment_name):
    # Make a request to Trello API to check for existing cards in the checklist
    response = requests.get(
        f'https://api.trello.com/1/checklists/{checklist_ids.get("Math")}/cards',
        params={'key': trello_key, 'token': trello_token}
    )
    if response.status_code == 200:
        cards = response.json()
        return any(card['name'] == assignment_name for card in cards)
    return False

# Function to add an assignment to Trello
def add_assignment_to_trello(checklist_id, assignment_name):
    # Make a request to Trello API to add the assignment to the specified checklist
    response = requests.post(
        'https://api.trello.com/1/cards',
        params={
            'key': trello_key,
            'token': trello_token,
            'name': assignment_name,
            'idChecklist': checklist_id
        }
    )
    if response.status_code == 200:
        print(f'Added "{assignment_name}" to Trello successfully.')
    else:
        print(f'Failed to add "{assignment_name}" to Trello: {response.content}')

# Function to sync assignments with Trello
def sync_assignments():
    today = datetime.now().date()
    try:
        feed = sc.get_feed()

        for update in feed:
            # Print the entire update object for debugging
            print(update)  # This will help you see available attributes

            # Extract relevant data
            assignment_body = update.body
            assignment_name = assignment_body.split('\n')[0]  # Assuming the first line is the assignment title
            created_at = datetime.fromtimestamp(update.created).date()

            # Skip assignments created before today
            if created_at < today:
                continue

            # Check if the assignment already exists in Trello
            if assignment_exists_in_trello(assignment_name):
                print(f'"{assignment_name}" already exists in Trello.')
                continue

            # Determine subject from the section ID
            subject = section_id_to_course.get(update.section_id, '')
            if not subject:
                print(f'No course information available for section ID {update.section_id}. Assignment skipped.')
                continue

            # Debugging output to see what is detected
            print(f'Detected assignment: "{assignment_name}" | Created at: {created_at} | Subject: {subject}')

            # Check if there is a designated checklist for the subject
            if subject in checklist_ids:
                add_assignment_to_trello(checklist_ids[subject], assignment_name)
            else:
                print(f'No designated checklist for subject: "{subject}". Assignment skipped.')

    except Exception as e:
        print(f'Failed to fetch assignments: {e}')

# Main execution
if __name__ == '__main__':
    sync_assignments()
