import pandas as pd
import os

def process_modbus_xml_style(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Файл {input_path} не знайдено!")
        return

    # Читаємо всі аркуші без заголовків
    all_sheets = pd.read_excel(input_path, sheet_name=None, header=None)
    writer = pd.ExcelWriter(output_path, engine='openpyxl')
    
    cols = ['No', 'Signal name', 'Read and write', 'Type', 'Unit', 'Gain', 'Address', 'Number of regs', 'Scope']
    something_saved = False

    for sheet_name, df in all_sheets.items():
        # Видаляємо повністю порожні рядки/стовпчики
        df = df.dropna(how='all').reset_index(drop=True)
        if df.empty:
            continue

        final_rows = []
        current_record = None
        start_col_idx = 0 

        for _, row in df.iterrows():
            clean_row = [str(x).strip() if pd.notnull(x) else "" for x in row]
            
            # Шукаємо номер регістра (зазвичай це число < 5000 у перших 3 колонках)
            found_no = None
            for i in range(min(3, len(clean_row))):
                val = clean_row[i].replace('.0', '') # прибираємо хвости від float
                if val.isdigit() and 0 < len(val) < 5:
                    found_no = val
                    start_col_idx = i
                    break
            
            if found_no:
                if current_record:
                    final_rows.append(current_record)
                
                # Створюємо новий запис
                current_record = []
                for j in range(start_col_idx, start_col_idx + 9):
                    val = clean_row[j] if j < len(clean_row) else ""
                    current_record.append(val)
                current_record[0] = found_no
            else:
                # Доклеюємо текст до існуючого запису
                if current_record:
                    for j in range(start_col_idx, len(clean_row)):
                        target_col = j - start_col_idx
                        if 0 < target_col < 9:
                            val = clean_row[j]
                            if val and val.lower() != 'nan':
                                # Адреси та кількість (стовпці 6 та 7) клеїмо без пробілів
                                if target_col in [6, 7]:
                                    current_record[target_col] = (current_record[target_col] + val).replace(' ', '').replace('.0', '')
                                else:
                                    # Текст клеїмо через пробіл
                                    current_record[target_col] = f"{current_record[target_col]} {val}".strip()

        if current_record:
            final_rows.append(current_record)

        if final_rows:
            res_df = pd.DataFrame(final_rows, columns=cols)
            # Очищуємо колонку Address від усього, крім цифр
            res_df['Address'] = res_df['Address'].str.replace(r'[^0-9]', '', regex=True)
            res_df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Аркуш '{sheet_name}': оброблено {len(res_df)} рядків.")
            something_saved = True

    if not something_saved:
        # Створюємо порожню сторінку, щоб Excel не ламався
        pd.DataFrame([["Дані не знайдено"]]).to_excel(writer, sheet_name="Порожньо")
        print("Регістрів не знайдено в жодному аркуші.")

    writer.close()
    print(f"Готово! Файл збережено: {output_path}")

# Запуск
process_modbus_xml_style('3reg-2.xlsx', 'Huawei_Final_Result.xlsx')
