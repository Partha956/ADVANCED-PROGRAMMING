class ScoreProcessor:
    def process_score_file(self, file_path: str) -> int:
        file = None
        try:
            # 1. Attempt to open and read the file
            file = open(file_path, 'r')
            content = file.read().strip()
            
            # 2. Parse the text into an integer and multiply
            score = int(content)
            result = score * 10
            
        except FileNotFoundError as e:
            # Handle missing files gracefully
            print(f"Error: The file '{file_path}' was not found.")
            raise e  # Re-raising so the test suite can catch it
            
        except ValueError as e:
            # Handle letters or corrupted data where an integer was expected
            print(f"Error: The file '{file_path}' contains invalid data. Expected an integer.")
            raise e
            
        else:
            # Executes ONLY if the try block succeeds without throwing an error
            print("Data processed successfully")
            return result
            
        finally:
            # Executes EVERY TIME, guaranteeing system resources are freed
            if file is not None:
                file.close()
            print("File cleanup completed")


# --- THE MAIN PART (MUST START AT THE FAR LEFT WALL) ---
if __name__ == "__main__":
    import os
    
    # 1. Initialize our logic module
    processor = ScoreProcessor()
    filename = "score.txt"
    
    print("=== SCENARIO 1: Processing a Valid File ===")
    # Create a temporary file with standard numeric content
    with open(filename, "w") as f:
        f.write("85")
        
    try:
        output = processor.process_score_file(filename)
        print(f"Calculation Result (Score * 10): {output}")
    except Exception as e:
        print(f"Main caught an unexpected error: {e}")
        
    print("\n" + "="*40 + "\n")
    
    print("=== SCENARIO 2: Processing a Corrupted File ===")
    # Overwrite the file with text data instead of numbers
    with open(filename, "w") as f:
        f.write("eighty-five")
        
    try:
        processor.process_score_file(filename)
    except ValueError:
        print("Main block successfully monitored the ValueError exception wrapper.")
        
    print("\n" + "="*40 + "\n")
    
    print("=== SCENARIO 3: Processing a Missing File ===")
    # Clean up and completely remove the file from your workspace directory
    if os.path.exists(filename):
        os.remove(filename)
        
    try:
        processor.process_score_file(filename)
    except FileNotFoundError:
        print("Main block successfully monitored the FileNotFoundError exception wrapper.")