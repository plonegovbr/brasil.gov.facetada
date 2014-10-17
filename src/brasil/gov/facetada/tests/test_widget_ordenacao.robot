*** Settings ***

Library  Selenium2Library  timeout=10 seconds  implicit_wait=5 seconds
Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description

*** Test cases ***

Test ORDENAR
    # Loga
    Log in as site owner
    Go to  ${PLONE_URL}
    # Adiciona Pasta
    Open Add New Menu
    Click Link  css=a#folder
    Page Should Contain  Add Folder
    Input Text  css=#title  Facetada
    Input Text  css=#description  Descricao
    Click Button  Save
    Page Should Contain  Changes saved
    # Ativa a facetada
    Go to  ${PLONE_URL}/facetada/@@faceted_subtyper/enable
    # Acesse facetad criteria
    Go to  ${PLONE_URL}/facetada/configure_faceted.html
    Page Should Contain  Extended search
    # Adicionar widget
    Sleep  1 sec
    Click Element  css=span.ui-icon.ui-icon-plus.ui-corner-all
    Sleep  1 sec
    Page Should Contain  Type of the widget
    Select From List  xpath=//select[@name="wtype"]  ordenar
    Sleep  3 sec
    Page Should Contain  Filter from vocabulary
    Input Text  css=#c0_title  Ordenar por
    Select From List  xpath=//select[@name="c0_vocabulary"]  brasil.gov.ordenacao
    Click Element  xpath=//span[text()='Add']
    Sleep  3 sec
    Go to  ${PLONE_URL}/facetada/@@faceted_layout?layout=faceted-summary
    Select From List  xpath=//select[@name="ordenacao"]  sortable_title_reverse
    Page Should Contain  Imagem de PloneGovBR


*** Keywords ***

Click Label
    [Arguments]    ${label}    ${index}=1
    [Documentation]    Clicks label element which contains text ${label}.
    ...    If there is more than one label with given text, specify index to match those labels.
    Click Element    xpath=(//label[contains(., '${label}')])[${index}]