def insAttendanceRecordStmt():
    return '''
        INSERT INTO attendance (
            badgeNumber,
            checkinDateTime,
            checkinDate,
            checkinTime,
            studentFirstName,
            studentLastName,
            studentStatus,
            studentRankNum,
            studentRankName,
            studentStripeId,
            studentStripeName,
            classNum,
            className,
            classStartTime,
            styleNum,
            appliesPromotion
        )
        VALUES (
            :badgeNumber,
            :checkinDateTime,
            :checkinDate,
            :checkinTime,
            :studentFirstName,
            :studentLastName,
            :studentStatus,
            :studentRankNum,
            :studentRankName,
            :studentStripeId,
            :studentStripeName,
            :classNum,
            :className,
            :classStartTime,
            :styleNum,
            :appliesPromotion
        );

    '''