import boto3
import json
from config import AWS_REGION, SQS_QUEUE_URL

# Initialize the SQS client
sqs = boto3.client('sqs', region_name=AWS_REGION)

def send_book_order(order_id, title, author, isbn, order_format, delivery_info):
    message_body = json.dumps({
        'order_id': order_id,
        'title': title,
        'author': author,
        'isbn': isbn,
        'format': order_format,  # "physical" or "digital"
        'delivery_info': delivery_info
    })
    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=message_body
    )
    print(f"Sent book order {order_id}. Message ID: {response.get('MessageId')}")

if __name__ == "__main__":
    # Example order for a physical book
    send_book_order(
        order_id="order_001",
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        isbn="9780743273565",
        order_format="physical",
        delivery_info={"address": "123 Main St, Anytown, USA"}
    )
    
    # Example order for a digital (Kindle) book
    send_book_order(
        order_id="order_002",
        title="1984",
        author="George Orwell",
        isbn="9780451524935",
        order_format="digital",
        delivery_info={"kindle_email": "yourkindle@example.com"}
    )
