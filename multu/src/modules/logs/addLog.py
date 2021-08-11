def add_error(elementName, elementCss, logs, filePath, actualUrl):
    logs.add(
        'ERROR',
        filePath + ' [' + elementName + ']',
        'Za pomocą selektora ' + elementCss + ' nic nie znaleziono',
        actualUrl
    )


def add_warn(elementName, elementCss, logs, filePath, actualUrl):
    logs.add(
        'WARN',
        filePath + ' [' + elementName + ']',
        'Za pomocą selektora ' + elementCss + ' nic nie znaleziono',
        actualUrl
    )