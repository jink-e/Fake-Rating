import gradio as gr
import openai
import pandas as pd
from datetime import datetime

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = "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"


def generate_reviews(product_name, product_features, num_reviews, csv_template):
    # Parse the CSV template to get the header
    if csv_template is None:
        return "Please upload a CSV template to continue.", None

    # template_stream = io.StringIO(csv_template.decode("utf-8"))
    template_df = pd.read_csv(csv_template)
    headers = template_df.columns.tolist()

    # Create an empty DataFrame to match the template headers
    reviews_df = pd.DataFrame(columns=headers)

    for _ in range(num_reviews):
        # Call the OpenAI GPT model to generate review content
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=f"Write a review for a product named {product_name} which has the following features: {product_features}",
        #     max_tokens=50,
        # )
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Write a review for a product named {product_name} which has the following features: {product_features}",
                },
            ],
            max_tokens=50,
        )
        review_body = response.choices[0].message.content.strip()

        # Create a new review entry
        review_entry = {header: "" for header in headers}
        review_entry["body"] = review_body
        review_entry["rating"] = "5"  # Example default rating
        review_entry["review_date"] = datetime.now().strftime("%Y-%m-%d")

        # Append the new review entry to the DataFrame
        # reviews_df = reviews_df.append(review_entry, ignore_index=True)
        reviews_df = pd.concat([reviews_df, pd.DataFrame(review_entry, index=[0])])

    # Convert to CSV
    csv_buffer = "export.csv"
    reviews_df.to_csv(csv_buffer, index=False)
    # csv_buffer.seek(0)

    return reviews_df, csv_buffer


# Create the Gradio interface with the correct component imports
iface = gr.Interface(
    fn=generate_reviews,
    inputs=[
        gr.components.Textbox(
            label="Product Name", placeholder="Enter the product name here"
        ),
        gr.components.Textbox(
            label="Product Features", placeholder="Enter the product features here"
        ),
        gr.components.Number(label="Number of Reviews to Generate"),
        gr.components.File(label="Upload CSV Template"),
    ],
    outputs=[
        gr.components.Dataframe(label="Generated Reviews", type="pandas"),
        gr.components.File(label="Download Reviews as CSV"),
    ],
    live=False,  # Set to False to disable automatic processing
)

iface.launch()
