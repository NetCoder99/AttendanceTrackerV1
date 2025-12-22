def GetZipCodesStmt():
    return '''
        select physicalCity,
               physicalState,
               physicalZip,
               physicalZip4
        from   zipCodes
        where  physicalZip = :physicalZip
    '''

def GetStateCodesStmt():
    return '''
        select z.physicalState 
        from   zipCodes z
        group  by z.physicalState       
    '''
