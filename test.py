import pypandoc
import md_to_rst

with open('test.md', 'r') as f:

    with open('out.txt', 'w') as out:
        
        out.write(md_to_rst.convertMarkdownToRst(f.read()))