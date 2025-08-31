#!/usr/bin/env python

import pandas as pd

def load_multiproportions(file):
    df = pd.read_csv(file, sep='\t')
    df = df.set_axis(['Question', 'Response', 'Count'], axis=1)
    return df

def load_proportions(file):
    df = pd.read_csv(file, sep='\t')
    df['Percentage'] = df['Percentage'].astype(float).map(lambda x: f"{x:.2f}")
    df['Count'] = df['Count'].astype(str) + ' (' + df['Percentage'] + ')'
    df = df.drop(columns=['Percentage'])
    return df

def load_averages(file):
    df = pd.read_csv(file, sep='\t', index_col=0)
    return df

def merge_data(multiproportions_file, proportions_file, averages_file):
    multiproportions_df = load_multiproportions(multiproportions_file)
    proportions_df = load_proportions(proportions_file)
    averages_df = load_averages(averages_file)
    
    # Convert the averages data to a structured format
    averages_table = []
    for index, row in averages_df.iterrows():
        averages_table.append({
            "Question": index,
            "Response": "Mean (SD)",
            "Count": f"{row['mean']:.2f} ({row['std']:.2f})"
        })
    
    # Combine both tables
    merged_df = pd.concat([multiproportions_df, proportions_df, pd.DataFrame(averages_table)], ignore_index=True)
    
    return merged_df

def save_table(merged_df, output_file):
    # Save as Excel file with Times New Roman font formatting using xlsxwriter
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    merged_df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    
    # Create a cell format that uses Times New Roman
    cell_format = workbook.add_format({'font_name': 'Times New Roman'})
    header_format = workbook.add_format({'font_name': 'Times New Roman', 'bold': True})
    
    # Apply the header format to the header row
    for col_num, header in enumerate(merged_df.columns):
        worksheet.write(0, col_num, header, header_format)
        # Set the format for the column; you can adjust the width as necessary.
        worksheet.set_column(col_num, col_num, 20, cell_format)
    
    writer.close()

def main():
    proportions_file = "results/proportions.tsv"
    multiproportions_file = "results/multiproportions.tsv"
    averages_file = "results/averages.tsv"
    output_file = "results/table1.xlsx"
    questions_file = 'conf/questions.xlsx'
    questions = pd.read_excel(questions_file, index_col=0)
    
    merged_df = merge_data(multiproportions_file, proportions_file, averages_file).set_index('Question')
    col_df = merged_df.join(questions.full_question).set_index('full_question').reset_index()
    col_df.rename(columns= {'full_question': 'Question'}, inplace=True)

    # Remove duplicate 'Question' entries after the first occurrence
    col_df['Question'] = col_df['Question'].where(~col_df['Question'].duplicated(), '')

    save_table(col_df, output_file)
    print(f"Table saved to {output_file}")

if __name__ == "__main__":
    main()
