*** Settings ***
Documentation        章节练习
Library              ../../Library/SqlDjango.py
Library              Collections
Library              RequestsLibrary


*** Keywords ***
chapter_answer
    [Arguments]    ${caseid}
    [Documentation]    章节答题
    ${userid}    ${answer}    getParams    ${caseid}    chapter_answer
    should be true    ${False}    代码还没有实现

