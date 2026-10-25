import React from "react";
import { Globe, Heart } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-gray-100 border-t border-gray-200 mt-16 text-xs text-gray-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8 pb-8 border-b border-gray-200">
          <div className="space-y-3">
            <h4 className="font-bold text-gray-900 text-sm">Hỗ trợ</h4>
            <ul className="space-y-2">
              <li><a href="#" className="hover:underline">Trung tâm trợ giúp</a></li>
              <li><a href="#" className="hover:underline">Bảo vệ đặt phòng Airbnb Cover</a></li>
              <li><a href="#" className="hover:underline">Hỗ trợ người khuyết tật</a></li>
              <li><a href="#" className="hover:underline">Các tùy chọn hủy</a></li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="font-bold text-gray-900 text-sm">Cộng đồng</h4>
            <ul className="space-y-2">
              <li><a href="#" className="hover:underline">Diễn đàn cộng đồng Airbnb</a></li>
              <li><a href="#" className="hover:underline">Nhà ở cứu trợ khẩn cấp</a></li>
              <li><a href="#" className="hover:underline">Chống phân biệt đối xử</a></li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="font-bold text-gray-900 text-sm">Đón tiếp khách (Host)</h4>
            <ul className="space-y-2">
              <li><a href="#" className="hover:underline">Cho thuê nhà trên Airbnb</a></li>
              <li><a href="#" className="hover:underline">Bảo hiểm AirCover cho Chủ nhà</a></li>
              <li><a href="#" className="hover:underline">Tài nguyên đón tiếp khách</a></li>
              <li><a href="#" className="hover:underline">Đón tiếp khách có trách nhiệm</a></li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="font-bold text-gray-900 text-sm">Airbnb</h4>
            <ul className="space-y-2">
              <li><a href="#" className="hover:underline">Trang tin tức</a></li>
              <li><a href="#" className="hover:underline">Tính năng mới</a></li>
              <li><a href="#" className="hover:underline">Cơ hội nghề nghiệp</a></li>
              <li><a href="#" className="hover:underline">Nhà đầu tư</a></li>
            </ul>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 flex-wrap text-center sm:text-left">
            <span>© 2026 Airbnb Clone, Inc. Thiết kế theo tài liệu SRS Đặt phòng trực tuyến.</span>
            <span>•</span>
            <a href="#" className="hover:underline">Quyền riêng tư</a>
            <span>•</span>
            <a href="#" className="hover:underline">Điều khoản</a>
            <span>•</span>
            <a href="#" className="hover:underline">Sơ đồ trang web</a>
          </div>

          <div className="flex items-center gap-4 font-bold text-gray-800">
            <div className="flex items-center gap-1.5 cursor-pointer hover:underline">
              <Globe className="w-4 h-4" />
              <span>Tiếng Việt (VN)</span>
            </div>
            <span>₫ VND</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
