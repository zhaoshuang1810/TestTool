*** Settings ***
Documentation     章节练习
Force Tags        InterfaceTest    ChapterPractice    chapter
Resource        ../../../Common/Request.robot
Resource        ../../../Business/Request/ChapterPractice.robot
Resource        ../../../Business/Request/BasicFunction.robot


*** Test Cases ***
TestCase-003
    [Documentation]    青豆中心
    [Tags]    Run

TestCase-002
    [Documentation]    章节练习
    [Tags]    Run
    change_type    2
    chapter_answer    2



