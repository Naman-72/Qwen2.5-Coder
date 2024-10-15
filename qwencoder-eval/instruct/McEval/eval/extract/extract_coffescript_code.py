import os 
import re 
import json 
import textwrap
# from humanevalpack import create_all_tasks, create_task
# create_all_tasks()


def extract_coffeescript_code_block(text: str, entry_point) -> str:
    code_block_pattern = re.compile(rf"```(?:[Cc]offeescript\n)?.*?({entry_point}.*?)\n```", re.DOTALL)
    code_block = code_block_pattern.search(text)
    if code_block is None:
        code_block_pattern = re.compile(rf"({entry_point}.*?)(?:\n(?!\n*(?:  |\t))|$)", re.DOTALL)
        code_block = code_block_pattern.search(text)
    if code_block is not None:
        return code_block.group(1)
    # if no code block is found, assume the LM is simply filling the code. Try attaching the output to the prompt
    return text


def extract_coffeescript_code(text, item):
    # task = create_task('', 'synthesize')(language='csharp')
    
    # print('='*100)
    # print(item['task_id'])
    # print(item['prompt'])

    # if "```" in content:
    # code = text.split("```")[1]
    code = extract_coffeescript_code_block(text, item['entry_point'])
    
    
       
    pattern_imports = r"^import.*?$"
    pattern_imports2 = r"^from.*?import.*?$"

    # Extracting import lines from the code
    import_lines =  re.findall(pattern_imports, code, flags=re.MULTILINE)
    import_lines += re.findall(pattern_imports2, code, flags=re.MULTILINE)

    # Removing import lines from the code
    code = re.sub(pattern_imports, "", code, flags=re.MULTILINE).strip()
    
    delca_row_idx = -1
    code_lines = code.split('\n')
    code_lines = [x for x in code_lines if 'console.log' not in x]

    for idx, line in enumerate(code_lines):
        if '->' in line and item['entry_point'] in line:
            delca_row_idx = idx 
            break 

    
    # main_row_idx = -1
    # remove main part
    # for idx, line in enumerate(code_lines):
    #     if '__main__'in line:
    #         main_row_idx = idx 
    #         break 
    # if main_row_idx > 0:
    #     code_lines = code_lines[:main_row_idx]

    # if '{'  in code_lines[delca_row_idx]:
    #     item['prompt'] += '{'


    full_code ='\n'.join(import_lines)+'\n'+ '\n'.join(code_lines[:delca_row_idx])+'\n' + item['prompt']+'\n' + '\n'.join(code_lines[delca_row_idx+1:])+'\n' + item['test']

    # print(full_code)
    return full_code


if __name__ == '__main__':
    items = [json.loads(x) for x in open('completions_coffeescript_humanevalsynthesize.jsonl').readlines() if x]
    for item in items:
        extract_coffeescript_code(item['raw_generation'][0], item)
        


        
  






