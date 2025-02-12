import boto3
import json
import time
from config import AWS_REGION, SQS_QUEUE_URL, SNS_TOPIC_ARN

# Initialize the SQS and SNS clients
sqs = boto3.client('sqs', region_name=AWS_REGION)
sns = boto3.client('sns', region_name=AWS_REGION)

def process_book_orders():
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10 
        )
        
        messages = response.get('Messages', [])
        if not messages:
            print("No messages in queue. Waiting...")
            time.sleep(2)
            continue
        
        for message in messages:
            receipt_handle = message['ReceiptHandle']
            order = json.loads(message['Body'])
            order_id = order.get('order_id')
            title = order.get('title')
            author = order.get('author')
            isbn = order.get('isbn')
            order_format = order.get('format')
            delivery_info = order.get('delivery_info')
            
            print(f"Processing order {order_id} for '{title}' by {author}...")
            time.sleep(1)
            
            # Prepare a notification message based on the order format
            if order_format.lower() == "physical":
                notification_message = (
                    f"Order {order_id}: '{title}' by {author} will be shipped to "
                    f"{delivery_info.get('address')}."
                )
            else:
                notification_message = (
                    f"Order {order_id}: '{title}' by {author} is now available for download on "
                    f"your Kindle account ({delivery_info.get('kindle_email')})."
                )
            
            # Publish the notification to the SNS topic
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=notification_message,
                Subject="Swapnil's Book Order Processed"
            )
            
            print(f"Notification sent for order {order_id}.")
            
            # Delete the message from the queue to prevent reprocessing
            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=receipt_handle
            )
            print(f"Order {order_id} removed from queue.\n")
            
if __name__ == "__main__":
    process_book_orders()
