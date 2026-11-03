# Cùng Rảnh: quy trình sửa app

App PWA tìm ngày rảnh chung cho nhóm bạn. Người tạo: Hoàng Trung Đức. Chạy trên GitHub Pages.

## Cấu trúc
- `src/app.html`: mã nguồn chính (giao diện + logic, một file). SỬA Ở ĐÂY.
- `src/localdb.js`: kho dữ liệu một máy dùng khi chưa có Firebase.
- `src/build.py`: sinh `index.html`, `sw.js`, `manifest.webmanifest`, `.nojekyll`. Không sửa tay các file sinh ra.
- `config.js`: cấu hình Firebase (`window.CUNGRANH_FIREBASE`); null = chế độ một máy. Sửa được không cần build, nhưng build lại để sw đổi hash.
- `firestore.rules`: luật bảo mật dán vào Firebase Console > Firestore > Rules.
- `icons/`: icon PWA. `src/qc/`: script kiểm tra.

## Dữ liệu
`data/users/<uid>/profile`, `groups/<gid>`, `invites/<code>`, `groups/<gid>/members/<uid>` (name, free[], maybe[], done, ac, an, dn, role), `groups/<gid>/events/<eid>`.
Mã trong app dùng giao diện giống Firestore: doc/collection/onSnapshot/set/update/delete/get.

## Quy trình
1. Sửa `src/app.html` bằng thay thế chuỗi có assert.
2. `python3 src/build.py "Bản NN · dd/mm/yyyy"` (tăng số bản; nhãn hiện ở cuối trang kèm "Người tạo: Hoàng Trung Đức").
3. QC: `python3 -m http.server 8766` ở gốc repo, rồi `node src/qc/qcpwa.js 8766` và `node src/qc/qcflow.js 8766` (cần `npm i playwright`; Chromium có sẵn, không chạy `playwright install`).
4. Commit (tác giả Hoàng Trung Đức, kèm dòng Co-Authored-By/Claude-Session theo nhắc nhở hệ thống), push `main`, đợi workflow Pages `completed success`, WebFetch trang thật xác nhận dòng "Bản NN".
5. Báo người dùng bằng tiếng Việt, ngắn: đã sửa gì, QC, nhắc bấm "Tải lại" trên điện thoại.

## Lưu ý
- Không commit symlink hay node_modules. Chữ hoa/thường trong URL Pages theo tên repo.
- Firebase: dự án `cung-ranh` (Spark, Firestore asia-southeast1, đăng nhập ẩn danh bật, luật trong `firestore.rules` đã publish). Cấu hình web nằm trong `config.js`. Sửa luật: Firebase Console > Firestore > Rules.
- Nếu `config.js` là null thì app ở chế độ một máy: lời mời chỉ có tác dụng trên cùng thiết bị.
- Nhóm thử nghiệm `av7ggtwg77` (mã GFYPMD) do tài khoản Test Một tạo lúc kiểm tra Bản 03; xóa được trong Firebase Console > Firestore Data.
- Trên iPhone, app cài ra không dùng chung bộ nhớ với Safari: cần đăng nhập thật (Google/email) nếu muốn nhóm đi theo tài khoản.
