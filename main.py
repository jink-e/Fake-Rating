import gradio as gr
import openai
import pandas as pd
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
# openai.api_key = "YOUR_OPENAI_API_KEY"


def generate_reviews(product_name, product_features, num_reviews, csv_template):
    # Parse the CSV template to get the header
    if csv_template is None:
        return "Please upload a CSV template to continue.", None

    try:
        template_df = pd.read_csv(csv_template.name, encoding="utf-8")
        headers = template_df.columns.tolist()
    except FileNotFoundError:
        raise gr.Error("File not exist, please check the file path.")
    except pd.errors.InvalidColumnName:
        raise gr.Error("Column Name format is not correct, please check the name.")
    except pd.errors.EmptyDataError:
        raise gr.Error("Empty Data, please check the file content.")
    except Exception as e:
        raise gr.Error(f"Error: {e}")

    # Create an empty DataFrame to match the template headers
    reviews_df = pd.DataFrame(columns=headers)

    batch_size = 10
    max_words = 50
    num_reviews = int(num_reviews)
    loop_size = num_reviews

    output_format = f"""
    Output as JSON
    - Please reply with the CSV columns:  {','.join(headers)}.
    - Output should be a plain JSON text without formatting.
    - Each review should no more than {max_words} worlds
    - No comments, and no extra words.
    - Should contain a "data" key
    - Rating should be a int number between 1 and 5
    - Country should be "United States of America"
    """

    # examples
    examples = """
    {"data": []}
    """

    for _ in range(0, num_reviews, batch_size):
        # 稍微调整下咒语，加入输出格式
        instruction = f"""
        Write {min(loop_size, batch_size)} reviews for a product named {product_name} which has the following features: {product_features}.
        """
        prompt = f"""
        {instruction}

        {output_format}

        for example:
        {examples}
        """
        # Call the OpenAI GPT model to generate review content
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a dropshipping expert."},
                {"role": "user", "content": prompt},
            ],
        )
        loop_size -= batch_size
        review_body = response.choices[0].message.content.strip()

        # Create a new review entry
        reviews = json.loads(review_body)
        review_entry = pd.json_normalize(reviews["data"])

        # Append the new reviews array to the DataFrame
        reviews_df = pd.concat([reviews_df, review_entry])

    # Convert to CSV
    csv_buffer = "export.csv"
    reviews_df.to_csv(csv_buffer, index=False)

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
