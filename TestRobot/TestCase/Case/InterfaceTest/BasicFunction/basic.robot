*** Settings ***
Documentation     修改考试类型功能
Force Tags        InterfaceTest    BasicFunction    basic
Resource        ../../../Business/Request/ChapterPractice.robot
Resource        ../../../Business/Request/BasicFunction.robot


*** Test Cases ***
TestCase-001
    [Documentation]    修改考试类型，科目类型
    [Tags]    Run
    change_type    1



