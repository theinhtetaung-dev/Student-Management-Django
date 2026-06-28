import pandas as pd
import os
from filelock import FileLock

class DataManager:
    """
    Handles Pandas read/write operations cleanly to avoid file locking issues.
    Uses filelock to ensure thread-safe and process-safe access to the Excel file.
    """
    def __init__(self, file_path='data/students.xlsx'):
        self.file_path = file_path
        self.lock_path = f"{file_path}.lock"
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['id', 'roll_no', 'studentName', 'major'])
            df.to_excel(self.file_path, index=False)

    def get_all_students(self):
        with FileLock(self.lock_path):
            try:
                if not os.path.exists(self.file_path):
                    return []
                df = pd.read_excel(self.file_path)
                df = df.fillna('')
                # ensure id is int if possible
                if not df.empty and 'id' in df.columns:
                    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
                return df.to_dict('records')
            except Exception as e:
                print(f"Error reading excel: {e}")
                return []

    def add_student(self, student_data):
        with FileLock(self.lock_path):
            try:
                df = pd.read_excel(self.file_path)
                if not df.empty and 'id' in df.columns:
                    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
                    new_id = int(df['id'].max()) + 1
                else:
                    new_id = 1
                    
                student_data['id'] = new_id
                new_df = pd.DataFrame([student_data])
                df = pd.concat([df, new_df], ignore_index=True)
                df.to_excel(self.file_path, index=False)
                return True
            except Exception as e:
                print(f"Error writing to excel: {e}")
                return False

    def update_student(self, student_id, updated_data):
        with FileLock(self.lock_path):
            try:
                df = pd.read_excel(self.file_path)
                if not df.empty and 'id' in df.columns:
                    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
                    idx = df[df['id'] == int(student_id)].index
                    if not idx.empty:
                        for key, value in updated_data.items():
                            df.loc[idx, key] = value
                        df.to_excel(self.file_path, index=False)
                        return True
                return False
            except Exception as e:
                print(f"Error updating excel: {e}")
                return False

    def delete_student(self, student_id):
        with FileLock(self.lock_path):
            try:
                df = pd.read_excel(self.file_path)
                if not df.empty and 'id' in df.columns:
                    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
                    df = df[df['id'] != int(student_id)]
                    df.to_excel(self.file_path, index=False)
                    return True
                return False
            except Exception as e:
                print(f"Error deleting from excel: {e}")
                return False
