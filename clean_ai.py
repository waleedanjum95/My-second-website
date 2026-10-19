import os
import re

def clean_tool_titles(directory):
    # Supported file extensions
    extensions = ('.html', '.php', '.js', '.jsx', '.tsx')
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Function to remove "AI " prefix only from inside tags
                    def remove_ai(match):
                        tag_open = match.group(1)
                        inner_text = match.group(2)
                        tag_close = match.group(3)
                        
                        # Remove leading "AI", "AI:", "AI -" case-insensitively
                        cleaned_text = re.sub(r'^\s*AI\s*[:-]?\s*', '', inner_text, flags=re.IGNORECASE)
                        return f"{tag_open}{cleaned_text}{tag_close}"

                    # 1. Target <title> tags
                    new_content = re.sub(r'(<title[^>]*>)(.*?)(</title>)', remove_ai, content, flags=re.DOTALL | re.IGNORECASE)
                    
                    # 2. Target <h1>, <h2>, <h3> headings
                    new_content = re.sub(r'(<h[1-3][^>]*>)(.*?)(</h[1-3>)', remove_ai, new_content, flags=re.DOTALL | re.IGNORECASE)
                    
                    # 3. Target elements with class containing 'title' or 'heading' or 'tool-name'
                    new_content = re.sub(r'(<(?:span|div|p)[^>]*class="[^"]*(?:title|heading|tool-name|card-title)[^"]*"[^>]*>)(.*?)(</(?:span|div|p)>)', remove_ai, new_content, flags=re.DOTALL | re.IGNORECASE)

                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Successfully cleaned: {file}")
                
                except Exception as e:
                    print(f"Error reading {file}: {e}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print("Starting AI prefix cleanup from headings...")
    clean_tool_titles(current_dir)
    print("Cleanup completed!")
                  
