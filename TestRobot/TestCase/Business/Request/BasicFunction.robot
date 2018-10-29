*** Settings ***
Documentation        基础功能
Library              ../../Library/SqlDjango.py
Library              Collections
Library              RequestsLibrary


*** Keywords ***
change_type
    [Arguments]    ${caseid}
    [Documentation]    修改考试类型
    ${userid}    ${subjecttype}    getParams    ${caseid}    change_type
    should be true    ${False}    代码还没有实现

