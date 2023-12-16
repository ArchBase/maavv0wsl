import pyarrow.parquet as pq

def read_from_paraquet(file_path="dataset.parquet", limit=10):
    need_limit = True
    if limit==-1:
        need_limit=False
    # Specify the path to your Parquet file
    parquet_file_path = file_path

    # Read the Parquet file into a PyArrow Table
    table = pq.read_table(parquet_file_path)
    questions = []
    answers = []
    # Iterate over rows
    for i in range(table.num_rows):
        #print(f"Row {i}:")
        ans=True
        # Iterate over columns in the current row
        for j in range(table.num_columns):
            
            column_name = table.column_names[j]
            cell_value = table.column(column_name)[i].as_py()
            #print(f"  {column_name}: {cell_value}")
            if ans:
                answers.append(cell_value)
                ans = False
            else:
                questions.append(cell_value)
                ans = True
        if need_limit:
            if i > limit:
                break
    #print(answers)
    print(f"readed {len(questions)} questions and {len(answers)} answers")
    return (questions[:-2], answers[:-2])