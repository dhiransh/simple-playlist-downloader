from csv import writer

def write_to_csv(csv_file_name,data_list):
    with open(str(csv_file_name), 'a', newline='',encoding="utf-8") as f_object:  
        writer_object = writer(f_object)
        writer_object.writerow(data_list)  
        f_object.close()
