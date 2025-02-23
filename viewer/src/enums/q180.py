from enum import Enum


class Q180(Enum):

    def __str__(self):
        return str(self.value)

    # "_id" : 1.0,
    # "QV181" : "Quyền viết bài",
    # "QV182" : "CRE_NEW_PIE",
    # "QV183" : "COM",
    # "QL186" : ISODate("2018-05-30T07:13:31.908+0000"),
    # "QL188" : "Tungns"
    CRE_NEW_PIE = 1
    #  "_id" : 2.0,
    # "QV181" : "Quyền piep bài",
    # "QV182" : "CRE_NEW_SEN",
    # "QV183" : "COM",
    # "QL186" : ISODate("2018-05-30T07:13:44.665+0000"),
    # "QL188" : "Tungns"
    CRE_NEW_SEN = 2
    #  "_id" : 4.0,
    # "QV181" : "Quyền scan voucher",
    # "QV182" : "VOU_NEW_SCA",
    # "QV183" : "COM",
    # "QL186" : ISODate("2018-05-30T07:14:52.055+0000"),
    # "QL188" : "Tungns"
    VOU_NEW_SCA = 4
    #  "_id" : 5.0,
    # "QV181" : "LiveStream trong kênh COM",
    # "QV182" : "EXE_NEW_LIV",
    # "QV183" : "COM",
    # "QL186" : ISODate("2018-05-30T07:14:52.055+0000"),
    # "QL188" : "Tungns"
    EXE_NEW_LIV = 5
    #  "_id" : 6.0,
    # "QV181" : "Quyền đọc barcode dành cho nhân viên nhà xe vận tải",
    # "QV182" : "EXE_NEW_BAR",
    # "QV183" : "LOGI",
    # "QL185" : ISODate("2018-05-30T07:15:31.961+0000"),
    # "QL186" : ISODate("2018-05-30T07:14:52.055+0000"),
    # "QL188" : "Tungns"
    EXE_NEW_BAR = 6
    #  "_id" : 7.0,
    # "QV181" : "Quyen thay ADM COMMENT voi user",
    # "QV182" : "FBA_NEW_COM",
    # "QL186" : ISODate("2018-10-26T03:24:04.478+0000"),
    # "QL188" : "TUNGNS"
    FBA_NEW_COM = 7
    #  "_id" : 8.0,
    # "QV181" : "Quyen nhan va tra loi tin nhan",
    # "QV182" : "REC_MSG_FBA",
    # "QL186" : ISODate("2018-10-26T03:24:47.337+0000"),
    # "QL188" : "TUNGNS"
    REC_MSG_FBA = 8
    #  "_id" : 9.0,
    # "QV181" : "Quyen tao PiepLive cho ca nhan tren muc CD",
    # "QV182" : "CRE_PUB_PIE",
    # "QL186" : ISODate("2018-11-02T02:52:58.637+0000"),
    # "QL188" : "TUNGNS"
    CRE_PUB_PIE = 9
    #  "_id" : 10.0,
    # "QV181" : "Quyen lixi cho DN",
    # "QV182" : "CRE_LIX_PIE",
    # "QL186" : ISODate("2018-11-02T02:52:58.637+0000"),
    # "QL188" : "TUNGNS"
    CRE_LIX_PIE = 10
    # "_id" : 11.0,
    # "QV181" : "Quyen tat bat camera",
    # "QV182" : "CAM_LIV_OOF",
    # "QL186" : ISODate("2018-11-02T02:52:58.637+0000"),
    # "QL188" : "TUNGNS"
    CAM_LIV_OOF = 11
    # "_id" : 12.0,
    # "QV181" : "Quyen duyet comment tren cac bai Piep",
    # "QV182" : "CHA_COM_CON",
    # "QL186" : ISODate("2018-11-02T02:52:58.637+0000"),
    # "QL188" : "TUNGNS"
    CHA_COM_CON = 35
    # "_id" : 36.0,
    # "QV181" : "Quyen livestream ve trung tam CENTER cua Kenhp",
    # "QV182" : "CHA_LIV_CEN",
    # "QL186" : ISODate("2018-11-02T02:52:58.637+0000"),
    # "QL188" : "TUNGNS"
    CHA_LIV_CEN = 36
