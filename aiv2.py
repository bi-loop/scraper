import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
import re
import sheets_auto
import categorize
import time

# Assuming sheets_auto.fetch_all_data() returns a pandas DataFrame
df = sheets_auto.fetch_all_data()


async def fetch_url(session, url):
    async with session.get(url + "/videos") as response:
        return await response.text()


async def process_row(row_number, session):
    try:
        if pd.isnull(df.at[row_number, 'Status']):  # Process rows with no 'Status' value
            row = df.iloc[row_number]
            title = row['title']
            html_content = await fetch_url(session, row['URL'])
            soup = BeautifulSoup(html_content, 'html.parser')
            description = soup.find('meta', attrs={'itemprop': 'description'})['content']
            pattern = re.compile(r'"title":\{"runs":\[\{"text":"(.*?)"\}\]')
            matches = pattern.findall(str(soup))[:20]
            category = categorize.ask_gpt(title, description, matches)
            sub_category = categorize.ask_gpt(title, description, matches, category)
            df.at[row_number, 'Status'] = 'Whitelist'
            df.at[row_number, 'Category'] = category
            df.at[row_number, 'Sub_Category_1'] = sub_category
            return f"Processed row {row_number}"
    except Exception as e:
        print(f"Error processing row {row_number}: {e}")


async def process_batch(start_row, end_row, session):
    tasks = []
    for row_number in range(start_row, end_row):
        tasks.append(process_row(row_number, session))
    results = await asyncio.gather(*tasks)
    for result in results:
        if result:
            print(result)


async def process_rows_in_batches(start_row, batch_size):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        for current_start_row in range(start_row, len(df), batch_size):
            end_row = min(current_start_row + batch_size, len(df))
            await process_batch(current_start_row, end_row, session)
            elapsed_time = time.time() - start_time
            print(f"Processed rows {current_start_row}-{end_row - 1}, Time elapsed: {elapsed_time:.2f} seconds.")

            if ((
                        current_start_row - start_row) // batch_size + 1) % 5 == 0:  # Update after every 5 batches (50 rows if batch_size is 10)
                sheets_auto.update_sheet_with_dataframe(df)
                print(f"Updated sheet with rows {current_start_row}-{end_row - 1}")


async def main():
    batch_size = 10
    start_row = int(input("Enter the starting row number: "))
    await process_rows_in_batches(start_row, batch_size)
    # Ensure the final update after all rows are processed
    sheets_auto.update_sheet_with_dataframe(df)


if __name__ == "__main__":
    asyncio.run(main())
