## -*- coding: utf-8 -*-

%if header['function']:
    %if header['class']:
${h1} ${header['class']}.${header['function']}
    %else:
${h1} ${header['function']}
    %endif
```python
def ${header['function']}${header['signature']}:
```
%elif header['class']:
${h1} ${header['class']}
```python
class ${header['class']}${header['signature']}:
```
%endif 

%for section in sections:
    %if section['header']:
${h2} ${section['header']}
    %else:
---
    %endif
    %if section['args']:
        %for arg in section['args']:
        %if arg['field']:
* **${arg['field']}** ${arg['signature']} : ${arg['description']}
        %else:
* ${arg['description']}
        %endif
        %endfor
    %endif
${section['text']}
%endfor

%if header['function'] and header['source']:
${h2} Source
```python
${header['source']}
```
%endif
