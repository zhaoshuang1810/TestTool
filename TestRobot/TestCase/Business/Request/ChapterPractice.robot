*** Settings ***
Documentation        章节练习
Library              Collections
Library              ../../Library/SqlDjango.py
Library              ../../Library/LibRequest.py


*** Keywords ***
chapter_answer
    [Arguments]    ${caseid}
    [Documentation]    章节答题
    ${userid}    ${answer}    getParamvalues    ${caseid}    chapter_answer
    should be true    ${False}    代码还没有实现

