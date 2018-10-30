*** Settings ***
Documentation        基础功能
Library              Collections
Library              ../../Library/SqlDjango.py
Library              ../../Library/SqlQing.py
Library              ../../Library/LibRequest.py


*** Keywords ***
change_type
    [Arguments]    ${caseid}
    [Documentation]    修改考试类型
    ${userid}    ${subjecttype}    getParamvalues    ${caseid}    change_type
    ${parentId}    ${examtypeId}     ${subjectId}    getSubjectIdFromSubjecttype    ${subjecttype}
    ${params}     create dictionary     subjectId=${subjectId}
    ${code}    ${resp}      getResponse     ${userid}   put    /users/subjects    params=${params}
    should be equal as strings     ${code}    200
    ${curexamId}    ${cursubjectId}    get_current_typeid    ${userid}
    should be equal as strings      ${cursubjectId}    ${subjectId}

get_current_typeId
    [Arguments]     ${userid}
    ${params}    create dictionary      lat=${EMPTY}      lon=${EMPTY}
	${code}    ${resp}      getResponse     ${userid}    get    /users/me    ${params}
	should be equal as strings     ${code}    200
	${curexamId}    get from dictionary    ${resp}    examTypeId
	${cursubjectId}    get from dictionary    ${resp}    currentSubjectId
	[Return]     ${curexamId}    ${cursubjectId}

get_current_typename
    [Arguments]     ${userid}
    ${params}    create dictionary      lat=${EMPTY}      lon=${EMPTY}
	${code}    ${resp}      getResponse     ${userid}    get    /users/me    ${params}
	should be equal as strings     ${code}    200
	${curexamName}    get from dictionary    ${resp}    examType
	${cursubjectName}    get from dictionary    ${resp}    currentSubject
	[Return]     ${curexamName}    ${cursubjectName}