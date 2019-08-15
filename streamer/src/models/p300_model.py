from . import HTTP_MODEL


class P300_model(HTTP_MODEL):
    def __init__(self):
        super(P300_model, self).__init__()

    # POST
    #  Lấy danh sách pieper COM
    # {
    #   ACTION: ___,
    #   PP300: ___,
    #   FO100: ___, // chủ doanh nghiệp
    #   FO100W: ___, // người viết
    #   SEARCH: ___,
    #   OFFSET: ___,
    #   LIMIT: ___,
    #   LOGIN: ___,
    #   FILTER: ['LIVE', 'COUNTDOWN' ] <<< Chỉ dành cho App Pieplivecenter
    # }
    def listoftabP300EByOwner(self, param):
        return self._get("/v2/service/p300e/p2019_listoftabP300EByOwner", param)

    # POST
    # Hàm cập nhật thông tin P300 (tuy chon)
    #
    # @param FO100 : <required> ID doanh nghiệp (Nếu không viết cho doanh nghiệp thì là ID của người viết)
    # @param PP300 : <required> ID bai viet
    # @param FT300 <required>
    #              0: không thuôc category
    #              1: là category COM (Ẩn)
    #              2: là category tuyển dụng
    #              3: là category ẩm thực
    #              4: là category bất động sản
    #              5: là category thời trang
    #              6: là category PUBLIC (Ẩn)
    #              7: là category CIRCLE (Ẩn)
    # @param PV301 : tieu de
    # @param PV302 : key ma hoa (neu = OFF thi khong can ma hoa)
    # @param PN303 : = 1 là text ko hình, = 2 là pieper có hình
    # @param PV304 : hình
    # @param PV305 : nội dung
    # @param PV307 : Link Thumb hình ảnh
    # @param PN309 : tỷ lệ width/height của hình
    # @param PV314 : 100 ký tự của pv305
    # @param PA316 : O Tag [ ]
    # @param PA318 : O Tag Bổ sung [ ]// xu ly sau
    # @param PV319 : Ngôn ngữ
    # @param PO322 : Data audio/video
    # @param PO323: Setting
    #      {
    #          PN323_CM: 0 || 1 // Comment
    #          PN323_NRC: 0 || 1 // Not remove Comment
    #          // 0: Cho xoa
    #          // 1: Khong cho xoa
    #          PN323_FEE: 0 || 1 // Thu phí hay không
    #          PN323_FEV: 0 // Giá tiền
    #          PA323_SRE: [
    #              'PME' // PiepMe
    #              'OTH' // Social #
    #          ]
    #          PV323_SEE: "ME || FRI || PUB"
    #      }
    # @param PN326 : Priority ( 0, 1, 2)
    # @param LOGIN nguoi login
    #
    # Chú ý: Field nào truyền lên thì sẽ được update, không truyền không update
    # @returns -2;// Bài này không tồn tại hoặc đã bị xóa
    #
    def updatetabP300_prov(self, param):
        return self.v3_post("/v3/service/p300/p2018_v3_updatetabP300_prov", param)
