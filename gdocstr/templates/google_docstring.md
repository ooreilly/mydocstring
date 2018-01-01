## -*- coding: utf-8 -*-


%if header['function']:
    %if header['class']:
${h1} ${header['class']}.${header['function']}
    %else:
${h1} ${header['function']}
    %endif
```python
def ${header['function']} ${header['signature']}:
```
%endif 
%for section in sections:
    %if section['header']:
${h2} ${section['header']}
    %endif
    %if section['args']:
        %for arg in section['args']:
* **${arg['field']}** ${arg['signature']} : ${arg['description']}
        %endfor
    %endif
${section['text']}
%endfor
%if header['source']:
${h2} Source
```python
${header['source']}
```
%endif

