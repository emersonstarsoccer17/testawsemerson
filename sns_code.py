import boto3
import xml.etree.ElementTree as ET

# AWS SNS Topic ARN
sns_topic_arn = 'arn:aws:sns:us-east-2:825765397227:sns-notification-emerson'  # Replace with your SNS topic ARN

# Function to parse the XML file and extract the test case results
def parse_xml_file(file_path):
    try:
        print(f"Parsing XML file: {file_path}")
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Initialize lists to track passed and failed test cases
        passed_tests = []
        failed_tests = []

        # Iterate through the XML tree to find test results
        for test in root.iter('test'):
            test_name = test.get('name')
            status = test.find('status').get('status')
            
            if status == 'PASS':
                passed_tests.append(test_name)
            elif status == 'FAIL':
                failed_tests.append(test_name)

        # Create a message string with passed and failed test cases
        message = "Test Results:\n"
        message += "\nPassed Tests:\n"
        message += "\n".join(passed_tests) if passed_tests else "None\n"
        
        message += "\nFailed Tests:\n"
        message += "\n".join(failed_tests) if failed_tests else "None\n"

        return message
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return None

# Function to send an SNS notification
def send_sns_notification(topic_arn, message):
    try:
        print(f"Sending SNS notification to {topic_arn}")
        sns_client = boto3.client('sns')
        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='Test Results Notification from Robot Framework'
        )
        print("SNS notification sent successfully.")
    except Exception as e:
        print(f"Error sending SNS notification: {e}")

# Main function to coordinate the steps
def main():
    # Step 1: Parse the XML file and extract the test results
    file_path = 'output.xml'  # Replace with the path to your output.xml file
    message = parse_xml_file(file_path)
    
    if message is None or message == "":
        print("No message to send. Exiting.")
        return
    
    # Step 2: Send SNS notification with the extracted message
    send_sns_notification(sns_topic_arn, message)

if __name__ == '__main__':
    main()
