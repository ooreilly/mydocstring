## -*- coding: utf-8 -*-
%for block in blocks:
    %if block['header']:
${h2} ${block['header']}
    %endif
    %if block['args']:
        %for arg in block['args']:
* **${arg['field']}** ${arg['signature']} : ${arg['description']}
        %endfor
    %endif
${block['text']}
%endfor

